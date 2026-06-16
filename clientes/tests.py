from django.test import TestCase

from .forms import ClienteForm


class ClienteFormTest(TestCase):
    def test_formata_cpf(self):
        form = ClienteForm(
            data={
                "nome_completo": "Cliente CPF",
                "cpf_cnpj": "12345678901",
                "telefone": "11999999999",
                "email": "cpf@example.com",
                "endereco": "Rua CPF",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["cpf_cnpj"], "123.456.789-01")

    def test_formata_cnpj(self):
        form = ClienteForm(
            data={
                "nome_completo": "Cliente CNPJ",
                "cpf_cnpj": "12345678000199",
                "telefone": "11999999999",
                "email": "cnpj@example.com",
                "endereco": "Rua CNPJ",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["cpf_cnpj"], "12.345.678/0001-99")

    def test_cpf_cnpj_field_nao_usa_maxlength_fixo(self):
        form = ClienteForm()
        widget_attrs = form.fields["cpf_cnpj"].widget.attrs

        self.assertNotIn("maxlength", widget_attrs)
        self.assertEqual(widget_attrs["data-max-digits"], "14")

    def test_telefone_usa_limite_por_digitos_sem_maxlength_fixo(self):
        form = ClienteForm()
        widget_attrs = form.fields["telefone"].widget.attrs

        self.assertNotIn("maxlength", widget_attrs)
        self.assertEqual(widget_attrs["data-max-digits"], "11")
