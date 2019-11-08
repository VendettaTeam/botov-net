import vk_api
import random
from project.bots.utils import is_chat
from .response import BotResponse
from .response_exception import ResponseException
from vk_api.utils import get_random_id


class WeakToDoResponse(BotResponse):

    def setup(self, *args, **kwargs):
        if not is_chat(self.request_info.request):
            raise ResponseException("WhoIsResponse working only with chats")

    def get_weak_message(self):
        weak_list = [
            "поцеловать",
            "трахнуть",
            "наебать",
            "подкатить к",
            "дать пиздюлей",
            "отсосать у",
            "дать закурить",
            "занять",
            "ударить",
            "насмешить",
            "пукнуть на",
        ]
        weak_list_vip = [
            "подколоть",
            "сесть на лицо",
        ]
        if self.request_info.user_info.is_vip():
            weak_list += weak_list_vip

        return random.choice(weak_list)

    def get_message(self, vk):
        try:
            conversation_info = vk.messages.getConversationMembers(
                peer_id=self.request_info.request['object']['peer_id'])

            first_user = random.choice(conversation_info['profiles'])
            first_user = first_user['first_name'] + ' ' + first_user['last_name']

            second_user = random.choice(conversation_info['profiles'])
            second_user = second_user['first_name'] + ' ' + second_user['last_name']

            message = "{}, слабо {} {}".format(first_user, self.get_weak_message(), second_user)

        except:
            message = "Для работы этой функции меня нужно назначить администратором"

        return message

    def run(self):

        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        vk.messages.send(
            message=self.get_message(vk),
            random_id=get_random_id(),
            peer_id=self.request_info.request['object']['peer_id']
        )
