from .analyser import Analyser
from project.bots.response.response import BotResponse
from project.bots.response.echo_response import EchoResponse


class EchoAnalyser(Analyser):
    """
    Always return echo message
    """

    def get_response(self) -> BotResponse:
        return EchoResponse(self.request_info)
