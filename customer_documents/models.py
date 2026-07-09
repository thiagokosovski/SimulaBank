from django.db import models
from django.contrib.auth.models import User


class Documento(models.Model):

    STATUS = (
        ("ANALISE", "Em análise"),
        ("APROVADO", "Aprovado"),
        ("REJEITADO", "Rejeitado"),
    )


    TIPOS = (
        ("RG", "RG"),
        ("CPF", "CPF"),
        ("CNH", "CNH"),
        ("RESIDENCIA", "Comprovante de Residência"),
    )


    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    descricao = models.CharField(
        max_length=100
    )


    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )


    arquivo = models.FileField(
        upload_to="documentos/"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="ANALISE"
    )


    observacao = models.TextField(
        blank=True
    )


    data_envio = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return f"{self.usuario.username} - {self.tipo}"