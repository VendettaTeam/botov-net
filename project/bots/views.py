import os, json, logging
from django.http import HttpResponse
from django.http import HttpResponseServerError, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import BotModel
from .decorators import vk_success_response
from .request import RequestInfo
from project.bots.tasks import save_to_elastic
from project.bots.analyser.echo_analyser import EchoAnalyser
from project.bots.analyser.hashmap_analyser import HashMapAnalyser
from project.bots.analyser.elastic_analyser import ElasticAnalyser
from project.bots.analyser.nothing_analyser import NothingAnalyser

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
                request_info = RequestInfo(json_data, bot_obj)
                do_nothing = True if (os.environ['DJANGO_DO_NOTHING']).lower() in ("yes", "true", "1") else False
                if do_nothing:
                    return do_nothing_bot(request_info)
                return elasticsearch_bot(request_info)

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
def echo_bot(request_info: RequestInfo):
    if not request_info.is_appeal_to_bot():
        return

    analyser = EchoAnalyser(request_info)
    bot_response = analyser.get_response()
    bot_response.run()


@vk_success_response
def hashmap_bot(request_info: RequestInfo):
    if not request_info.is_appeal_to_bot():
        return

    analyser = HashMapAnalyser(request_info)
    bot_response = analyser.get_response()
    bot_response.run()


@vk_success_response
def elasticsearch_bot(request_info: RequestInfo):
    save_to_elastic.delay(request_info.request, request_info.bot_obj.pk)

    if not request_info.is_appeal_to_bot():
        return

    analyser = ElasticAnalyser(request_info)
    bot_response = analyser.get_response()
    bot_response.run()


@vk_success_response
def do_nothing_bot(request_info: RequestInfo):
    save_to_elastic.delay(request_info.request, request_info.bot_obj.pk)

    if not request_info.is_appeal_to_bot():
        return

    analyser = NothingAnalyser(request_info)
    bot_response = analyser.get_response()
    bot_response.run()
