from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Texto(models.Model):
    titulo = models.CharField(max_length=100,null=True,blank=True)
    texto = models.TextField()
    imagem = models.ImageField(upload_to='textos/',blank=True,null=True)
    slug = models.SlugField(max_length=120)

class Configuracao(models.Model):
    slug = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    usuario = models.ForeignKey(User)


