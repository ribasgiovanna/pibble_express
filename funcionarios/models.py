from django.db import models

class Funcionario(models.Model):
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    endereco = models.TextField(verbose_name="Endereço")
    data_contratacao = models.DateField(verbose_name="Data de Contratação")

    def __str__(self):
        return f"{self.nome_completo} - {self.cargo}"
