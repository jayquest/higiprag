#coding=utf-8

from ckeditor.widgets import CKEditorWidget

__author__ = 'Johnny'

from django import forms

class ContactForm(forms.Form):
    nome = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'class':'input-field','style':'width:400px;'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-field','style':'width:400px;'}))
    assunto = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'class':'input-field','style':'width:400px;'}))
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'class':'input-field','style':'width:400px;'}))

class ConfigContatoForm(forms.Form):
    titulo = forms.CharField(max_length=100,label='Título')
    texto = forms.CharField(widget=CKEditorWidget())

    razao_social = forms.CharField(max_length=100,required=False, label='Razão Social')
    nome_fantasia = forms.CharField(max_length=100,required=False, label='Nome Fantasia')
    endereco = forms.CharField(max_length=100,label='Endereço')
    bairro = forms.CharField(max_length=100)
    cidade = forms.CharField(max_length=100)
    estado = forms.CharField(max_length=100)
    CEP = forms.CharField(max_length=12,label='CEP')

    telefone = forms.CharField(max_length=100,required=False)
    telefone_secundario = forms.CharField(max_length=100,required=False,label='2º Telefone')
    celular = forms.CharField(max_length=100,required=False)
    celular_secundario = forms.CharField(max_length=100,required=False,label='2º Celular')
    email = forms.EmailField()