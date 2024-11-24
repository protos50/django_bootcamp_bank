from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Transaction

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'})
        }

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01'
            })
        }

class TransferForm(forms.ModelForm):
    to_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Seleccionar usuario",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = ['to_user', 'amount', 'reason', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01'
            }),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional'
            })
        }

    def __init__(self, *args, from_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if from_user:
            # Excluir al usuario actual y mostrar primero los favoritos
            self.fields['to_user'].queryset = User.objects.exclude(id=from_user.id)
            self.fields['to_user'].queryset = (
                User.objects.filter(favorited_by=from_user).exclude(id=from_user.id) |
                User.objects.exclude(favorited_by=from_user).exclude(id=from_user.id)
            )
