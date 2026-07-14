from django.urls import path

from . import views

from rest_framework_simplejwt.views import (

    TokenObtainPairView,

    TokenRefreshView,

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
  


]