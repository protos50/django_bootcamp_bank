from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_django


def home_view(request):
    # Simulando datos de ejemplo
    lista_usuarios = [
        {"nombre": "Lucas", "apellido": "Ibañez"},
        {"nombre": "Federico", "apellido": "Aguirre"},
        {"nombre": "Raul", "apellido": "Rolon"},
    ]
    contexto = {
        "todo_los_usuarios": lista_usuarios,
        "usuario_autenticado": "Lucas Ibañez",
        "TITULO": "INICIO"
    }
    return render(request, 'home.html', contexto)


def login_view(request):
    se_autentico = False
    salio_mal = True
    username = ""
    if request.method == "POST":
        username = request.POST.get("username", default=None)
        password = request.POST.get("password", default=None)
        usuario = authenticate(request, username=username, password=password)
        se_autentico = True
        if usuario:
            salio_mal = False
            login_django(request, usuario)
            return redirect("home")

    ctx = {
        "se_autentico": se_autentico,
        "salio_mal": salio_mal,
        "username": username
    }
    return render(request, 'login.html', ctx)
