from rest_framework import serializers
from django.contrib.auth.models import User

from core.models import Cliente, Conta, Movimentacao


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [

            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "date_joined",

        ]    

class ClienteSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="usuario.username",
        read_only=True
    )

    nome = serializers.CharField(
        source="usuario.first_name",
        read_only=True
    )

    email = serializers.EmailField(
        source="usuario.email",
        read_only=True
    )

    class Meta:

        model = Cliente

        fields = [
            "id",
            "username",
            "nome",
            "email",
            "cpf",
            "telefone",
            "data_nascimento",
        ]  

class ContaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Conta

        fields = [

            "id",

            "agencia",

            "numero",

            "saldo",

            "ativa",

        ]     


class MovimentacaoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Movimentacao

        fields = [

            "id",

            "tipo",

            "valor",

            "descricao",

            "data",

        ]             