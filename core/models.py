from django.db import models
from django.contrib.auth.models import User


# ===============================
# CLIENTE
# ===============================
class Cliente(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    cpf = models.CharField(max_length=11, unique=True)

    telefone = models.CharField(max_length=20)

    data_nascimento = models.DateField()

    def __str__(self):
        return self.usuario.username


# ===============================
# CONTA
# ===============================
class Conta(models.Model):

    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    numero = models.CharField(max_length=10, unique=True)

    agencia = models.CharField(max_length=5, default="0001")

    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.agencia} / {self.numero}"


# ===============================
# MOVIMENTAÇÃO (EXTRATO ÚNICO)
# ===============================
class Movimentacao(models.Model):

    TIPOS = [
        ("DEPOSITO", "Depósito"),
        ("SAQUE", "Saque"),
        ("PIX", "PIX"),
        ("TRANSFERENCIA", "Transferência"),
    ]

    conta = models.ForeignKey(
        Conta,
        on_delete=models.CASCADE,
        related_name="movimentacoes"
    )

    tipo = models.CharField(max_length=20, choices=TIPOS)

    valor = models.DecimalField(max_digits=12, decimal_places=2)

    descricao = models.CharField(max_length=200, blank=True)

    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - R$ {self.valor}"