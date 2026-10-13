from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente

from .models import Funcionario


def criar_funcionario(username, tipo, cpf, email):
    usuario = User.objects.create_user(
        username=username,
        password="senha123",
        is_staff=(tipo == "ADM"),
        is_superuser=(tipo == "ADM"),
    )
    return Funcionario.objects.create(
        nome_completo=username.title(),
        cpf=cpf,
        cargo="Operador",
        telefone="(41) 99999-9999",
        email=email,
        endereco="Rua A, 1",
        data_contratacao=date(2026, 1, 1),
        usuario=usuario,
        tipo_usuario=tipo,
    )


class NiveisDeAcessoTest(TestCase):
    """ADM tem acesso às funções administrativas; FUNC opera os cadastros."""

    def setUp(self):
        self.adm = criar_funcionario("admin", "ADM", "111.111.111-11", "adm@example.com")
        self.func = criar_funcionario("operador", "FUNC", "222.222.222-22", "func@example.com")

    def test_funcionario_comum_nao_acessa_paginas_administrativas(self):
        self.client.force_login(self.func.usuario)
        for nome, args in [
            ("dashboard", []),
            ("funcionarios", []),
            ("editar_funcionario", [self.adm.pk]),
        ]:
            with self.subTest(pagina=nome):
                response = self.client.get(reverse(nome, args=args))
                self.assertEqual(response.status_code, 403)

    def test_funcionario_comum_nao_exclui_outro_funcionario(self):
        self.client.force_login(self.func.usuario)
        response = self.client.post(reverse("deletar_funcionario", args=[self.adm.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Funcionario.objects.filter(pk=self.adm.pk).exists())

    def test_funcionario_comum_opera_os_cadastros(self):
        self.client.force_login(self.func.usuario)
        for nome in ["clientes", "produtos", "entregas"]:
            with self.subTest(pagina=nome):
                self.assertEqual(self.client.get(reverse(nome)).status_code, 200)

    def test_administrador_acessa_tudo(self):
        self.client.force_login(self.adm.usuario)
        for nome in ["dashboard", "funcionarios", "clientes", "produtos", "entregas"]:
            with self.subTest(pagina=nome):
                self.assertEqual(self.client.get(reverse(nome)).status_code, 200)

    def test_menu_esconde_links_administrativos_do_funcionario_comum(self):
        self.client.force_login(self.func.usuario)
        response = self.client.get(reverse("clientes"))
        self.assertNotContains(response, 'href="/funcionarios/"')
        self.assertNotContains(response, 'href="/dashboard/"')

    def test_login_leva_cada_perfil_para_a_sua_pagina_inicial(self):
        response = self.client.post(reverse("login"), {"username": "admin", "password": "senha123"})
        self.assertRedirects(response, reverse("dashboard"))
        self.client.logout()
        response = self.client.post(reverse("login"), {"username": "operador", "password": "senha123"})
        self.assertRedirects(response, reverse("entregas"))

    def test_administrador_exclui_funcionario_e_o_usuario_dele(self):
        self.client.force_login(self.adm.usuario)
        usuario_id = self.func.usuario_id
        response = self.client.post(reverse("deletar_funcionario", args=[self.func.pk]))
        self.assertRedirects(response, reverse("funcionarios"))
        self.assertFalse(Funcionario.objects.filter(pk=self.func.pk).exists())
        self.assertFalse(User.objects.filter(pk=usuario_id).exists())


class ExclusaoSoPorPostTest(TestCase):
    """Excluir por um link (GET) permitiria que outro site disparasse exclusões (CSRF)."""

    def setUp(self):
        self.adm = criar_funcionario("admin", "ADM", "111.111.111-11", "adm@example.com")
        self.cliente = Cliente.objects.create(
            nome_completo="Cliente", cpf_cnpj="123.456.789-01", telefone="1", email="c@example.com", endereco="Rua"
        )
        self.client.force_login(self.adm.usuario)

    def test_get_nao_exclui(self):
        response = self.client.get(reverse("deletar_cliente", args=[self.cliente.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())

    def test_post_exclui(self):
        response = self.client.post(reverse("deletar_cliente", args=[self.cliente.pk]))
        self.assertRedirects(response, reverse("clientes"))
        self.assertFalse(Cliente.objects.filter(pk=self.cliente.pk).exists())

    def test_post_sem_token_csrf_e_recusado(self):
        from django.test import Client

        navegador = Client(enforce_csrf_checks=True)
        navegador.force_login(self.adm.usuario)
        response = navegador.post(reverse("deletar_cliente", args=[self.cliente.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())

    def test_lista_usa_formulario_com_token_para_excluir(self):
        response = self.client.get(reverse("clientes"))
        self.assertContains(response, 'class="delete-form"')
        self.assertContains(response, "csrfmiddlewaretoken")


class ApiTest(TestCase):
    """A API REST não pode ficar aberta para quem não fez login."""

    def setUp(self):
        self.adm = criar_funcionario("admin", "ADM", "111.111.111-11", "adm@example.com")
        self.func = criar_funcionario("operador", "FUNC", "222.222.222-22", "func@example.com")

    def test_api_exige_login(self):
        for recurso in ["clientes", "produtos", "entregas", "funcionarios"]:
            with self.subTest(recurso=recurso):
                response = self.client.get(f"/api/{recurso}/")
                self.assertIn(response.status_code, (401, 403))

    def test_api_nao_permite_excluir_sem_login(self):
        cliente = Cliente.objects.create(
            nome_completo="Cliente", cpf_cnpj="123.456.789-01", telefone="1", email="c@example.com", endereco="Rua"
        )
        response = self.client.delete(f"/api/clientes/{cliente.pk}/")
        self.assertIn(response.status_code, (401, 403))
        self.assertTrue(Cliente.objects.filter(pk=cliente.pk).exists())

    def test_dados_de_funcionarios_so_para_administrador(self):
        self.client.force_login(self.func.usuario)
        self.assertEqual(self.client.get("/api/funcionarios/").status_code, 403)
        self.assertEqual(self.client.get("/api/clientes/").status_code, 200)

        self.client.force_login(self.adm.usuario)
        self.assertEqual(self.client.get("/api/funcionarios/").status_code, 200)
