import vk_api
import random
from .response import BotResponse
from vk_api.utils import get_random_id


class UnknownResponse(BotResponse):
    def get_message(self):
        messages = [
            "Да",
            "Нет",
            "Навреное",
            "Не знаю",
        ]
        return random.choice(messages)

    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        vk.messages.send(
            message=self.get_message(),
            random_id=get_random_id(),
            peer_id=self.request_info.request['object']['peer_id']
        )
