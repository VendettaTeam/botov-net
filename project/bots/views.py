import json, logging
from django.http import HttpResponse
from django.http import HttpResponseServerError, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import BotModel
from .decorators import vk_success_response
from .request import RequestInfo
from project.bots.response.echo_response import EchoResponse

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

            request_info = RequestInfo(json_data, bot_obj)
            if request_type == "confirmation":
                return confirmation_code(request_info)
            elif request_type == "message_new":
                return echo_bot(request_info)

            return HttpResponseServerError("Request type is invalid")

        except KeyError:
            return HttpResponseServerError("Malformed data!")
        except:
            return HttpResponseServerError("Unknown error")
    else:
        return HttpResponseNotAllowed("Method not allowed")


def confirmation_code(request_info):
    request_info.bot_obj.is_confirmed = True
    request_info.bot_obj.save()
    return HttpResponse(request_info.bot_obj.confirm_code)


@vk_success_response
def echo_bot(request_info: RequestInfo):
    if not request_info.is_appeal_to_bot():
        return

    bot_response = EchoResponse(request_info)
    bot_response.run()
