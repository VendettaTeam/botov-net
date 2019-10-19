from django.db import models


# Create your models here.
class BotModel(models.Model):
    api_key = models.CharField(max_length=256, default='')
    confirm_code = models.CharField(max_length=256, default='')
    group_id = models.BigIntegerField(unique=True)
    secret_key = models.CharField(max_length=256, default='')
    is_confirmed = models.BooleanField(default=False)
    names = models.TextField(null=True)
