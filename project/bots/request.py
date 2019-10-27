from .models import BotModel


class RequestInfo:
    """
    Contains all info about input request
    """
    def __init__(self, request, bot_obj: BotModel):
        self.request = request
        self.bot_obj = bot_obj
