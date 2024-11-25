from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User
from .forms import UserRegistrationForm, ProfileForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso!')
                return redirect('users:home')
            except Exception as e:
                form.add_error(None, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

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
            return redirect('users:home')
        else:
            context['salio_mal'] = True
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('landing')

def home_view(request):
    if request.user.is_authenticated:
        context = {
            'TITULO': 'Sistema Bancario',
            'todo_los_usuarios': User.objects.exclude(id=request.user.id)
        }
        return render(request, 'users/home.html', context)
    return render(request, 'users/landing.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

@login_required
def toggle_favorite_view(request, user_id):
    user_to_toggle = get_object_or_404(User, id=user_id)
    if user_to_toggle in request.user.favorite_users.all():
        request.user.favorite_users.remove(user_to_toggle)
        messages.success(request, f'{user_to_toggle.get_full_name()} removido de favoritos')
    else:
        request.user.favorite_users.add(user_to_toggle)
        messages.success(request, f'{user_to_toggle.get_full_name()} agregado a favoritos')
    return redirect('users:home')
