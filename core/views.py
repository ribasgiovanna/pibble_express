from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db import transaction

from clientes.forms import ClienteForm
from clientes.models import Cliente
from entregas.forms import EntregaForm
from entregas.models import Entrega
from funcionarios.forms import FuncionarioForm
from funcionarios.models import Funcionario
from produtos.forms import ProdutoForm
from produtos.models import Produto


def salvar_formulario_com_feedback(form):
    try:
        with transaction.atomic():
            form.save()
    except Exception:
        form.add_error(
            None,
            "Algo deu errado ao salvar. Confira os dados e tente novamente.",
        )
        return False
    return True


def atualizar_status_entregas():
    hoje = timezone.localdate()
    Entrega.objects.filter(
        status_entrega="CADASTRADO",
        data_envio__lte=hoje,
    ).update(status_entrega="EM_TRANSITO")


def dados_formulario(request):
    return request.POST if request.method == "POST" else None


def dashboard(request):
    atualizar_status_entregas()
    ultimas_entregas = Entrega.objects.select_related("cliente", "produto").order_by("-id")[:10]

    context = {
        "total_clientes": Cliente.objects.count(),
        "total_produtos": Produto.objects.count(),
        "entregas_ativas": Entrega.objects.exclude(status_entrega="ENTREGUE").count(),
        "entregas_concluidas": Entrega.objects.filter(status_entrega="ENTREGUE").count(),
        "ultimas_entregas": ultimas_entregas,
    }
    return render(request, "dashboard.html", context)


def clientes(request):
    form = ClienteForm(dados_formulario(request))

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("clientes")

    context = {
        "form": form,
        "clientes": Cliente.objects.all().order_by("nome_completo"),
    }
    return render(request, "clientes.html", context)


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(dados_formulario(request), instance=cliente)

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("clientes")

    context = {
        "form": form,
        "clientes": Cliente.objects.all().order_by("nome_completo"),
        "editando": cliente,
    }
    return render(request, "clientes.html", context)


def deletar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect("clientes")


def funcionarios(request):
    form = FuncionarioForm(dados_formulario(request))

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("funcionarios")

    context = {
        "form": form,
        "funcionarios": Funcionario.objects.all().order_by("nome_completo"),
    }
    return render(request, "funcionarios.html", context)


def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    form = FuncionarioForm(dados_formulario(request), instance=funcionario)

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("funcionarios")

    context = {
        "form": form,
        "funcionarios": Funcionario.objects.all().order_by("nome_completo"),
        "editando": funcionario,
    }
    return render(request, "funcionarios.html", context)


def deletar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    usuario = funcionario.usuario
    funcionario.delete()
    if usuario:
        usuario.delete()
    return redirect("funcionarios")


def produtos(request):
    form = ProdutoForm(dados_formulario(request))

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("produtos")

    context = {
        "form": form,
        "produtos": Produto.objects.all().order_by("nome_produto"),
    }
    return render(request, "produtos.html", context)


def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(dados_formulario(request), instance=produto)

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("produtos")

    context = {
        "form": form,
        "produtos": Produto.objects.all().order_by("nome_produto"),
        "editando": produto,
    }
    return render(request, "produtos.html", context)


def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.delete()
    return redirect("produtos")


def entregas(request):
    atualizar_status_entregas()
    form = EntregaForm(dados_formulario(request))

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("entregas")

    context = {
        "form": form,
        "entregas": Entrega.objects.select_related(
            "cliente",
            "produto",
            "funcionario_responsavel",
        ).order_by("-id"),
    }
    return render(request, "entregas.html", context)


def editar_entrega(request, pk):
    atualizar_status_entregas()
    entrega = get_object_or_404(Entrega, pk=pk)
    form = EntregaForm(dados_formulario(request), instance=entrega)

    if request.method == "POST" and form.is_valid() and salvar_formulario_com_feedback(form):
        return redirect("entregas")

    context = {
        "form": form,
        "entregas": Entrega.objects.select_related(
            "cliente",
            "produto",
            "funcionario_responsavel",
        ).order_by("-id"),
        "editando": entrega,
    }
    return render(request, "entregas.html", context)


def deletar_entrega(request, pk):
    entrega = get_object_or_404(Entrega, pk=pk)
    entrega.delete()
    return redirect("entregas")

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")
