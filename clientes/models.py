from django.db import models

class Cliente(models.Model):
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf_cnpj = models.CharField(max_length=18, unique=True, verbose_name="CPF/CNPJ")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    endereco = models.TextField(verbose_name="Endereço")

    def __str__(self):
        return self.nome_completo