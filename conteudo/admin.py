#coding=utf-8
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

#
#    def configuracoes_servicos_view(self,request):
#        import forms
#        from string import capitalize
#        from django.utils.encoding import force_unicode
#        from django.contrib.admin import  helpers
#
#        model = self.model
#        opts = model._meta
#        prepopuled_fields = {}
#
#        add, change = True,False
#
#        if request.method == 'POST': # If the form has been submitted...
#
#            form = forms.ConfigServicoForm(request.POST,request.FILES) # A form bound to the POST data
#
#            if request.POST.has_key('_update'):
#                form.fields['imagem'].required = False
#
#            if form.is_valid(): # All validation rules pass
#
#                form.fields['imagem'].required = True
#
#                try:
#                    texto = TextoPagina.objects.get(slug='texto_servico')
#                except:
#                    texto = TextoPagina()
#
#                if texto.texto == None or texto.texto != form.cleaned_data['texto']:
#                    texto.texto = form.cleaned_data['texto']
#
#                if not request.POST.has_key('_update') or request.FILES.has_key('imagem'):
#                    texto.imagem = request.FILES['imagem']
#
#
#
#                texto.slug = 'texto_servico'
#                texto.save()
#
#                form = forms.ConfigServicoForm()
#                form.initial['texto']  = texto.texto
#                form.initial['imagem'] = texto.imagem
#
#                change = True
#                add = False
#        else:
#            form = forms.ConfigServicoForm()
#            try:
#                texto = TextoPagina.objects.get(slug='texto_servico')
#                change = True
#                add = False
#                form.initial['texto']  = texto.texto
#                form.initial['imagem'] = texto.imagem
#            except:
#                pass
#
#        adminForm = helpers.AdminForm(form,[('Texto da página de serviços',{'fields':['imagem','texto']})],prepopuled_fields)
#
#        return render_to_response('admin/config_form.html',
#            {
#                'add':add,
#                'change':change,
#                'title': 'Configurações',
#                'is_popup': "_popup" in request.REQUEST,
#                'show_delete': False,
#                'has_delete_permission':False,
#                'has_add_permission':True,
#                'has_change_permission':True,
#                'errors': form.errors,
#                'app_label': opts.app_label,
#                'current_app':capitalize(opts.app_label),
#                'all_app_list':self.admin_site.all_app_list(request),
#                'module_name': force_unicode(opts.verbose_name_plural),
#                'opts':opts,
#                'has_file_field':True,
#                'adminform':adminForm,
#                'save_as':False,
#                }
#            ,context_instance=RequestContext(request))
#
#    def get_urls(self):
#        urls = super(ServicosAdmin, self).get_urls()
#        info = self.model._meta.app_label, self.model._meta.module_name
#        my_urls = patterns('',
#            url(r'^config/$', custom_admin.custom_site.admin_view(self.configuracoes_servicos_view),name='%s_%s_config' % info),
#        )
#        return my_urls + urls


class DocumentosAdmin(CustomModelAdmin):
    list_display = ('titulo','descricao','tipo_arquivo')
    search_fields = ['titulo','descricao']

custom_admin.custom_site.register(Feature,FeatureAdmin)
custom_admin.custom_site.register(Banner,BannerAdmin)
#custom_admin.custom_site.register(Pagina,PaginasAdmin)
#custom_admin.custom_site.register(Publicacao,PublicacoesAdmin)
custom_admin.custom_site.register(Contato,ContatoAdmin)
custom_admin.custom_site.register(Documento,DocumentosAdmin)