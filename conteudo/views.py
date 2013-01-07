#coding=utf8
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from forms import ContactForm
from conteudo.models import *
from blog.models import Artigo
from portfolio.models import *
from catalogo.models import *


def paginas_list(request):    

    paginas = [
        {'descricao':'Página Inicial','url':reverse('conteudo.views.index')},
        {'descricao':'Institucional','url':reverse('catalogo.views.listar')},
        {'descricao':'Serviços','url':reverse('portfolio.views.servicos')},
        {'descricao':'Produtos','url':reverse('catalogo.views.listar')},
        {'descricao':'Downloads','url':reverse('conteudo.views.documentos')},
        {'descricao':'Nóticias','url':reverse('blog.views.index')},
        {'descricao':'Contato','url':reverse('conteudo.views.contato')},
    ]

    return {'paginas':paginas}

def features_list(request):
    features = Feature.objects.all().order_by("?")[:3]

    return {'features':features}

def index(request):
    artigos = Artigo.objects.all()[:4]
    servicos = Servico.objects.order_by('?')[:3]
    banners = Banner.objects.order_by('?').all()[:4]
    portfolio = Trabalho.objects.order_by('?').all()[:4]
    produtos = Produto.objects.order_by('?').all()[:3]

    return render_to_response('index.html',{'artigos':artigos,'servicos':servicos,'banners':banners,'current':'home','portfolio':portfolio,'produtos':produtos},context_instance=RequestContext(request))

def home(request):
    return render_to_response('comingsoon.html',context_instance=RequestContext(request))

def paginas(request,slug):
    try:
        pagina = Pagina.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    return render_to_response('page.html',{'pagina':pagina,'current':pagina.slug},context_instance=RequestContext(request))


def documentos(request,pagina):

    docs_list = Documento.objects.all();

    paginator = Paginator(docs_list,8)

    try:
        docs = paginator.page(pagina)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    return render_to_response('documents.html',{'documentos':docs},context_instance=RequestContext(request))

def contato(request):
    sucesso = False

    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            contato = Contato()

            contato.nome = form.cleaned_data['nome']
            contato.email = form.cleaned_data['email']
            contato.assunto = form.cleaned_data['assunto']
            contato.mensagem = form.cleaned_data['mensagem']

            contato.save()

            sucesso = True


    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html',{'form':form,'current':'contato','sucesso':sucesso},context_instance=RequestContext(request))
