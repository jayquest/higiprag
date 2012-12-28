__author__ = 'Johnny'

from django import forms

class ContactForm(forms.Form):
    nome = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'class':'input-field','style':'width:400px;'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-field','style':'width:400px;'}))
    assunto = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'class':'input-field','style':'width:400px;'}))
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'class':'input-field','style':'width:400px;'}))