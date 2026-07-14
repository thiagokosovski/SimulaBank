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

from decimal import Decimal

class DepositoSerializer(serializers.Serializer):

    valor = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    descricao = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True
    )

    def validate_valor(self, value):

        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "O valor do depósito deve ser maior que zero."
            )

        return value              