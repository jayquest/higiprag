#coding=utf8
from django.db import models
from django.core.validators import MaxLengthValidator

class Categoria(models.Model):
    titulo = models.CharField(max_length=30)
    categoria_superior = models.ForeignKey('self', blank=True, null=True, related_name='subcategorias',help_text="Selecione a categoria superior caso essa categoria seja uma subcategoria")
    slug = models.SlugField(max_length=60)
    class Meta:        
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def produtos(self):
        return Produto.objects.filter(Q(categoria__slug__exact=self.slug)|(Q(categoria__categoria_superior__slug__exact=self.slug)))

    def __unicode__(self):                            
        if self.categoria_superior is None:
            return self.titulo
        return self.categoria_superior.titulo + '->' + self.titulo
        
class Caracteristica(models.Model):
    titulo = models.CharField(max_length=80)
    slug = models.SlugField(max_length=120)
    class Meta:
        verbose_name = "característica"
        verbose_name_plural = "características"
    def __unicode__(self):
        return self.titulo

class Produto(models.Model):
    titulo = models.CharField(max_length=100)    
    categoria = models.ForeignKey(Categoria)    
    descricao = models.TextField(validators=[MaxLengthValidator(140)],blank=True,null=True)
    slug = models.SlugField(max_length=120)
    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"
    
    def __unicode__(self):
        return self.titulo + ' (' + self.categoria.titulo + ')'

    def imagem(self):
        if self.imagensproduto_set.count() > 0:
            return self.imagensproduto_set.order_by('-inicial')[0].imagem
        return None

class ImagensProduto(models.Model):
    produto = models.ForeignKey(Produto)
    imagem = models.ImageField(upload_to='produtos')
    inicial = models.BooleanField()

    class Meta:
        verbose_name = "imagem do produto"
        verbose_name_plural = "imagens do produto"
    def __unicode__(self):
        return self.produto.titulo + ' - ' + self.imagem.url

class ArquivoProduto(models.Model):
    produto = models.ForeignKey(Produto)
    arquivo = models.FileField(upload_to='produtos/arquivos')
    descricao = models.CharField(max_length=140)

    class Meta:
        verbose_name = "arquivo do produto"
        verbose_name_plural = "arquivos do produto"

class CaracteristicaProduto(models.Model):
    produto = models.ForeignKey(Produto)
    caracteristica = models.ForeignKey(Caracteristica)
    valor = models.CharField(max_length=100)
    class Meta:
        verbose_name = "característica do produto"
        verbose_name_plural = "características do produto"
    def __unicode__(self):
        return self.caracteristica.titulo + ' - ' + self.valor


#################   SIGNALS  ################

from django.db.models import signals, Q
from django.template.defaultfilters import slugify

def categoria_pre_save(signal,instance,sender, **kwargs):
    """Este signal gera um slug automaticamente. Ele verifica se ja existe um
    artigo com o mesmo slug e acrescenta um numero ao final para evitar
    duplicidade"""

    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Categoria.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def caracteristica_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Caracteristica.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def produto_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Produto.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

signals.pre_save.connect(caracteristica_pre_save,sender=Caracteristica)
signals.pre_save.connect(produto_pre_save,sender=Produto)
signals.pre_save.connect(caracteristica_pre_save,sender=Categoria)
