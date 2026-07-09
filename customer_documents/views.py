from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Documento
from .forms import DocumentoForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.shortcuts import get_object_or_404



def dashboard_documentos(request):

    documentos = Documento.objects.filter(
        usuario=request.user
    )


    total_documentos = documentos.count()


    em_analise = documentos.filter(
        status="ANALISE"
    ).count()


    aprovados = documentos.filter(
        status="APROVADO"
    ).count()


    rejeitados = documentos.filter(
        status="REJEITADO"
    ).count()


    ultimos_documentos = documentos.order_by(
        "-data_envio"
    )[:5]


    context = {

        "documentos": documentos,

        "total_documentos": total_documentos,

        "em_analise": em_analise,

        "aprovados": aprovados,

        "rejeitados": rejeitados,

        "ultimos_documentos": ultimos_documentos,

    }


    return render(
        request,
        "customer_documents/dashboard.html",
        context
    )



def enviar_documento(request):

    if request.method == "POST":

        form = DocumentoForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            documento = form.save(commit=False)


            documento.usuario = request.user


            documento.save()


            messages.success(
                request,
                "Documento enviado com sucesso."
            )


            return redirect(
                "customer_documents:dashboard_documentos"
            )


    else:

        form = DocumentoForm()


    return render(
        request,
        "customer_documents/upload_documento.html",
        {
            "form": form
        }
    )

    


@login_required
def meus_documentos(request):


    documentos = Documento.objects.filter(

        usuario=request.user

    ).order_by(

        "-data_envio"

    )


    return render(

        request,

        "customer_documents/meus_documentos.html",

        {

            "documentos": documentos

        }

    )

@login_required
def excluir_documento(request, id):


    documento = get_object_or_404(

        Documento,

        id=id,

        usuario=request.user

    )


    if request.method == "POST":


        documento.arquivo.delete()


        documento.delete()



        messages.success(

            request,

            "Documento excluído com sucesso."

        )


    return redirect(

        "customer_documents:meus_documentos"

    )