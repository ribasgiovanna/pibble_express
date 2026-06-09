from django import forms

from .models import Funcionario


class FuncionarioForm(forms.ModelForm):

    username = forms.CharField(label="Usuário")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Senha"
    )

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
            "tipo_usuario",
        ]
        widgets = {
            "data_contratacao": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
