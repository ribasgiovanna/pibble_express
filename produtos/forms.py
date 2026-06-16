from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome_produto",
            "descricao",
            "peso",
            "quantidade_estoque",
            "valor",
            "categoria",
        ]
