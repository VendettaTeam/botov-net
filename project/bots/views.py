import json, logging
import vk_api
from vk_api.utils import get_random_id
from django.http import HttpResponse
from django.http import HttpResponseServerError, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import BotModel
from .decorators import vk_success_response
from .tasks import save_to_elastic
from .utils import is_appeal_to_bot, get_clean_message

logger = logging.getLogger(__name__)


# Create your views here.
@csrf_exempt
def entrypoint(request):
    """
    Entrypoint for vk callback api
    :param request:
    :return:
    """
    if request.method == "POST":
        json_data = json.loads(request.body)
        logger.debug(json_data)
        try:
            request_group_id = json_data['group_id']
            request_type = json_data['type']
            secret_key = json_data['secret']
            bot_obj = BotModel.objects.get(group_id=request_group_id)

            # validate request
            if not bot_obj:
                return HttpResponseServerError("Group is not found")

            if secret_key != bot_obj.secret_key:
                return HttpResponseServerError("Secret is invalid")

            if request_type == "confirmation":
                return confirmation_code(bot_obj)
            elif request_type == "message_new":
                return echo_bot(json_data, bot_obj)

            return HttpResponseServerError("Request type is invalid")

        except KeyError:
            return HttpResponseServerError("Malformed data!")
        except:
            return HttpResponseServerError("Unknown error")
    else:
        return HttpResponseNotAllowed("Method not allowed")


def confirmation_code(bot_obj):
    bot_obj.is_confirmed = True
    bot_obj.save()
    return HttpResponse(bot_obj.confirm_code)


@vk_success_response
def echo_bot(request_json, bot_obj):
    if not is_appeal_to_bot(request_json, bot_obj):
        return

    save_to_elastic.delay(request_json, bot_obj.pk)

    vk_session = vk_api.VkApi(token=bot_obj.api_key)
    vk = vk_session.get_api()

    message = get_clean_message(request_json, bot_obj)
    if message != "":
        vk.messages.send(
            message=message,
            random_id=get_random_id(),
            peer_id=request_json['object']['peer_id']
        )
