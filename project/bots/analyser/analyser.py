from abc import ABC, abstractmethod
from project.bots.request import RequestInfo
from project.bots.response.response import BotResponse


class Analyser(ABC):
    def __init__(self, request_info: RequestInfo):
        self.request_info = request_info

    @abstractmethod
    def get_response(self) -> BotResponse:
        """
        Function will return BotResponse obj
        Simple example:
            input message -> response
        :return:
        """
        pass
