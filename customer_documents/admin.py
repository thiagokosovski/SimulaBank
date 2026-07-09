from django.contrib import admin
from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usuario",
        "tipo",
        "status",
        "data_envio",
    )

    list_filter = (
        "status",
        "tipo",
    )

    search_fields = (
        "usuario__username",
        "descricao",
    )