#coding=utf8

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.forms import CheckboxSelectMultiple

from django.test import TestCase
from catalogo import views
from catalogo.forms import OrcamentoForm1, CamaraResfriadoraForm
from catalogo.models import Categoria, Produto
from django import forms

class OrcamentoTeste(TestCase):
    def test_orcamento(self):
        form_list = []


        data_orcamento = {'endereco':'Teste',
                          'cidade':'Medianeira',
                          'estado':14,
                          'nome_completo':'Jonatas Wesley Gonçalves',
                          'telefone':'2312312321',
                          'email':'johnnyrox@gmail.com',
                          'ehCliente':False,
                          'observacoes':'Nada a declarar',
                          'receber_novidades':0}

        form = OrcamentoForm1(data_orcamento)
        form.is_valid()
        form_list.append(form)

        data_camaras = {'frigorifica':True,
                        'produto_armazenado':'Carne assada'}


        form = CamaraResfriadoraForm(data_camaras)
        form.is_valid()
        form_list.append(form)

        categorias = Categoria.objects.filter(categoria_superior__isnull=False)
        
        for categoria in categorias:
            fields = { 'categoria': forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple,label=categoria.titulo,queryset=Produto.objects.filter(categoria__slug__exact=categoria.slug),required=False)}
            data = {'categoria':['1']}
            form = type('CategoriaForm', (forms.BaseForm,), { 'base_fields': fields ,'data':data})
            form.is_valid()
            form_list.append(form)

        views.enviarOrcamentoEmail(form_list)

        self.assertTrue(True)
