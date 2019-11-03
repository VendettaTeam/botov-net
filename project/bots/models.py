from django.db import models
from django.contrib.postgres.fields import JSONField
from project.bots.response.response_answer import ResponseAnswer


def default_names():
    return ["bot", "бот"]


# Create your models here.
class BotModel(models.Model):
    api_key = models.CharField(max_length=256, default='')
    confirm_code = models.CharField(max_length=256, default='')
    group_id = models.BigIntegerField(unique=True)
    secret_key = models.CharField(max_length=256, default='')
    is_confirmed = models.BooleanField(default=False)
    names = JSONField(default=default_names)
    comment = models.CharField(max_length=256, default='')

    def __str__(self):
        return 'BotModel: ' + self.comment


class Messages(models.Model):
    bot_id = models.ForeignKey(BotModel, on_delete=models.CASCADE)
    message = models.CharField(max_length=1024, default='')
    answer = JSONField(default=ResponseAnswer.default_answer_structure)

    def __str__(self):
        return 'Message: ' + self.message
