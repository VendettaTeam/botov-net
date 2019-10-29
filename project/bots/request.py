from .utils import is_chat, get_names
from .models import BotModel


class RequestInfo:
    """
    Contains all info about input request
    """

    def __init__(self, request, bot_obj: BotModel):
        self.request = request
        self.bot_obj = bot_obj
        self.clean_message = self._get_clean_message()

    def is_appeal_to_bot(self):
        if not is_chat(self.request):
            return True
        else:
            for name in get_names(self.bot_obj):
                if self.request['object']['text'].startswith(name):
                    return True, name

        return False

    def _get_clean_message(self):
        """
        Return message without bots name
        :return:
        """
        message = self.request['object']['text']
        if is_chat(self.request):
            for name in get_names(self.bot_obj):
                if message.startswith(name):
                    message = message[len(name):]
                    return message.strip(',')

        return message
