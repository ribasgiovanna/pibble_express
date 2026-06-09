from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from clientes.views import ClienteViewSet
from core import views
from entregas.views import EntregaViewSet
from funcionarios.views import FuncionarioViewSet
from produtos.views import ProdutoViewSet


router = routers.DefaultRouter()
router.register(r"clientes", ClienteViewSet)
router.register(r"funcionarios", FuncionarioViewSet)
router.register(r"produtos", ProdutoViewSet)
router.register(r"entregas", EntregaViewSet)

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("clientes/", views.clientes, name="clientes"),
    path("clientes/<int:pk>/editar/", views.editar_cliente, name="editar_cliente"),
    path("clientes/<int:pk>/deletar/", views.deletar_cliente, name="deletar_cliente"),
    path("funcionarios/", views.funcionarios, name="funcionarios"),
    path("funcionarios/<int:pk>/editar/", views.editar_funcionario, name="editar_funcionario"),
    path("funcionarios/<int:pk>/deletar/", views.deletar_funcionario, name="deletar_funcionario"),
    path("produtos/", views.produtos, name="produtos"),
    path("produtos/<int:pk>/editar/", views.editar_produto, name="editar_produto"),
    path("produtos/<int:pk>/deletar/", views.deletar_produto, name="deletar_produto"),
    path("entregas/", views.entregas, name="entregas"),
    path("entregas/<int:pk>/editar/", views.editar_entrega, name="editar_entrega"),
    path("entregas/<int:pk>/deletar/", views.deletar_entrega, name="deletar_entrega"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
