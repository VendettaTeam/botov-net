import vk_api, redis, json, os
from celery import shared_task
from datetime import datetime
from elasticsearch import Elasticsearch
from .models import BotModel
from .utils import is_chat
from .request import RequestInfo


@shared_task()
def save_to_elastic(request_json, bot_obj_pk):
    """
    Usage:
        celery worker -A project.settings
        celery worker -A project.settings -l ERROR
    :param request_json:
    :param bot_obj_pk:
    :return:
    """
    bot_obj = BotModel.objects.get(pk=bot_obj_pk)
    request_info = RequestInfo(request_json, bot_obj)

    print(request_info.request)

    obj = {
        'timestamp': datetime.now(),
        'bot_id': bot_obj.id,
        'text': request_info.request['object']['text'],
        'from_id': request_info.request['object']['from_id'],
        'is_chat': is_chat(request_info.request)
    }

    try:
        obj['user_info'] = get_vk_info_from_redis(request_info)

        es = Elasticsearch(hosts=os.environ['DJANGO_DOCKER_MACHINE_IP'])
        es.index(index="my_index", body=obj)
        print(obj['user_info'])
    except Exception as e:
        # TODO setup exception logging
        print(e)


def get_vk_info_from_redis(request_info: RequestInfo):
    prefix = 'vk-'
    r = redis.StrictRedis(host=os.environ['DJANGO_DOCKER_MACHINE_IP'], port=6379, db=0)
    vk_info = r.get(prefix + str(request_info.request['object']['from_id']))
    if vk_info is None:
        vk_session = vk_api.VkApi(token=request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        vk_info = vk.users.get(user_ids=request_info.request['object']['from_id'], fields="photo_50,city,verified")

        location = get_geo_location(vk_info[0]['city']['title'])
        if location:
            vk_info[0]['city']['location'] = location

        r.set(prefix + str(request_info.request['object']['from_id']), json.dumps(vk_info))

        return vk_info
    else:
        return json.loads(vk_info)


def get_geo_location(city_title):
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim()
        location = geolocator.geocode(city_title)

        return str(location.latitude) + "," + str(location.longitude)
    except:
        return None
