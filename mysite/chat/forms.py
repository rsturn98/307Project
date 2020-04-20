from django.forms import ModelForm
from .models import Rooms
from django import forms
from . import characters

class RoomForm(ModelForm):
    class Meta:
        model = Rooms
        fields = ['roomname']


charList = [(c.Name,c.Name) for c in characters.getAll()]
charList = tuple(charList)

class CharForm(forms.Form):
    char_name = forms.ChoiceField(label='Select Character', choices = charList)
