from django.conf.urls import patterns, include, url
from blog.views import UltimosPosts
import custom_admin
import settings

custom_admin.autodiscover()

urlpatterns = patterns('',
    url(r'^servicos/(?P<servico>[a-zA-Z0-9_.-]+)', 'portfolio.views.detalhes_servicos', name='detalhar_servico'),
    url(r'^servicos/', 'portfolio.views.servicos', name='servicos'),
    url(r'^contato/', 'conteudo.views.contato', name='contato'),
    url(r'^documentos/(?P<pagina>\d)?', 'conteudo.views.documentos', name='documentos'),
    url(r'^blog/', include('blog.urls')),
    url(r'^catalogo/', include('catalogo.urls')),
    url(r'^portfolio/', include('portfolio.urls')),
    url(r'^feeds/$', UltimosPosts()),
    url(r'^ckeditor/', include('ckeditor.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(custom_admin.custom_site.urls)),
    url(r'^$', 'conteudo.views.index', name='home'),
)

if settings.MEDIA_ROOT == '':
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )