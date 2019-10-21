import json


def is_appeal_to_bot(request_json, bot_obj):
    if not is_chat(request_json):
        return True
    else:
        for name in get_names(bot_obj):
            if request_json['object']['text'].startswith(name):
                return True, name

    return False


def get_names(bot_obj):
    names = json.loads(bot_obj.names)
    return sorted(names, key=len, reverse=True)


def is_chat(request_json):
    if request_json['object']['peer_id'] >= 2000000000:
        return True
    return False


def get_clean_message(request_json, bot_obj):
    """
    Return message without bots name
    :param request_json:
    :param bot_obj:
    :return:
    """
    message = request_json['object']['text']
    if is_chat(request_json):
        for name in get_names(bot_obj):
            if message.startswith(name):
                message = message[len(name):]
                return message.strip(',')

    return message
