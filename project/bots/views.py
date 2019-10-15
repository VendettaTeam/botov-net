import json
from django.http import HttpResponse
from django.http import HttpResponseServerError, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import BotModel


# Create your views here.
@csrf_exempt
def confirmation_code(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        try:
            group_id = json_data['group_id']
            group = BotModel.objects.get(group_id=group_id)
            return HttpResponse(group.confirm_code)
        except KeyError:
            HttpResponseServerError("Malformed data!")
    else:
        return HttpResponseNotAllowed("Method not allowed")
