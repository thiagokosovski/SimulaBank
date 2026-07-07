from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("", views.conta, name="conta"),

    path("deposito/", views.deposito_view, name="deposito"),

    path("saque/", views.saque, name="saque"),

    path("pix/", views.pix_view, name="pix"),

    path("extrato/", views.extrato_view, name="extrato"),

    path("sucesso/", views.sucesso_view, name="sucesso"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("cadastro/", views.cadastro_cliente, name="cadastro_cliente"),

    path('meus-dados/', views.meus_dados, name='meus_dados'),

]