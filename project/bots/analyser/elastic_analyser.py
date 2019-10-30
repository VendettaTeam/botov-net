from .analyser import Analyser
from project.bots.response.response import BotResponse


class ElasticAnalyser(Analyser):
    def get_response(self) -> BotResponse:
        """
        if message len < 5:
            first
        if message in elastic:
            second
        """
        pass
