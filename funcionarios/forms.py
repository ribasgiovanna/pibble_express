from django import forms
from django.contrib.auth.models import User

from .models import Funcionario


def apenas_numeros(valor):
    return "".join(numero for numero in valor if numero.isdigit())


def formatar_cpf(valor):
    numeros = apenas_numeros(valor)
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:11]}"


def formatar_cnpj(valor):
    numeros = apenas_numeros(valor)
    return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:14]}"


def formatar_telefone(valor):
    numeros = apenas_numeros(valor)
    if len(numeros) == 10:
        return f"({numeros[:2]}){numeros[2:6]}-{numeros[6:10]}"
    return f"({numeros[:2]}){numeros[2:7]}-{numeros[7:11]}"


class FuncionarioForm(forms.ModelForm):

    username = forms.CharField(label="Usuário")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Senha",
        required=False,
        help_text="Deixe em branco para manter a senha atual (ao editar).",
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
            "cpf": forms.TextInput(
                attrs={
                    "data-mask": "cpf-cnpj",
                    "data-max-digits": "14",
                    "inputmode": "numeric",
                    "placeholder": "000.000.000-00 ou 00.000.000/0000-00",
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "data-mask": "telefone",
                    "data-max-digits": "11",
                    "inputmode": "numeric",
                    "placeholder": "(00)00000-0000",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cpf"].widget.attrs.pop("maxlength", None)
        self.fields["telefone"].widget.attrs.pop("maxlength", None)
        if self.instance.pk and self.instance.usuario_id:
            self.fields["username"].initial = self.instance.usuario.username
            

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        total_numeros = len(apenas_numeros(cpf))
        if total_numeros == 11:
            return formatar_cpf(cpf)
        if total_numeros == 14:
            return formatar_cnpj(cpf)
        raise forms.ValidationError("CPF/CNPJ inválido")

    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        total_numeros = len(apenas_numeros(telefone))
        if total_numeros not in (10, 11):
            raise forms.ValidationError("Telefone inválido")
        return formatar_telefone(telefone)

    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = User.objects.filter(username=username)
        if self.instance.pk and self.instance.usuario_id:
            qs = qs.exclude(pk=self.instance.usuario_id)
        if qs.exists():
            raise forms.ValidationError("Já existe um usuário com esse nome.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        is_novo = not (self.instance.pk and self.instance.usuario_id)
        if is_novo and not cleaned_data.get("password"):
            self.add_error("password", "A senha é obrigatória ao cadastrar um funcionário.")
        return cleaned_data

    def save(self, commit=True):
        funcionario = super().save(commit=False)

        username = self.cleaned_data["username"]
        password = self.cleaned_data.get("password")
        is_admin = self.cleaned_data.get("tipo_usuario") == "ADM"

        if funcionario.usuario_id:
            user = funcionario.usuario
            user.username = username
        else:
            user = User(username=username)

        user.email = self.cleaned_data.get("email", "")
        user.first_name = self.cleaned_data.get("nome_completo", "")[:150]
        user.is_staff = is_admin
        user.is_superuser = is_admin
        if password:
            user.set_password(password)
        user.save()

        funcionario.usuario = user
        if commit:
            funcionario.save()
        return funcionario
