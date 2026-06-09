from django import forms

from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            "nome_completo",
            "cpf",
            "cargo",
            "telefone",
            "email",
            "endereco",
            "data_contratacao",
        ]
        widgets = {
            "data_contratacao": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
