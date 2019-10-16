import json
from django.http import HttpResponse
from django.http import HttpResponseServerError, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import BotModel


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
        try:
            request_group_id = json_data['group_id']
            request_type = json_data['type']

            if request_type == "confirmation":
                return confirmation_code(request_group_id)

            return HttpResponseServerError("Request type is invalid")

        except KeyError:
            HttpResponseServerError("Malformed data!")
    else:
        return HttpResponseNotAllowed("Method not allowed")


def confirmation_code(group_id):
    group = BotModel.objects.get(group_id=group_id)
    return HttpResponse(group.confirm_code)
