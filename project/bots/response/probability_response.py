import vk_api
import random
from .response import BotResponse
from vk_api.utils import get_random_id


class ProbabilityResponse(BotResponse):
    def get_message(self):
        return str(random.randint(0, 100)) + "%"

    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        vk.messages.send(
            message=self.get_message(),
            random_id=get_random_id(),
            peer_id=self.request_info.request['object']['peer_id']
        )
