import vk_api
import random
from project.bots.utils import is_chat
from .response import BotResponse
from .response_exception import ResponseException
from vk_api.utils import get_random_id


class InfaResponse(BotResponse):

    def setup(self, *args, **kwargs):
        if not is_chat(self.request_info.request):
            raise ResponseException("InfaResponse working only with chats")

    def get_message(self, vk):
        try:
            conversation_info = vk.messages.getConversationMembers(
                peer_id=self.request_info.request['object']['peer_id'])

            first_user = random.choice(conversation_info['profiles'])
            first_user = first_user['first_name'] + ' ' + first_user['last_name']

            second_user = random.choice(conversation_info['profiles'])
            second_user = second_user['first_name'] + ' ' + second_user['last_name']

            message = "{} {} {} {}".format(self.prefix_message(), first_user, self.get_infa(), second_user)

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

    def prefix_message(self):
        prefix = [
            "",
            "говорят, что",
            "ходит слушок, что",
            "я знаю, что",
            "вчера",
            "на той неделе",
            "год назад",
        ]
        return random.choice(prefix)

    def get_infa(self):
        infa_list = [
            "сосался с",
            "трахал",
            "подкатывал к",
            "дал пиздюлей",
            "отсосал у",
            "дунул с",
            "ударил",
            "пукнул на",
        ]
        infa_list_vip = [
            "подколол",
            "сел на лицо",
        ]
        if self.request_info.user_info.is_vip():
            infa_list += infa_list_vip

        return random.choice(infa_list)
