import vk_api, random, os
from vk_api.utils import get_random_id
from .response import BotResponse


class GirlsResponse(BotResponse):
    def setup(self, text_response=None, **payload):
        pass

    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        vk.messages.send(
            attachment=self.get_photo_attachment(),
            random_id=get_random_id(),
            peer_id=self.request_info.request['object']['peer_id']
        )

    def get_photo_attachment(self):
        f = open(os.path.dirname(os.path.abspath(__file__)) + '/static/girls.txt', 'r')
        photos_list = [line.strip() for line in f]

        return random.choice(photos_list)
