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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome_produto"].widget.attrs["placeholder"] = "Digite o nome do produto"
        self.fields["descricao"].widget.attrs["placeholder"] = "Descreva o produto"
        self.fields["peso"].widget.attrs["placeholder"] = "Ex.: 1.50"
        self.fields["quantidade_estoque"].widget.attrs["placeholder"] = "Ex.: 100"
        self.fields["valor"].widget.attrs["placeholder"] = "Ex.: 99.90"
        self.fields["categoria"].widget.attrs["placeholder"] = "Ex.: Eletrônicos"
