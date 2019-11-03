from django import forms
from django_json_widget.widgets import JSONEditorWidget
from .models import Messages, BotModel


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages

        fields = ('jsonfield',)

        widgets = {
            'jsonfield': JSONEditorWidget
        }


class BotForm(forms.ModelForm):
    class Meta:
        model = BotModel

        fields = ('jsonfield',)

        widgets = {
            'jsonfield': JSONEditorWidget
        }
