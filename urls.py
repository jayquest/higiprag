'''
Created on 05/09/2012

@author: Johnny
'''

from django.conf.urls import patterns, url
from catalogo.views import OrcamentoWizard
from catalogo import forms

urlpatterns = patterns('catalogo.views',
    # Examples:
    # url(r'^$', 'NovoProjeto.views.home', name='home'),
    # url(r'^artigos/', include('NovoProjeto.Artigos.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^orcamentos/',OrcamentoWizard.as_view(form_list=forms.forms_orcamento(),template_name='orcamento.html'),name='orcamentos'),
    url(r'^detalhes/(?P<produto>[a-zA-Z0-9_.-]+)', 'produto',name='detalhes_produto'),
    url(r'^(?P<categoria>(?!\d{1,2})[a-zA-Z0-9_.-]+)?(/(?P<subcategoria>(?!\d{1,2})[a-zA-Z0-9_.-]+))?(/(?P<pagina>\d))?','listar',name='listar_produtos'),
)
