from django import forms
from django.contrib.auth.models import User

from .models import Funcionario


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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ao editar, pré-preenche o nome de usuário a partir do User vinculado.
        if self.instance.pk and self.instance.usuario_id:
            self.fields["username"].initial = self.instance.usuario.username

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
        # A senha só é obrigatória ao cadastrar um novo funcionário (sem User ainda).
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
