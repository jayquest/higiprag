# Create your views here.

def configuracoes_servicos_view(self,request):
    import forms
    from string import capitalize
    from django.utils.encoding import force_unicode
    from django.contrib.admin import  helpers

    model = self.model
    opts = model._meta
    prepopuled_fields = {}

    add, change = True,False

    if request.method == 'POST': # If the form has been submitted...

        form = forms.ConfigServicoForm(request.POST,request.FILES) # A form bound to the POST data

        if request.POST.has_key('_update'):
            form.fields['imagem'].required = False

        if form.is_valid(): # All validation rules pass

            form.fields['imagem'].required = True

            try:
                texto = TextoPagina.objects.get(slug='texto_servico')
            except:
                texto = TextoPagina()

            if texto.texto == None or texto.texto != form.cleaned_data['texto']:
                texto.texto = form.cleaned_data['texto']

            if not request.POST.has_key('_update') or request.FILES.has_key('imagem'):
                texto.imagem = request.FILES['imagem']



            texto.slug = 'texto_servico'
            texto.save()

            form = forms.ConfigServicoForm()
            form.initial['texto']  = texto.texto
            form.initial['imagem'] = texto.imagem

            change = True
            add = False
    else:
        form = forms.ConfigServicoForm()
        try:
            texto = TextoPagina.objects.get(slug='texto_servico')
            change = True
            add = False
            form.initial['texto']  = texto.texto
            form.initial['imagem'] = texto.imagem
        except:
            pass

    adminForm = helpers.AdminForm(form,[('Texto da página de serviços',{'fields':['imagem','texto']})],prepopuled_fields)

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
            }
        ,context_instance=RequestContext(request))


