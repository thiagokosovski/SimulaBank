from django import forms
from django.contrib.auth.models import User
from core.models import Cliente




# ==========================================
# CLIENTE
# ==========================================
class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [
            "cpf",
            "telefone",
            "data_nascimento"
        ]


# ==========================================
# SAQUE
# ==========================================
class SaqueForm(forms.Form):

    valor = forms.DecimalField(

        label="Valor do saque",
        max_digits=12,
        decimal_places=2,
        min_value=0.01,

        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o valor",
            "step": "0.01",
        })
    )

# ==========================================
# DEPÓSITO
# ==========================================
class DepositoForm(forms.Form):

    valor = forms.DecimalField(
        label="Valor do depósito",
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o valor",
            "step": "0.01",
        })
    )    


# ==========================================
# PIX
# ==========================================
class PixForm(forms.Form):

    chave_destino = forms.CharField(
        label="Chave PIX (e-mail ou ID da conta)",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite a chave do destinatário"
        })
    )

    valor = forms.DecimalField(
        label="Valor",
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0.00",
            "step": "0.01"
        })
    )

# ==========================================
# EDITAR CLIENTE
# ==========================================
class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['data_nascimento']

        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }


# ==========================================
# EDITAR USER
# ==========================================
class EditarUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }