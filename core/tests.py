from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LogoutViewTest(TestCase):
    def test_botao_logout_aparece_para_usuario_logado(self):
        user = User.objects.create_user(username="usuario", password="senha123")
        self.client.force_login(user)

        response = self.client.get(reverse("clientes"))

        self.assertContains(response, 'action="%s"' % reverse("logout"))
        self.assertContains(response, "Sair")

    def test_logout_redireciona_para_login(self):
        user = User.objects.create_user(username="usuario", password="senha123")
        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_paginas_internas_exigem_login(self):
        response = self.client.get(reverse("clientes"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('clientes')}")
