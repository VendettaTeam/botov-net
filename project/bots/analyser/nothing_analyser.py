from .analyser import Analyser
from project.bots.response.response import BotResponse
from project.bots.response.nothing_response import NothingResponse


class NothingAnalyser(Analyser):
    """
    Nothing do it
    """

    def get_response(self) -> BotResponse:
        return NothingResponse(self.request_info)
