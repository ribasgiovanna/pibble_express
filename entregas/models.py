from django.db import models
from clientes.models import Cliente
from funcionarios.models import Funcionario
from produtos.models import Produto

class Entrega(models.Model):
    STATUS_CHOICES = [
        ('CADASTRADO', 'Cadastrado'),
        ('EM_TRANSITO', 'Em Trânsito'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente Responsável")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto Enviado")
    funcionario_responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, verbose_name="Funcionário Responsável")
    
    endereco_entrega = models.TextField(verbose_name="Endereço de Entrega")
    data_envio = models.DateField(verbose_name="Data de Envio")
    data_prevista = models.DateField(verbose_name="Data Prevista")
    status_entrega = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CADASTRADO', verbose_name="Status da Entrega")

    def __str__(self):
        return f"Entrega #{self.id} - Status: {self.get_status_entrega_display()}"