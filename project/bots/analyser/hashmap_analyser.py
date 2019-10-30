from .analyser import Analyser
from project.bots.response.response import BotResponse
from project.bots.response.text_response import TextResponse


class HashMapAnalyser(Analyser):
    text = {
        'привет': 'Привет',
        'хай': 'Привет',
        'куку': 'Хаюшки'
    }

    def get_response(self) -> BotResponse:
        bot_resp = TextResponse(self.request_info)
        print(self.request_info.clean_message.lower())
        answer = self.text.get(self.request_info.clean_message.lower())
        if answer:
            bot_resp.setup(answer)
        else:
            bot_resp.setup('Не найдено')

        return bot_resp
