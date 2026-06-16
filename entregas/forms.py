from django import forms

from .models import Entrega


class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = [
            "cliente",
            "produto",
            "endereco_entrega",
            "data_envio",
            "data_prevista",
            "status_entrega",
            "funcionario_responsavel",
        ]
        widgets = {
            "data_envio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "data_prevista": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["endereco_entrega"].widget.attrs["placeholder"] = "Digite o endereço de entrega"
