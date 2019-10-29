import vk_api
from .response import BotResponse
from vk_api.utils import get_random_id


class EchoResponse(BotResponse):
    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        message = self.request_info.clean_message
        if message != "":
            vk.messages.send(
                message=message,
                random_id=get_random_id(),
                peer_id=self.request_info.request['object']['peer_id']
            )
