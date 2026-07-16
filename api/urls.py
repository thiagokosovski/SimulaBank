from django.urls import path

from . import views

from rest_framework_simplejwt.views import (

    TokenObtainPairView,

    TokenRefreshView,

)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [

    path("health/", views.health, name="api_health"),

    path("version/", views.version, name="api_version"),

    path("login/", views.login, name="api_login"),

    path(
        "token/",
        TokenObtainPairView.as_view(),
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
    ),

    path(
    "cliente/",
    views.cliente,
    name="api_cliente",
    ),

    path(
    "conta/",
    views.conta,
    name="api_conta",
    ),

    path(
    "extrato/",
    views.extrato,
    name="api_extrato",
    ),

    path(
    "deposito/",
    views.deposito,
    name="api_deposito",
    ),

    path(
    "saque/",
    views.saque,
    name="api_saque",
    ),

    path(
    "pix/",
    views.pix,
    name="api_pix",
    ),

    path(
    "documentos/",
    views.documentos,
    name="api_documentos",
    ),

    path(
        "documentos/<int:id>/",
        views.documento_detalhe,
        name="api_documento_detalhe",
    ),

    # ===============================
    # DOCUMENTAÇÃO OPENAPI
    # ===============================

    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    path(
        "redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),


  
  


]