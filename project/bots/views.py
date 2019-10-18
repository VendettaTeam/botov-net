import json, logging
from django.http import HttpResponse
from django.http import HttpResponseServerError, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import BotModel
from .decorators import vk_success_response

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
            group = BotModel.objects.get(group_id=request_group_id)

            # validate request
            if not group:
                return HttpResponseServerError("Group is not found")

            if secret_key != group.secret_key:
                return HttpResponseServerError("Secret is invalid")

            if request_type == "confirmation":
                return confirmation_code(group)
            elif request_type == "message_new":
                return echo_bot(json_data, group)

            return HttpResponseServerError("Request type is invalid")

        except KeyError:
            return HttpResponseServerError("Malformed data!")
        except:
            return HttpResponseServerError("Unknown error")
    else:
        return HttpResponseNotAllowed("Method not allowed")


def confirmation_code(group):
    group.is_confirmed = True
    group.save()
    return HttpResponse(group.confirm_code)


@vk_success_response
def echo_bot(request_json, group):
    import vk_api
    from vk_api.utils import get_random_id

    vk_session = vk_api.VkApi(token=group.api_key)
    vk = vk_session.get_api()

    vk.messages.send(
        message=request_json['object']['body'],
        random_id=get_random_id(),
        peer_id=request_json['object']['user_id']
    )
