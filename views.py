#coding=utf8

# Create your views here.
from django.contrib.formtools.preview import FormPreview
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from catalogo.forms import OrcamentoForm1, CamaraResfriadoraForm
from catalogo.models import Categoria,Produto
from conteudo.models import Estado


def categorias_list(request):
    categorias = Categoria.objects.order_by('-titulo').all();
    return {'categorias_produtos':categorias}

def produto(request,produto):

    selected_produto = Produto.objects.get(slug__exact=produto)

    try:
        next_produto = Produto.objects.get(id=selected_produto.id+1)
    except:
        next_produto = None
    try:
        previous_produto = next_produto = Produto.objects.get(id=selected_produto.id-1)
    except:
        previous_produto = None

    return render_to_response('single_product.html',{'produto':selected_produto,'anterior':previous_produto,'proximo':next_produto},context_instance=RequestContext(request))

def listar(request,categoria,subcategoria,pagina):
    current_categoria = None

    if categoria is None and subcategoria is None:
        product_list = Produto.objects.all()
    else:
        if subcategoria is None:
            current_categoria = Categoria.objects.get(slug=categoria)
            #busca os produtos da categoria e das subcategorias da categoria especifica
            product_list = Produto.objects.filter(Q(categoria__slug__exact=categoria)|(Q(categoria__categoria_superior__slug__exact=categoria)))
        else:
            current_categoria = Categoria.objects.get(slug=subcategoria)
            #busca apenas os produtos diretamente relacionados a categoria
            product_list = Produto.objects.filter(categoria__slug=subcategoria)

    paginator = Paginator(product_list,9)

    try:
        produtos = paginator.page(pagina)
    except PageNotAnInteger:
        produtos = paginator.page(1)
    except EmptyPage:
        produtos = paginator.page(paginator.num_pages)

    if categoria is None and subcategoria is None:
        return render_to_response('products.html',{'produtos':produtos},context_instance=RequestContext(request))
    else:
        if subcategoria is None:
            return render_to_response('products.html',{'produtos':produtos,'categoria':current_categoria},context_instance=RequestContext(request))
        else:
            return render_to_response('products.html',{'produtos':produtos,'categoria':current_categoria.categoria_superior,'subcategoria':current_categoria},context_instance=RequestContext(request))


def fim_orcamento(request):
    return render_to_response('fim_orcamento.html',context_instance=RequestContext(request))

from django.contrib.formtools.wizard.views import SessionWizardView

class OrcamentoWizard(SessionWizardView):
#    def done(self, form_list, **kwargs):
#        return render_to_response('done.html', {'form_data': [form.cleaned_data for form in form_list],})
    def done(self, form_list, **kwargs):
        enviarOrcamentoEmail(form_list)
        return HttpResponseRedirect(reverse('catalogo.views.fim_orcamento'))




from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.formtools import models,preview,utils

def enviarOrcamentoEmail(form_list):


    dados_contato = [
        {'label':'Nome completo','data':form_list[0].cleaned_data['nome_completo']},
        {'label':'Endereço','data':form_list[0].cleaned_data['endereco']},
        {'label':'Cidade','data':form_list[0].cleaned_data['cidade']},
        {'label':'Estado','data':form_list[0].cleaned_data['estado'].descricao},
        {'label':'Telefone','data':form_list[0].cleaned_data['telefone']},
        {'label':'E-mail','data':form_list[0].cleaned_data['email']},
        {'label':'Já é cliente Zero Grau','data': "Sim" if form_list[0].cleaned_data['ehCliente'] == u'1' else 'Não' },
        {'label':'Observações','data':form_list[0].cleaned_data['observacoes']},
        {'label':'Deseja receber novidades','data': "Sim" if form_list[0].cleaned_data['receber_novidades']else "Não"},
    ]

    camara_resfriadora = [
        {'label':'Figorifica','data':"Sim" if form_list[1].cleaned_data['frigorifica']else "Não"},
        {'label':'Mini-câmara','data':"Sim" if form_list[1].cleaned_data['mini_camara']else "Não"},
        {'label':'Produto armazenado','data':form_list[1].cleaned_data['produto_armazenado']},
        {'label':'Temperatura de entrada','data':form_list[1].cleaned_data['temperatura_entrada']},
        {'label':'Temperatura interna','data':form_list[1].cleaned_data['temperatura_interna']},
        {'label':'Carga diaria','data':form_list[1].cleaned_data['carga_diaria']},
        {'label':'Medidas externas','data':form_list[1].cleaned_data['medidas_externas']},
        {'label':'Porta giratoria','data':"Sim" if form_list[1].cleaned_data['porta_giratoria'] else "Não"},
        {'label':'Porta corredeira','data':"Sim" if form_list[1].cleaned_data['porta_corredeira'] else "Não"},
    ]

    result_list = [
        {'titulo':"Dados de contato",'form':dados_contato},
        {'titulo':"Camara resfriadora",'form':camara_resfriadora},
    ]

    nome_completo = form_list[0].cleaned_data['nome_completo']

    i = 0
    for f in form_list:
        if i > 1:
            result_list.append({'titulo':None,'form':f})
        i+=1

    subject, from_email, to, acc = 'Orcamento: ' + nome_completo, 'orcamentos@zero.ind.br', 'johnnyrox@gmail.com', 'lucasebcanali@gmail.com'

    html_content = render_to_string('email_orcamento.html', {'result_list':result_list,'nome_completo':nome_completo}) # ...
    text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,acc])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

