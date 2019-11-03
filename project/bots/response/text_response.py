import vk_api
from vk_api.utils import get_random_id
from .response import BotResponse
from .response_exception import ResponseException


class TextResponse(BotResponse):
    def setup(self, text_response=None, **payload):
        if not text_response and 'text_response' not in payload:
            raise ResponseException("No text_response field")

        if 'text_response' not in payload:
            self.text_response = text_response
        else:
            self.text_response = payload['text_response']

    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        message = self.text_response
        if message != "":
            vk.messages.send(
                message=message,
                random_id=get_random_id(),
                peer_id=self.request_info.request['object']['peer_id']
            )
