#coding=utf8
from datetime import datetime
import Image
from django.db import models
from django.core.validators import MaxLengthValidator
from django.db.models import signals
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

class Institucional(models.Model):
    titulo = models.CharField(max_length=30)
    texto = models.TextField()
    data_publicacao = models.DateField()
    data_fim_public = models.DateField()
    slug = models.SlugField(max_length=30)
    def __unicode__(self):
        return self.titulo + ' (' + self.pagina.titulo + ')'
    class Meta:
        verbose_name = 'publicação'
        verbose_name_plural = 'publicações'

class Banner(models.Model):
    titulo = models.CharField(max_length=40)
    texto = models.TextField(validators=[MaxLengthValidator(300)],blank=True)
    imagem = models.ImageField(upload_to='banners')
    link = models.URLField(blank=True)
    def __unicode__(self):
        return self.titulo

class Contato(models.Model):
    nome = models.CharField(max_length=60)
    email = models.EmailField()
    assunto = models.CharField(max_length=60)
    mensagem = models.TextField()
    data_hora = models.DateTimeField()
    respondido = models.BooleanField()

    class Meta:
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'
        permissions = (('config','Can modify contato settings'),)


class TextoContato(models.Model):
    titulo = models.CharField(max_length=100,null=True,blank=True)
    texto = models.TextField()
    slug = models.SlugField(max_length=100)

class ConfiguracoesContato(models.Model):
    razao_social = models.CharField(max_length=100,null=True,blank=True, verbose_name='razão social')
    nome_fantasia = models.CharField(max_length=100,null=True,blank=True, verbose_name='nome fantasia')
    endereco = models.CharField(max_length=100,verbose_name='endereço')
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    CEP = models.CharField(max_length=12,null=True,blank=True,verbose_name='CEP')

    telefone = models.CharField(max_length=100,null=True,blank=True)
    telefone_secundario = models.CharField(max_length=100,null=True,blank=True)
    celular = models.CharField(max_length=100,null=True,blank=True)
    celular_secundario = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField()

    slug = models.SlugField(max_length=100)

class Feature(models.Model):
    titulo = models.CharField(max_length=14)
    descricao = models.CharField(max_length=110)
    icone = models.ImageField(upload_to='icones')
    slug = models.SlugField(max_length=100)

class Documento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='documentos')
    tags = TaggableManager()

    def tipo_arquivo(self):
        if self.arquivo:
            name = self.arquivo.name
            split = name.split('.')

            ext = split[split.__len__() - 1]
            return ext

    def tipo_arquivo_imagem(self):
        from higiprag import settings

        static_images = ''

        for name, path in settings.STATICFILES_DIRS:
            if(name == 'images'):
                static_images = path

        if(self.tipo_arquivo() == 'doc' or self.tipo_arquivo() == 'docx'):
            image_file = type('imageobj', (object,), {'url':settings.STATIC_URL +'images/documentos/doc.jpg','path':static_images +'/documentos/doc.jpg'})
            return image_file
        if(self.tipo_arquivo() == 'xls' or self.tipo_arquivo() == 'xlsx'):
            image_file = type('imageobj', (object,), {'url':settings.STATIC_URL +'images/documentos/excel.png','path':static_images +'/documentos/excel.png'})
            return image_file
        if(self.tipo_arquivo() == 'pdf'):
            image_file = type('imageobj', (object,), {'url':settings.STATIC_URL +'images/documentos/pdf.png','path':static_images +'/documentos/pdf.png'})
            return image_file

        image_file = type('imageobj', (object,), {'url':settings.STATIC_URL +'images/documentos/outros.jpg','path':static_images +'/documentos/outros.jpg'})

        return image_file
# SIGNALS

def pagina_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Pagina.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def feature_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Feature.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def publicacao_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Institucional.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

class Estado(models.Model):
    descricao = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)
    uf = models.CharField(max_length=4)

    def __unicode__(self):
        return self.descricao

def contato_pre_save(signal,instance,sender, **kwargs):
    instance.data_hora = datetime.now()

def contato_post_save(signal,instance,sender, **kwargs):
    email_contato = ['contato@jwg.com.br']

    from django.core.mail import send_mail
    send_mail(instance.assunto, instance.mensagem, instance.email, email_contato)


signals.pre_save.connect(contato_pre_save,sender=Contato)

#SIGNALS POST-SAVE

signals.post_save.connect(contato_post_save,sender=Contato)
signals.pre_save.connect(feature_pre_save,sender=Feature)
signals.pre_save.connect(publicacao_pre_save,sender=Institucional)

