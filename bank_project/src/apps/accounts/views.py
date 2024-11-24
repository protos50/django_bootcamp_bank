from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from .models import User, Transaction, TransferReason
from .forms import UserRegistrationForm, ProfileForm, DepositForm, TransferForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('accounts:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    context = {
        'se_autentico': False,
        'salio_mal': False,
        'username': ''
    }
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        context['username'] = username
        context['se_autentico'] = True
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '¡Bienvenido!')
            return redirect('accounts:home')
        else:
            context['salio_mal'] = True
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('accounts:login')

def home_view(request):
    if request.user.is_authenticated:
        context = {
            'TITULO': 'Sistema Bancario',
            'todo_los_usuarios': User.objects.exclude(id=request.user.id)
        }
        return render(request, 'home.html', context)
    return render(request, 'landing.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            with transaction.atomic():
                # Crear la transacción
                Transaction.objects.create(
                    type='deposit',
                    from_user=request.user,
                    to_user=request.user,
                    amount=amount,
                    description='Depósito de dinero'
                )
                # Actualizar el saldo
                request.user.balance += amount
                request.user.save()
            
            messages.success(request, f'Has depositado ${amount} correctamente')
            return redirect('accounts:home')
    else:
        form = DepositForm()
    
    return render(request, 'deposit.html', {'form': form})

@login_required
def transfer_view(request):
    initial_data = {}
    if 'to' in request.GET:
        try:
            recipient = User.objects.get(username=request.GET['to'])
            if not recipient.is_active:
                messages.warning(request, 'El usuario seleccionado no está activo')
            else:
                initial_data['to_user'] = recipient
        except User.DoesNotExist:
            messages.warning(request, 'Usuario no encontrado')

    if request.method == 'POST':
        form = TransferForm(request.POST, from_user=request.user)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            to_user = form.cleaned_data['to_user']
            
            # Validaciones adicionales
            if amount <= 0:
                form.add_error('amount', 'El monto debe ser mayor que cero')
            elif amount > request.user.balance:
                form.add_error('amount', 'Saldo insuficiente para realizar la transferencia')
            elif not to_user.is_active:
                form.add_error('to_user', 'El usuario seleccionado no está activo')
            else:
                try:
                    with transaction.atomic():
                        # Crear la transacción
                        transfer = form.save(commit=False)
                        transfer.type = 'TRANSFER'
                        transfer.from_user = request.user
                        transfer.save()
                        
                        # Actualizar saldos
                        request.user.balance -= amount
                        request.user.save()
                        
                        to_user.balance += amount
                        to_user.save()
                    
                    messages.success(request, f'Has transferido ${amount:,.2f} a {to_user.get_full_name() or to_user.username}')
                    return redirect('accounts:transfer_receipt', transfer_id=transfer.id)
                except Exception as e:
                    messages.error(request, 'Ocurrió un error al procesar la transferencia. Por favor, intenta nuevamente.')
    else:
        form = TransferForm(from_user=request.user, initial=initial_data)
    
    # Obtener usuarios activos excepto el usuario actual
    available_users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    
    context = {
        'form': form,
        'TITULO': 'Realizar Transferencia',
        'available_users': available_users
    }
    
    return render(request, 'transfer.html', context)

@login_required
def transfer_receipt_view(request, transfer_id):
    transfer = get_object_or_404(
        Transaction,
        Q(from_user=request.user) | Q(to_user=request.user),
        id=transfer_id
    )
    return render(request, 'transfer_receipt.html', {'transfer': transfer})

@login_required
def transaction_history_view(request):
    transactions = Transaction.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    ).order_by('-timestamp')
    return render(request, 'transaction_history.html', {'transactions': transactions})

@login_required
def toggle_favorite_view(request, user_id):
    user_to_toggle = get_object_or_404(User, id=user_id)
    if request.user.favorite_users.filter(id=user_id).exists():
        request.user.favorite_users.remove(user_to_toggle)
        messages.success(request, f'{user_to_toggle.get_full_name()} eliminado de favoritos')
    else:
        request.user.favorite_users.add(user_to_toggle)
        messages.success(request, f'{user_to_toggle.get_full_name()} añadido a favoritos')
    return redirect('accounts:home')
