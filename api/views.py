from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status

from .serializers import (
    LoginSerializer,
    UserSerializer,
    ClienteSerializer,
    ContaSerializer,
    MovimentacaoSerializer,
    DepositoSerializer,
    SaqueSerializer,
    PixSerializer,
)
from core.models import Cliente, Conta, Movimentacao

@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """
    Verifica se a API está disponível.
    """

    return Response({
        "status": "online",
        "message": "API SimulaBank disponível."
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def version(request):
    """
    Retorna informações da versão da API.
    """

    return Response({
        "application": "SimulaBank",
        "api_version": "1.0.0",
        "django": "4.2",
        "status": "running"
    })



@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Realiza a autenticação do usuário.
    """

    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():

        return Response(
            serializer.errors,
            status=400
        )

    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:

        return Response(
            {
                "success": False,
                "message": "Usuário ou senha inválidos."
            },
            status=401
        )

    return Response({

        "success": True,

        "message": "Login realizado com sucesso.",

        "user": {

            "id": user.id,

            "username": user.username,

            "first_name": user.first_name,

            "email": user.email

        }

    })    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """
    Retorna os dados do usuário autenticado.
    """

    serializer = UserSerializer(request.user)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cliente(request):
    """
    Retorna os dados do cliente autenticado.
    """

    cliente = Cliente.objects.get(usuario=request.user)

    serializer = ClienteSerializer(cliente)

    return Response(serializer.data) 



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conta(request):
    """
    Retorna os dados da conta do cliente autenticado.
    """

    cliente = Cliente.objects.get(usuario=request.user)

    conta = Conta.objects.get(cliente=cliente)

    serializer = ContaSerializer(conta)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def extrato(request):
    """
    Retorna o extrato da conta do cliente autenticado.
    """

    cliente = Cliente.objects.get(usuario=request.user)

    conta = Conta.objects.get(cliente=cliente)

    movimentacoes = Movimentacao.objects.filter(
        conta=conta
    ).order_by("-data")

    serializer = MovimentacaoSerializer(
        movimentacoes,
        many=True
    )

    return Response(serializer.data)  


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deposito(request):
    """
    Realiza um depósito na conta do cliente autenticado.
    """

    serializer = DepositoSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    cliente = Cliente.objects.get(usuario=request.user)

    conta = Conta.objects.get(cliente=cliente)

    valor = serializer.validated_data["valor"]
    descricao = serializer.validated_data.get("descricao", "")

    with transaction.atomic():

        conta.saldo += valor
        conta.save()

        Movimentacao.objects.create(
            conta=conta,
            tipo="DEPOSITO",
            valor=valor,
            descricao=descricao
        )

    return Response(
        {
            "success": True,
            "message": "Depósito realizado com sucesso.",
            "saldo_atual": conta.saldo
        },
        status=status.HTTP_200_OK
    )      


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def saque(request):
    """
    Realiza um saque na conta do cliente autenticado.
    """

    serializer = SaqueSerializer(data=request.data)

    if not serializer.is_valid():

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    cliente = Cliente.objects.get(usuario=request.user)

    conta = Conta.objects.get(cliente=cliente)

    valor = serializer.validated_data["valor"]

    descricao = serializer.validated_data.get(
        "descricao",
        ""
    )

    if conta.saldo < valor:

        return Response(
            {
                "success": False,
                "message": "Saldo insuficiente."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():

        conta.saldo -= valor

        conta.save()

        Movimentacao.objects.create(

            conta=conta,

            tipo="SAQUE",

            valor=valor,

            descricao=descricao

        )

    return Response(

        {

            "success": True,

            "message": "Saque realizado com sucesso.",

            "saldo_atual": conta.saldo

        },

        status=status.HTTP_200_OK

    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pix(request):
    """
    Realiza uma transferência PIX.
    """

    serializer = PixSerializer(data=request.data)

    if not serializer.is_valid():

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    cliente_origem = Cliente.objects.get(usuario=request.user)

    conta_origem = Conta.objects.get(cliente=cliente_origem)

    cpf_destino = serializer.validated_data["cpf"]

    valor = serializer.validated_data["valor"]

    descricao = serializer.validated_data.get(
        "descricao",
        ""
    )

    try:

        cliente_destino = Cliente.objects.get(
            cpf=cpf_destino
        )

    except Cliente.DoesNotExist:

        return Response(
            {
                "success": False,
                "message": "Cliente destinatário não encontrado."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if cliente_destino == cliente_origem:

        return Response(
            {
                "success": False,
                "message": "Não é permitido realizar PIX para a própria conta."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    conta_destino = Conta.objects.get(
        cliente=cliente_destino
    )

    if conta_origem.saldo < valor:

        return Response(
            {
                "success": False,
                "message": "Saldo insuficiente."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():

        conta_origem.saldo -= valor

        conta_destino.saldo += valor

        conta_origem.save()

        conta_destino.save()

        Movimentacao.objects.create(
            conta=conta_origem,
            tipo="PIX",
            valor=valor,
            descricao=f"PIX enviado para {cliente_destino.usuario.first_name}. {descricao}"
        )

        Movimentacao.objects.create(
            conta=conta_destino,
            tipo="PIX",
            valor=valor,
            descricao=f"PIX recebido de {cliente_origem.usuario.first_name}. {descricao}"
        )

    return Response(
        {
            "success": True,
            "message": "PIX realizado com sucesso.",
            "saldo_atual": conta_origem.saldo
        },
        status=status.HTTP_200_OK
    )    