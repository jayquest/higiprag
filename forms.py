#coding=utf8

from django.forms import CheckboxInput, CheckboxSelectMultiple
from catalogo.models import Produto, Categoria
from higiprag.models import Estado

__author__ = 'Johnny'

from django import forms

class OrcamentoForm1(forms.Form):
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(),empty_label="(Selecione um Estado)")
    cidade = forms.CharField(max_length=100)
    nome_completo = forms.CharField(max_length=200,label="Nome completo")
    endereco = forms.CharField(max_length=200,label="Endereço",required=False)
    telefone = forms.CharField(max_length=30)
    email = forms.EmailField()
    ehCliente = forms.ChoiceField(label="Você já é cliente Zero Grau?",widget=forms.RadioSelect,choices=([('1','Sim'),('0','Não')]),initial='0')
    observacoes = forms.CharField(widget=forms.Textarea,required=False)
    receber_novidades = forms.BooleanField(label="Gostaria de receber novidades em seu e-mail?",required=False)


class CamaraResfriadoraForm(forms.Form):
    frigorifica = forms.BooleanField(label="Camera Frigorífica",required=False)
    mini_camara = forms.BooleanField(label="Mini-Câmara",required=False)
    produto_armazenado = forms.CharField(max_length=100,required=False)
    temperatura_entrada = forms.CharField(max_length=8,required=False)
    temperatura_interna = forms.CharField(max_length=8,required=False)
    carga_diaria = forms.CharField(max_length=8,label="Carga diária(kg)",required=False)
    medidas_externas = forms.CharField(max_length=50,required=False)
    porta_giratoria = forms.BooleanField(label="Porta Giratória",required=False)
    porta_corredeira = forms.BooleanField(label="Porta Corredeira",required=False)


def make_categoria_form(categoria):
    fields = { 'categoria': forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple,label=categoria.titulo,queryset=Produto.objects.filter(categoria__slug__exact=categoria.slug),required=False)}
    return type('CategoriaForm', (forms.BaseForm,), { 'base_fields': fields })

def forms_orcamento():
    form_list = [OrcamentoForm1,CamaraResfriadoraForm]

    categorias = Categoria.objects.filter(categoria_superior__isnull=False)

    for c in categorias:
        if c.produtos().count() > 0:
            form_list.append(make_categoria_form(c))

    return form_list





