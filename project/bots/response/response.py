from abc import ABC, abstractmethod
from project.bots.request import RequestInfo
from project.bots.tasks import save_to_elastic


class BotResponse(ABC):

    def __init__(self, request_info: RequestInfo):
        self.request_info = request_info
        save_to_elastic.delay(self.request_info.request, self.request_info.bot_obj.pk)

    def setup(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass
