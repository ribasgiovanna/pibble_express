from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome_completo", "cpf_cnpj", "telefone", "email", "endereco"]
