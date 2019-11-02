from django.contrib import admin

# Register your models here.
from .models import BotModel, Messages

admin.site.register(BotModel)
admin.site.register(Messages)
