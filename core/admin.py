from django.contrib import admin

# Importa os modelos do sistema
from .models import Cliente, Conta


# =====================================================
# Administração da tabela Cliente
# =====================================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    # Colunas exibidas na listagem
    list_display = (

        "usuario",

        "cpf",

        "telefone",

    )

    # Campos disponíveis para pesquisa
    search_fields = (

        "usuario__username",

        "cpf",

    )


# =====================================================
# Administração da tabela Conta
# =====================================================
@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):

    # Colunas exibidas na tela do Admin
    list_display = (

        "numero",

        "cliente",

        "agencia",

        "saldo",

        "ativa",

    )

    # Filtro lateral
    list_filter = (

        "ativa",

    )

    # Campo de pesquisa
    search_fields = (

        "numero",

        "cliente__usuario__username",

    )