from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
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
    enable = models.BooleanField(default=False)
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


class UserInfo(models.Model):
    vk_id = models.BigIntegerField(unique=True)
    coins = models.BigIntegerField(default=0)
    vip_expire = models.DateTimeField(default=now)
    date = models.DateTimeField(default=now)

    def is_vip(self):
        if self.vip_expire > now():
            return True
        return False
