from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from customer_documents.models import Documento
from django.shortcuts import get_object_or_404
import os


from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)

from .serializers import (
    LoginSerializer,
    UserSerializer,
    ClienteSerializer,
    ContaSerializer,
    MovimentacaoSerializer,
    DepositoSerializer,
    SaqueSerializer,
    PixSerializer,
    DocumentoSerializer,
    DocumentoCreateSerializer,
    DocumentoStatusSerializer,
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


@extend_schema(

    tags=["Operações"],

    summary="Realizar depósito",

    description="""
Realiza um depósito na conta do cliente autenticado.

Regras de negócio:

• É obrigatório estar autenticado.

• O valor deve ser maior que zero.

• O saldo da conta será atualizado.

• Será criada uma movimentação do tipo DEPÓSITO.

""",

    request=DepositoSerializer,

    examples=[

        OpenApiExample(

            name="Depósito válido",

            value={

                "valor": "500.00",

                "descricao": "Depósito em dinheiro"

            },

            request_only=True

        )

    ],

    responses={

        200: OpenApiResponse(
            description="Depósito realizado com sucesso."
        ),

        400: OpenApiResponse(
            description="Dados inválidos."
        ),

        401: OpenApiResponse(
            description="Usuário não autenticado."
        ),

        500: OpenApiResponse(
            description="Erro interno."
        ),

    }

)


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

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def documentos(request):
    """
    Lista ou cadastra documentos do usuário autenticado.
    """

    if request.method == "GET":

        documentos = Documento.objects.filter(
            usuario=request.user
        ).order_by("-data_envio")

        serializer = DocumentoSerializer(
            documentos,
            many=True
        )

        return Response(serializer.data)

    serializer = DocumentoCreateSerializer(
        data=request.data
    )

    if not serializer.is_valid():

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    documento = serializer.save(

        usuario=request.user,

        status="ANALISE"

    )

    return Response(

        {

            "success": True,

            "message": "Documento enviado com sucesso.",

            "id": documento.id,

            "status": documento.status

        },

        status=status.HTTP_201_CREATED

    )

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def documento_detalhe(request, id):
    """
    Consulta, atualiza, altera parcialmente ou exclui
    um documento do usuário autenticado.
    """

    documento = get_object_or_404(
        Documento,
        id=id,
        usuario=request.user
    )

    # ==========================
    # GET
    # Consulta o documento
    # ==========================
    if request.method == "GET":

        serializer = DocumentoSerializer(documento)

        return Response(serializer.data)

    # ==========================
    # PUT
    # Atualiza todos os dados
    # ==========================
    elif request.method == "PUT":

        serializer = DocumentoCreateSerializer(
            documento,
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Documento atualizado com sucesso.",
                "documento": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # ==========================
    # PATCH
    # Atualiza apenas o status
    # ==========================
    elif request.method == "PATCH":

        serializer = DocumentoStatusSerializer(
            documento,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Status do documento atualizado com sucesso.",
                "documento": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # ==========================
    # DELETE
    # Exclui o documento
    # ==========================
    elif request.method == "DELETE":

        if documento.arquivo:
            documento.arquivo.delete(save=False)

        documento.delete()

        return Response(
            {
                "success": True,
                "message": "Documento excluído com sucesso."
            },
            status=status.HTTP_200_OK
        )