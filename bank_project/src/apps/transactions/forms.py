from django import forms
from decimal import Decimal
from django.core.validators import MinValueValidator
from .models import Transaction, TransferReason
from django.contrib.auth import get_user_model

User = get_user_model()

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        label='Monto a depositar',
        min_value=0.01,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    description = forms.CharField(
        label='Descripción (opcional)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-lg border-gray-300 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Ej: Depósito de ahorros'
        })
    )

class TransferForm(forms.ModelForm):
    to_username = forms.CharField(
        label='Usuario destino',
        help_text='Ingrese el nombre de usuario del destinatario',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-lg border-gray-300 bg-gray-50 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Ingrese el nombre de usuario',
            'list': 'users-list',
            'autocomplete': 'off'
        })
    )
    
    class Meta:
        model = Transaction
        fields = ['amount', 'reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 bg-gray-50 focus:ring-primary-500 focus:border-primary-500'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'block w-full rounded-lg border-gray-300 bg-gray-50 focus:ring-primary-500 focus:border-primary-500',
                'min': '0.01',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-gray-300 bg-gray-50 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Agrega una descripción opcional para esta transferencia'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.from_user = kwargs.pop('from_user', None)
        super().__init__(*args, **kwargs)
        self.fields['reason'].queryset = TransferReason.objects.filter(is_active=True)
        self.fields['reason'].empty_label = None
    
    def clean_to_username(self):
        to_username = self.cleaned_data['to_username']
        try:
            to_user = User.objects.get(username=to_username)
            if to_user == self.from_user:
                raise forms.ValidationError('No puedes transferir dinero a ti mismo')
            return to_username
        except User.DoesNotExist:
            raise forms.ValidationError('El usuario ingresado no existe')
