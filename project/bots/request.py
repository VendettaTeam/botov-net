from .utils import is_chat, get_names
from .models import BotModel, UserInfo


class RequestInfo:
    """
    Contains all info about input request
    """

    def __init__(self, request, bot_obj: BotModel):
        self._check_request_structure(request)

        self.request = request
        self.bot_obj = bot_obj
        self.user_info = UserInfo.objects.get_or_create(vk_id=request['object']['from_id'])[0]

        self.clean_message = self._get_clean_message()

    def is_appeal_to_bot(self):
        if not is_chat(self.request):
            return True
        else:
            for name in get_names(self.bot_obj):
                if self.request['object']['text'].startswith(name):
                    return True, name

        return False

    def _get_clean_message(self) -> str:
        """
        Return message without bots name
        :return:
        """
        message = self.request['object']['text']
        if is_chat(self.request):
            for name in get_names(self.bot_obj):
                if message.startswith(name):
                    message = message[len(name):]
                    return message.strip(', ')

        return message

    def _check_request_structure(self, request):
        """
        Example:
            'type': 'message_new',
            'object': {
                'date': 1572381124,
                'from_id': 41790945,
                'id': 423,
                'out': 0,
                'peer_id': 41790945,
                'text': 'hj',
                'conversation_message_id': 419,
                'fwd_messages': [],
                'important': False,
                'random_id': 0,
                'attachments': [],
                'is_hidden': False
            },
            'group_id': 187639144,
            'secret': '123321'
        """
        assert request['type'] in ['message_new', 'confirmation']
        # TODO check another fields
