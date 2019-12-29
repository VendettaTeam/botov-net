import json
import requests
import vk_api
from .response import BotResponse
from vk_api.utils import get_random_id


class StoryResponse(BotResponse):
    def setup(self, *args, **kwargs):
        self.message = self.request_info.clean_message.lower()
        self.message = self.message.replace(kwargs['searched_message'], "", 1)
        self.message = self.message.strip(', ')

    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        if self.message != "":
            story_message = self.get_story()
            if story_message != "":
                vk.messages.send(
                    title=self.message,
                    message=story_message,
                    random_id=get_random_id(),
                    peer_id=self.request_info.request['object']['peer_id']
                )

    def get_story(self):
        url = 'https://models.dobro.ai/gpt2/medium/'
        headers = {
            'Content-type': 'application/json',
            'User-Agent': 'vk-bot (https://github.com/VendettaTeam/botov-net)',
            'Content-Encoding': 'utf-8'}
        data = {
            "prompt": self.message,
            "length": 60,
            "num_samples": 1
        }

        try:
            answer = requests.post(url, data=json.dumps(data), headers=headers)
            return answer.json()['replies'][0]
        except:
            return "Не удалось сгенерировать историю"
