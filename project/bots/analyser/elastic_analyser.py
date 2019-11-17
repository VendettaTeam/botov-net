from .analyser import Analyser
from project.bots.response.response_answer import ResponseAnswer
from project.bots.response.response import BotResponse
from project.bots.response.unknown_response import UnknownResponse
from project.bots.documents import MessagesDocument
from project.bots.models import Messages


class ElasticAnalyser(Analyser):
    def get_response(self) -> BotResponse:
        if self.request_info.is_chat_invite_user():
            # TODO delete hardcode
            search_message = "помощь"
        else:
            search_message = self.request_info.clean_message

        elastic_resp = MessagesDocument.search().query("match", message=search_message)
        elastic_resp = elastic_resp.to_queryset()

        # TODO think about priority commands and text
        # first iterate over the first full occurrence
        for match in elastic_resp:
            print(search_message.lower())
            print(match.message.lower())
            if search_message.lower().startswith(match.message.lower()):
                bot_resp = self.return_response(match.id)
                if bot_resp != False:
                    return bot_resp

        # try to use first (more relevant) match
        for match in elastic_resp:
            bot_resp = self.return_response(match.id)
            if bot_resp != False:
                return bot_resp

        return UnknownResponse(self.request_info)

    def return_response(self, message_id):
        try:
            answer = Messages.objects.get(pk=message_id)
            response_class, payload = ResponseAnswer.get_response_class(answer.answer)
            payload['searched_message'] = answer.message

            resp = response_class(self.request_info)
            resp.setup(**payload)

            return resp

        except Exception as e:
            print(e)
            return False
