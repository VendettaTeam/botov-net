import vk_api
from vk_api.utils import get_random_id
from .response import BotResponse
from .response_exception import ResponseException


class TextResponse(BotResponse):
    def setup(self, *args, **kwargs):
        if 'text_response' not in kwargs:
            raise ResponseException("No text_response field")

        self.text_response = kwargs['text_response']
        self.attachment = kwargs['attachment'] if 'attachment' in kwargs else None

    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        message = self.text_response
        attachment = self.attachment
        if message != "" or attachment != "":
            vk.messages.send(
                message=message,
                attachment=attachment,
                random_id=get_random_id(),
                peer_id=self.request_info.request['object']['peer_id']
            )
