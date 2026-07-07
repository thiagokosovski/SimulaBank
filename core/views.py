from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random

from django.contrib import messages

from core.forms import (
    ClienteForm,
    SaqueForm,
)

from core.models import Cliente, Conta, Movimentacao
from .forms import PixForm
from decimal import Decimal
from .forms import DepositoForm

from .forms import EditarClienteForm

from core.forms import EditarClienteForm, EditarUserForm


# ======================================
# TELA PRINCIPAL DA CONTA
# ======================================
@login_required
def conta(request):

    cliente = Cliente.objects.get(usuario=request.user)
    conta = Conta.objects.get(cliente=cliente)

    movimentacoes = Movimentacao.objects.filter(
        conta=conta
    ).order_by("-data")[:3]

    return render(request, "dashboard.html", {
        "cliente": cliente,
        "conta": conta,
        "saldo": conta.saldo,
        "limite": 1000,
        "ultimo_acesso": request.user.last_login,
        "movimentacoes": movimentacoes,
    })


# ======================================
# CADASTRO CLIENTE
# ======================================
@login_required
def cadastrar_cliente(request):

    if request.method == "POST":

        form = ClienteForm(request.POST)

        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()

            Conta.objects.create(
                cliente=cliente,
                numero=str(random.randint(100000, 999999)),
                agencia="0001"
            )

            return redirect("conta")

    else:
        form = ClienteForm()

    return render(request, "core/cadastrar_cliente.html", {"form": form})


# ======================================
# DEPÓSITO
# ======================================
@login_required
def deposito_view(request):

    cliente = Cliente.objects.get(usuario=request.user)
    conta = Conta.objects.get(cliente=cliente)

    form = DepositoForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            valor = form.cleaned_data["valor"]  # <- já é Decimal

            conta.saldo += valor
            conta.save()

            Movimentacao.objects.create(
                conta=conta,
                tipo="DEPOSITO",
                valor=valor,
                descricao="Depósito realizado"
            )

            return redirect("sucesso")

    return render(request, "core/deposito.html", {
        "conta": conta,
        "form": form
    })
# ======================================
# SAQUE
# ======================================
@login_required
def saque(request):

    cliente = Cliente.objects.get(usuario=request.user)
    conta = Conta.objects.get(cliente=cliente)

    if request.method == "POST":

        form = SaqueForm(request.POST)

        if form.is_valid():

            valor = form.cleaned_data["valor"]

            if valor > conta.saldo:
                form.add_error("valor", "Saldo insuficiente.")
            else:

                conta.saldo -= valor
                conta.save()

                Movimentacao.objects.create(
                    conta=conta,
                    tipo="SAQUE",
                    valor=valor,
                    descricao="Saque realizado"
                )

                return redirect("sucesso")

    else:
        form = SaqueForm()

    return render(request, "core/saque.html", {
        "form": form,
        "conta": conta,
    })


# ======================================
# PIX (DIDÁTICO - SEM TRANSFERÊNCIA REAL)
# ======================================
@login_required
def pix_view(request):

    cliente = Cliente.objects.get(usuario=request.user)
    conta = Conta.objects.get(cliente=cliente)

    form = PixForm()

    if request.method == "POST":

        form = PixForm(request.POST)

        if form.is_valid():

            chave_destino = form.cleaned_data["chave_destino"]
            valor = form.cleaned_data["valor"]

            if conta.saldo < valor:
                form.add_error("valor", "Saldo insuficiente")
                return render(request, "core/pix.html", {
                    "form": form,
                    "conta": conta
                })

            conta.saldo -= valor
            conta.save()

            Movimentacao.objects.create(
                conta=conta,
                tipo="PIX",
                valor=valor,
                descricao=f"PIX enviado para {chave_destino}"
            )

            return redirect("sucesso")

    return render(request, "core/pix.html", {
        "form": form,
        "conta": conta
    })


# ======================================
# EXTRATO
# ======================================
@login_required
def extrato_view(request):

    conta = request.user.cliente.conta

    transacoes = conta.movimentacoes.all().order_by("-data")

    return render(request, "core/extrato.html", {
        "conta": conta,
        "transacoes": transacoes
    })


# ======================================
# SUCESSO
# ======================================
@login_required
def sucesso_view(request):
    return render(request, "core/sucesso.html")

# ======================================
# CADASTRO DE NOVO CLIENTE
# ======================================

def cadastro_cliente(request):

    """
    Esta view apenas exibe a tela de cadastro.

    Nesta aula ainda não salvaremos nenhuma
    informação no banco de dados.

    A gravação será implementada na Aula 9.3.
    """

    return render(
        request,
        "core/cadastro_cliente.html"
    )

# ======================================
# Meus dados
# ======================================

@login_required
def meus_dados(request):
    cliente = Cliente.objects.get_or_create(usuario=request.user)[0]
    user = request.user

    if request.method == 'POST':

        form_user = EditarUserForm(request.POST, instance=user)
        form_cliente = EditarClienteForm(request.POST, instance=cliente)

        if form_user.is_valid() and form_cliente.is_valid():
            form_user.save()
            form_cliente.save()

            messages.success(request, "Dados atualizados com sucesso!")
            return redirect('meus_dados')

    else:
        form_user = EditarUserForm(instance=user)
        form_cliente = EditarClienteForm(instance=cliente)

    return render(request, 'core/meus_dados.html', {
        'form_user': form_user,
        'form_cliente': form_cliente,
        'cliente': cliente
    })