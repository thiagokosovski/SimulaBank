from django import forms

from .models import Documento



class DocumentoForm(forms.ModelForm):


    confirmar = forms.BooleanField(

        required=True,

        label="Declaro que o documento enviado é verdadeiro"

    )



    class Meta:


        model = Documento


        fields = [

            "tipo",

            "descricao",

            "arquivo",

        ]


        labels = {


            "tipo": "Tipo de Documento",

            "descricao": "Descrição",

            "arquivo": "Arquivo",

        }



        error_messages = {


            "tipo": {

                "required": "Selecione o tipo do documento."

            },


            "descricao": {

                "required": "Informe uma descrição."

            },


            "arquivo": {

                "required": "Selecione um arquivo."

            },


        }




    def clean_arquivo(self):


        arquivo = self.cleaned_data.get("arquivo")



        if not arquivo:

            raise forms.ValidationError(

                "Selecione um arquivo."

            )



        extensoes_permitidas = [

            ".jpg",

            ".jpeg",

            ".png",

            ".pdf"

        ]



        nome = arquivo.name.lower()



        if not any(

            nome.endswith(ext)

            for ext in extensoes_permitidas

        ):


            raise forms.ValidationError(

                "Formato inválido. Envie JPG, JPEG, PNG ou PDF."

            )



        tamanho_maximo = 5 * 1024 * 1024



        if arquivo.size > tamanho_maximo:


            raise forms.ValidationError(

                "Arquivo muito grande. Máximo permitido: 5 MB."

            )



        return arquivo