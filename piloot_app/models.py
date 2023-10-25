from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE
from django.contrib.auth.models import User
# Create your models here.



class Empresa(models.Model):
    id_E = models.AutoField(primary_key=True)
    nome_empresa = models.TextField(max_length=255)


class Opcoes(models.Model):
    nome_op = models.TextField(max_length=255)

class EmpresaDFV(models.Model):
    idG = models.AutoField(primary_key=True)
    titulo = models.TextField(max_length=255)
    data = models.DateField()
    valor = models.FloatField()
    tipo = models.ForeignKey(Opcoes,blank=True,on_delete=models.CASCADE,null=True)
    empresa = models.ForeignKey(Empresa,blank=True,on_delete=models.CASCADE,null=False)
    qtd_parcelas = models.IntegerField()


class tema(models.Model):
    user = models.ForeignKey(User,blank=True,on_delete=models.CASCADE,null=True)
    tema_escolhido = models.TextField(max_length=255)
    


def cadastrarNaTab(dados):
    empresaDados = EmpresaDFV()
    empresaDados.titulo = dados["titulo"]
    empresaDados.data = dados["data"]
    empresaDados.valor = dados["valor"]
    empresaDados.tipo_id = dados["tipo"]
    empresaDados.empresa_id  = dados["empresa"]
    empresaDados.qtd_parcelas = dados["qtd"]
    empresaDados.save()

