from .analyser import Analyser
from project.bots.response.response_answer import ResponseAnswer
from project.bots.response.response import BotResponse
from project.bots.response.unknown_response import UnknownResponse
from project.bots.documents import MessagesDocument
from project.bots.models import Messages


class ElasticAnalyser(Analyser):
    def get_response(self) -> BotResponse:
        elastic_resp = MessagesDocument.search().query("match", message=self.request_info.clean_message)
        elastic_resp = elastic_resp.to_queryset()

        # try to use first (more relevant) match
        # but if get exception, try to use another
        for match in elastic_resp:
            try:
                answer = Messages.objects.get(pk=match.id)
                response_class, payload = ResponseAnswer.get_response_class(answer.answer)

                resp = response_class(self.request_info)
                resp.setup(**payload)

                return resp

            except Exception as e:
                print(e)
                pass

        return UnknownResponse(self.request_info)
