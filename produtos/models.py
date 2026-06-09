from django.db import models

class Produto(models.Model):
    nome_produto = models.CharField(max_length=255, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    peso = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Peso (kg)")
    quantidade_estoque = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    categoria = models.CharField(max_length=100, verbose_name="Categoria")

    def __str__(self):
        return self.nome_produto
