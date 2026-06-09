from django.db import models
from django.contrib.auth.models import User

class Funcionario(models.Model):

    TIPOS_USUARIO = (
        ('ADM', 'Administrador'),
        ('FUNC', 'Funcionário'),
    )

    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    endereco = models.TextField(verbose_name="Endereço")
    data_contratacao = models.DateField(verbose_name="Data de Contratação")

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='funcionario'
    )

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPOS_USUARIO,
        default='FUNC',
        verbose_name='Tipo de Usuário'
    )

    def __str__(self):
        return self.nome_completo