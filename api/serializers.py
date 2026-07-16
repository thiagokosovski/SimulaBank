from rest_framework import serializers
from django.contrib.auth.models import User

from core.models import Cliente, Conta, Movimentacao
from customer_documents.models import Documento


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


class SaqueSerializer(serializers.Serializer):

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
                "O valor do saque deve ser maior que zero."
            )

        return value 


class PixSerializer(serializers.Serializer):

    cpf = serializers.CharField(
        max_length=11
    )

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
                "O valor do PIX deve ser maior que zero."
            )

        return value  

class DocumentoSerializer(serializers.ModelSerializer):

    arquivo = serializers.FileField(
        use_url=True
    )

    class Meta:

        model = Documento

        fields = [

            "id",

            "tipo",

            "descricao",

            "arquivo",

            "status",

            "observacao",

            "data_envio",

        ] 


class DocumentoCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Documento

        fields = [

            "tipo",

            "descricao",

            "arquivo",

        ]

    def validate_arquivo(self, arquivo):

        extensoes_permitidas = [

            ".pdf",

            ".jpg",

            ".jpeg",

            ".png",

        ]

        nome = arquivo.name.lower()

        if not any(
            nome.endswith(ext)
            for ext in extensoes_permitidas
        ):

            raise serializers.ValidationError(

                "Formato de arquivo não permitido."

            )

        return arquivo  


class DocumentoStatusSerializer(serializers.ModelSerializer):

    class Meta:

        model = Documento

        fields = [

            "status",

        ]           

class DepositoResponseSerializer(serializers.Serializer):

    success = serializers.BooleanField()

    message = serializers.CharField()

    saldo_atual = serializers.DecimalField(

        max_digits=12,

        decimal_places=2

    )                                       