import json
from .request import RequestInfo
from .models import BotModel


def is_appeal_to_bot(request_info: RequestInfo):
    if not is_chat(request_info.request):
        return True
    else:
        for name in get_names(request_info.bot_obj):
            if request_info.request['object']['text'].startswith(name):
                return True, name

    return False


def get_names(bot_obj: BotModel):
    names = json.loads(bot_obj.names)
    return sorted(names, key=len, reverse=True)


def is_chat(request_json):
    if request_json['object']['peer_id'] >= 2000000000:
        return True
    return False


def get_clean_message(request_info: RequestInfo):
    """
    Return message without bots name
    :param request_info:
    :return:
    """
    message = request_info.request['object']['text']
    if is_chat(request_info.request):
        for name in get_names(request_info.bot_obj):
            if message.startswith(name):
                message = message[len(name):]
                return message.strip(',')

    return message
