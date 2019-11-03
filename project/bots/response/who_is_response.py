import vk_api
import random
from project.bots.utils import is_chat
from .response import BotResponse
from .response_exception import ResponseException
from vk_api.utils import get_random_id


class WhoIsResponse(BotResponse):
    def setup(self, *args, **kwargs):
        if not is_chat(self.request_info.request):
            raise ResponseException("WhoIsResponse working only with chats")

    def get_people(self, vk):
        try:
            conversation_info = vk.messages.getConversationMembers(
                peer_id=self.request_info.request['object']['peer_id'])

            people = random.choice(conversation_info['profiles'])
            message = people['first_name'] + ' ' + people['last_name']

        except:
            message = "Для работы этой функции меня нужно назначить администратором"

        return message

    def run(self):

        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        vk.messages.send(
            message=self.get_people(vk),
            random_id=get_random_id(),
            peer_id=self.request_info.request['object']['peer_id']
        )
