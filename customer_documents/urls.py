from django.urls import path
from . import views

app_name = "customer_documents"

urlpatterns = [

    path(
        "",
        views.dashboard_documentos,
        name="dashboard_documentos",
    ),

    path(
        "enviar/",
        views.enviar_documento,
        name="enviar_documento",
    ),

    path(
        "meus/",
        views.meus_documentos,
        name="meus_documentos",
    ),

    path(
    "excluir/<int:id>/",
    views.excluir_documento,
    name="excluir_documento",
    ),

]