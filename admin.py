'''
Created on 04/09/2012

@author: Johnny
'''

from django.contrib import admin
from catalogo.models import *
from custom_admin.custom_model_admin import CustomModelAdmin
import custom_admin

class ImagensInline(admin.TabularInline):
    model = ImagensProduto    
    extra = 3

class ArquivosInline(admin.TabularInline):
    model = ArquivoProduto
    extra = 1

class CaracteristicasInline(admin.TabularInline):
    model = CaracteristicaProduto
    extra = 3

class ProdutosAdmin(CustomModelAdmin):
    list_display = ('titulo','categoria','descricao')   
    search_fields = ['titulo','descricao'] 
    list_filter = ['categoria']
    inlines = [ImagensInline,ArquivosInline,CaracteristicasInline]
    exclude = ['slug']

class CaracteristicasAdmin(CustomModelAdmin):
    list_display = ['titulo']
    search_fields = ['titulo']
    exclude = ['slug']

class CategoriasAdmin(CustomModelAdmin):
    list_display = ['titulo','categoria_superior']
    search_fields = ['titulo']
    exclude = ['slug']

custom_admin.custom_site.register(Produto,ProdutosAdmin)
custom_admin.custom_site.register(Categoria,CategoriasAdmin)
custom_admin.custom_site.register(Caracteristica,CaracteristicasAdmin)
