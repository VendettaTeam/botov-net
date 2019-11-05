from abc import ABC, abstractmethod
from project.bots.request import RequestInfo


class BotResponse(ABC):

    def __init__(self, request_info: RequestInfo):
        self.request_info = request_info

    def setup(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass
