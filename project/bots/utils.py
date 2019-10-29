import json
from .models import BotModel


def get_names(bot_obj: BotModel):
    names = json.loads(bot_obj.names)
    return sorted(names, key=len, reverse=True)


def is_chat(request_json):
    if request_json['object']['peer_id'] >= 2000000000:
        return True
    return False
