import vk_api, redis, json, os
from celery import shared_task
from datetime import datetime, date
from .models import BotModel
from .utils import is_chat
from .request import RequestInfo
from .documents import RequestsDocument


@shared_task()
def save_to_elastic(request_json, bot_obj_pk):
    bot_obj = BotModel.objects.get(pk=bot_obj_pk)
    request_info = RequestInfo(request_json, bot_obj)

    print(request_info.request)
    try:
        vk_user_info = get_user_info(request_info)

        doc = RequestsDocument()
        doc.init()

        doc.timestamp = datetime.now()
        doc.request_time = datetime.utcfromtimestamp(request_info.request['object']['date'])
        doc.bot_id = bot_obj.id
        doc.message = request_info.request['object']['text']
        doc.clean_message = request_info.clean_message
        doc.from_id = request_info.request['object']['from_id']
        doc.peer_id = request_info.request['object']['peer_id']
        doc.is_chat = is_chat(request_info.request)
        doc.is_appeal = request_info.is_appeal_to_bot()

        doc.user_info = vk_user_info
        bdate = get_bdate(vk_user_info)
        doc.location = get_geo_location(vk_user_info)
        doc.bdate = bdate
        doc.age = get_age(bdate)
        doc.sex = get_sex(vk_user_info)

        doc.save()
    except Exception as e:
        # TODO setup exception logging
        print(e)


def get_user_info(request_info: RequestInfo):
    prefix = 'vk-'
    redis_cache = redis.StrictRedis(host='botov_redis', port=6379, db=0)
    vk_info = redis_cache.get(prefix + str(request_info.request['object']['from_id']))
    if vk_info is None:
        vk_session = vk_api.VkApi(token=request_info.bot_obj.api_key)
        vk = vk_session.get_api()
        vk_info = vk.users.get(user_ids=request_info.request['object']['from_id'], fields="city,bdate,sex")

        redis_cache.set(prefix + str(request_info.request['object']['from_id']), json.dumps(vk_info))
        return vk_info
    else:
        return json.loads(vk_info)


def get_geo_location(vk_user_info):
    try:
        city_title = vk_user_info[0]['city']['title']
        from geopy.geocoders import Nominatim
        geolocator = Nominatim()
        location = geolocator.geocode(city_title)

        return str(location.latitude) + "," + str(location.longitude)
    except:
        return None


def get_bdate(vk_user_info):
    try:
        bdate = vk_user_info[0]['bdate']
        if len(bdate) > 5:
            return datetime.strptime(bdate, '%d.%m.%Y')
        return None
    except:
        return None


def get_age(born):
    if born is None:
        return None

    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_sex(vk_user_info):
    try:
        return int(vk_user_info[0]['sex'])
    except:
        return 0
