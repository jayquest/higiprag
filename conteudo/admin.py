#coding=utf-8
'''
Created on 04/09/2012

@author: Johnny
'''
from ckeditor.widgets import CKEditorWidget
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.templatetags.static import static
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

    def configuracoes_contato_view(self,request):
        import forms
        from string import capitalize
        from django.utils.encoding import force_unicode
        from django.contrib.admin import  helpers

        model = self.model
        opts = model._meta
        prepopuled_fields = {}

        add, change = True,False

        if request.method == 'POST': # If the form has been submitted...

            form = forms.ConfigContatoForm(request.POST) # A form bound to the POST data

            if form.is_valid(): # All validation rules pass

                try:
                    texto = TextoContato.objects.get(slug='texto_contato')
                except:
                    texto = TextoContato()

                try:
                    configs = ConfiguracoesContato.objects.get(slug='configs_contato')
                except:
                    configs = ConfiguracoesContato()

                texto.texto = form.cleaned_data['texto']
                texto.titulo = form.cleaned_data['titulo']

                configs.bairro = form.cleaned_data['bairro']
                configs.celular = form.cleaned_data['celular']
                configs.celular_secundario = form.cleaned_data['celular_secundario']
                configs.telefone = form.cleaned_data['telefone']
                configs.telefone_secundario = form.cleaned_data['telefone_secundario']
                configs.email = form.cleaned_data['email']
                configs.estado = form.cleaned_data['estado']
                configs.endereco = form.cleaned_data['endereco']
                configs.CEP = form.cleaned_data['CEP']
                configs.cidade = form.cleaned_data['cidade']
                configs.nome_fantasia = form.cleaned_data['nome_fantasia']
                configs.razao_social = form.cleaned_data['razao_social']

                configs.slug = 'configs_contato'
                configs.save()

                texto.slug = 'texto_contato'
                texto.save()

                form = forms.ConfigContatoForm()
                form.initial['texto']  = texto.texto
                form.initial['titulo'] = texto.titulo

                form.initial['bairro'] = configs.bairro
                form.initial['celular'] = configs.celular
                form.initial['celular_secundario'] = configs.celular_secundario
                form.initial['telefone'] = configs.telefone
                form.initial['telefone_secundario'] = configs.telefone_secundario
                form.initial['email'] = configs.email
                form.initial['estado'] = configs.estado
                form.initial['endereco'] = configs.endereco
                form.initial['CEP'] = configs.CEP
                form.initial['cidade'] = configs.cidade
                form.initial['nome_fantasia'] = configs.nome_fantasia
                form.initial['razao_social'] = configs.razao_social


                change = True
                add = False
        else:
            change = True
            add = False
            form = forms.ConfigContatoForm()
            try:
                texto = TextoContato.objects.get(slug='texto_contato')

                form.initial['texto']  = texto.texto
                form.initial['titulo'] = texto.titulo
            except:
                pass

            try:
                configs = ConfiguracoesContato.objects.get(slug='configs_contato')
                form.initial['bairro'] = configs.bairro
                form.initial['celular'] = configs.celular
                form.initial['celular_secundario'] = configs.celular_secundario
                form.initial['telefone'] = configs.telefone
                form.initial['telefone_secundario'] = configs.telefone_secundario
                form.initial['email'] = configs.email
                form.initial['estado'] = configs.estado
                form.initial['endereco'] = configs.endereco
                form.initial['CEP'] = configs.CEP
                form.initial['cidade'] = configs.cidade
                form.initial['nome_fantasia'] = configs.nome_fantasia
                form.initial['razao_social'] = configs.razao_social
            except:
                pass


        adminForm = helpers.AdminForm(
                            form,
                            [
                                (
                                    'Texto da página de contato',
                                    {'fields':['titulo','texto']}),
                                (
                                    'Informações de contato',
                                    {'fields':['nome_fantasia','razao_social','endereco','bairro','cidade','estado','CEP','celular','celular_secundario','telefone','telefone_secundario','email',]})
                            ]
                            ,prepopuled_fields)

        media = self.media + adminForm.media

        return render_to_response('admin/config_form.html',
            {
                'add':add,
                'change':change,
                'title': 'Configurações',
                'is_popup': "_popup" in request.REQUEST,
                'show_delete': False,
                'has_delete_permission':False,
                'has_add_permission':True,
                'has_change_permission':True,
                'errors': form.errors,
                'app_label': opts.app_label,
                'current_app':capitalize(opts.app_label),
                'all_app_list':self.admin_site.all_app_list(request),
                'module_name': force_unicode(opts.verbose_name_plural),
                'opts':opts,
                'has_file_field':True,
                'adminform':adminForm,
                'save_as':False,
                'media':media,
                }
            ,context_instance=RequestContext(request))

    def get_urls(self):
        urls = super(ContatoAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name
        my_urls = patterns('',
            url(r'^config/$', custom_admin.custom_site.admin_view(self.configuracoes_contato_view),name='%s_%s_config' % info),
        )
        return my_urls + urls

    def get_model_perms(self, request):
        permiss = super(ContatoAdmin, self).get_model_perms(request)
        permiss['add'] = False
        permiss['config'] = self.has_change_permission(request) and self.has_add_permission(request)
        return permiss

    @property
    def media(self):
        super_media = super(ContatoAdmin, self).media

        js = [
            'cufon-yui.js',
            'TitilliumText.font.js',
            'cufon-replace-ckeditor.js',
            ]

        current_media = forms.Media(js=[static('js/%s' % url) for url in js])

        media = super_media + current_media

        return media


class DocumentosAdmin(CustomModelAdmin):
    list_display = ('titulo','descricao','tipo_arquivo')
    search_fields = ['titulo','descricao']

custom_admin.custom_site.register(Feature,FeatureAdmin)
custom_admin.custom_site.register(Banner,BannerAdmin)
#custom_admin.custom_site.register(Pagina,PaginasAdmin)
#custom_admin.custom_site.register(Publicacao,PublicacoesAdmin)
custom_admin.custom_site.register(Contato,ContatoAdmin)
custom_admin.custom_site.register(Documento,DocumentosAdmin)