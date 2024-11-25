from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from .models import Transaction, TransferReason
from .forms import DepositForm, TransferForm
from apps.users.models import User
from django.db import models

@login_required
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', '')
            
            with transaction.atomic():
                # Obtener la razón por defecto como objeto, no como ID
                default_reason = TransferReason.objects.get(id=TransferReason.get_default_reason())
                
                # Actualizar el balance del usuario
                request.user.balance += amount
                request.user.save()
                
                # Crear la transacción con la instancia del objeto reason
                new_transaction = Transaction.objects.create(
                    from_user=request.user,
                    to_user=request.user,
                    amount=amount,
                    description=description,
                    type='DEPOSIT',
                    reason=default_reason
                )
            
            messages.success(request, f'Has depositado ${amount} exitosamente.')
            return redirect('users:home')
    else:
        form = DepositForm()
    
    return render(request, 'transactions/deposit.html', {'form': form})

@login_required
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(data=request.POST, from_user=request.user)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            to_username = form.cleaned_data['to_username']
            reason = form.cleaned_data['reason']
            description = form.cleaned_data.get('description', '')

            try:
                to_user = User.objects.get(username=to_username)
            except User.DoesNotExist:
                messages.error(request, 'El usuario ingresado no existe.')
                return redirect('transactions:transfer')

            if to_user == request.user:
                messages.error(request, 'No puedes transferir dinero a ti mismo.')
                return redirect('transactions:transfer')

            if not to_user.is_active:
                messages.error(request, 'No puedes transferir dinero a un usuario inactivo.')
                return redirect('transactions:transfer')

            if amount > request.user.balance:
                messages.error(request, 'No tienes suficiente saldo para realizar esta transferencia.')
                return redirect('transactions:transfer')

            with transaction.atomic():
                # Realizar la transferencia
                request.user.balance -= amount
                to_user.balance += amount
                request.user.save()
                to_user.save()

                # Crear el registro de la transacción
                Transaction.objects.create(
                    type='TRANSFER',
                    from_user=request.user,
                    to_user=to_user,
                    amount=amount,
                    reason=reason,
                    description=description
                )

            messages.success(request, f'Transferencia de ${amount} realizada con éxito a {to_user.get_full_name()}')
            return redirect('users:home')
    else:
        form = TransferForm(from_user=request.user)

    # Obtener usuarios favoritos
    favorite_users = User.objects.filter(
        favorited_by=request.user
    ).exclude(
        id=request.user.id
    )

    # Obtener los últimos 5 usuarios únicos a los que se les ha transferido
    recent_transfers = Transaction.objects.filter(
        from_user=request.user,
        type='TRANSFER'
    ).select_related('to_user').order_by('-created_at')

    # Obtener usuarios únicos de las transferencias recientes
    seen_users = set()
    recent_users = []
    for transfer in recent_transfers:
        if transfer.to_user.id not in seen_users and transfer.to_user.id != request.user.id and transfer.to_user.id not in favorite_users.values_list('id', flat=True):
            seen_users.add(transfer.to_user.id)
            recent_users.append(transfer.to_user)
            if len(recent_users) >= 5:
                break

    context = {
        'form': form,
        'favorite_users': favorite_users,
        'recent_users': recent_users,
    }

    return render(request, 'transactions/transfer.html', context)

@login_required
def transfer_receipt_view(request, transfer_id):
    transfer = get_object_or_404(Transaction, id=transfer_id, type='TRANSFER')
    return render(request, 'transactions/transfer_receipt.html', {'transfer': transfer})

@login_required
def transaction_history_view(request):
    transactions = Transaction.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    ).order_by('-created_at')
    return render(request, 'transactions/transaction_history.html', {'transactions': transactions})
