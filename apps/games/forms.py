from django import forms
from .models import Game


class CreateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'price', 'poster', 'rate')