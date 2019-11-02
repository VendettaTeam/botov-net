from .analyser import Analyser
from project.bots.response.response import BotResponse


class ElasticAnalyser(Analyser):
    def get_response(self) -> BotResponse:
        """
        message: {
            # metric for neural
            ...
            response: [
                0: {
                    type: text_response|echo_response|bla_bla_response,
                    payload {
                        key1: value1,
                        key2: value2,
                    }
                },
            ]
        }

        if message len < 5:
            first
        if message in elastic:
            second
        """


        pass
