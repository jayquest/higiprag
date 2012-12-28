'''
Created on 04/09/2012

@author: Johnny
'''
from ckeditor.widgets import CKEditorWidget
from models import *
from custom_admin import custom_admin
from custom_admin.custom_model_admin import CustomModelAdmin
from django import forms

class BannerAdmin(CustomModelAdmin):
    list_display = ('imagem','titulo')   
    search_fields = ['titulo','texto']

class FeatureAdmin(CustomModelAdmin):
    list_display = ('icone','titulo','descricao')
    search_fields = ['titulo','descricao']
    exclude = ['slug']

class PaginasAdmin(CustomModelAdmin):
    list_display = ('titulo','breve_descricao','data_publicacao','data_fim_public')   
    list_filter = ['data_publicacao','data_fim_public']
    search_fields = ['titulo','breve_descricao']
    exclude = ['slug']

class PublicacoesAdmin(CustomModelAdmin):
    list_display = ('titulo','pagina','data_publicacao','data_fim_public')
    list_filter = ['pagina','data_publicacao','data_fim_public']   
    search_fields = ['titulo','descricao','pagina']
    exclude = ['slug']


class ContatoAdmin(CustomModelAdmin):
    list_display = ('data_hora','nome','email','assunto','respondido')
    list_filter = ['assunto','data_hora','respondido']
    search_fields = ['nome','email','assunto']
    exclude = ['data_hora']

class DocumentosAdmin(CustomModelAdmin):
    list_display = ('titulo','descricao','tipo_arquivo')
    search_fields = ['titulo','descricao']

custom_admin.custom_site.register(Feature,FeatureAdmin)
custom_admin.custom_site.register(Banner,BannerAdmin)
#custom_admin.custom_site.register(Pagina,PaginasAdmin)
#custom_admin.custom_site.register(Publicacao,PublicacoesAdmin)
custom_admin.custom_site.register(Contato,ContatoAdmin)
custom_admin.custom_site.register(Documento,DocumentosAdmin)