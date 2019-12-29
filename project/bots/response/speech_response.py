import os
import requests
import vk_api
from .response import BotResponse
from vk_api.utils import get_random_id


class SpeechResponse(BotResponse):
    def setup(self, *args, **kwargs):
        self.message = self.request_info.clean_message.lower()
        self.message = self.message.replace(kwargs['searched_message'], "", 1)
        self.message = self.message.strip(', ')
        if self.message == "":
            self.message = "Не понял"

    def run(self):
        vk_session = vk_api.VkApi(token=self.request_info.bot_obj.api_key)
        vk = vk_session.get_api()

        url = 'http://botov_speech_synthesis:5000/'
        # voice = random.choice(['anna', 'aleksandr', 'elena', 'irina'])
        voice = 'aleksandr'
        speech_resp = requests.post(url, data={
            'voice': voice,
            'message': self.message
        })
        if speech_resp.status_code == 200:
            try:
                upload = vk_api.VkUpload(vk_session)

                file = "/usr/share/RHVoice-data/" + speech_resp.text  # docker volume
                audio_message = upload.audio_message(file, peer_id=self.request_info.request['object']['peer_id'])
                doc = "doc{}_{}".format(audio_message['audio_message']['owner_id'],
                                        audio_message['audio_message']['id'])
                vk.messages.send(
                    random_id=get_random_id(),
                    attachment=doc,
                    peer_id=self.request_info.request['object']['peer_id']
                )

                os.remove(file)
            except:
                pass
