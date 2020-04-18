from django import forms
from . import characters

charList = [(c.Name,c.Name) for c in characters.getAll()]
charList = tuple(charList)

class CharForm(forms.Form):
    char_name = forms.ChoiceField(label='Select Character', choices = charList)
