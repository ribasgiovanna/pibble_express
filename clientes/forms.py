from django import forms

from .models import Cliente


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


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome_completo", "cpf_cnpj", "telefone", "email", "endereco"]
        labels = {
            "cpf_cnpj": "CPF/CNPJ",
        }
        widgets = {
            "cpf_cnpj": forms.TextInput(
                attrs={
                    "data-mask": "cpf-cnpj",
                    "data-max-digits": "14",
                    "inputmode": "numeric",
                    "placeholder": "CPF ou CNPJ",
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
        self.fields["cpf_cnpj"].widget.attrs.pop("maxlength", None)
        self.fields["telefone"].widget.attrs.pop("maxlength", None)
        self.fields["nome_completo"].widget.attrs["placeholder"] = "Digite o nome completo"
        self.fields["email"].widget.attrs["placeholder"] = "exemplo@email.com"
        self.fields["endereco"].widget.attrs["placeholder"] = "Digite o endereço completo"

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data["cpf_cnpj"]
        total_numeros = len(apenas_numeros(cpf_cnpj))
        if total_numeros < 11:
            raise forms.ValidationError("CPF/CNPJ inválido")
        if total_numeros == 11:
            return formatar_cpf(cpf_cnpj)
        if total_numeros == 14:
            return formatar_cnpj(cpf_cnpj)
        raise forms.ValidationError("CPF/CNPJ inválido")

    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        total_numeros = len(apenas_numeros(telefone))
        if total_numeros not in (10, 11):
            raise forms.ValidationError("Telefone inválido")
        return formatar_telefone(telefone)
