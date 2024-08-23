from .models import Client, Mailing, Message
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment', ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'text', ]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('user',)
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local',
                       'step': 3600, }
            ),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local',
                       'step': 3600, }
            )
        }


class MailingManagerForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['status', ]
