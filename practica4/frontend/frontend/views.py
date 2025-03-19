from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
import requests

# URL del backend Flask
BACKEND_URL = "http://127.0.0.1:5000"

# Vista para la página principal (home)
def home(request):
    return render(request, 'home.html')  # Asegúrate de tener este archivo 'home.html'

# Vista para la página de login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Si el usuario ya está autenticado, lo redirigimos a la página principal
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {username}!')
                return redirect('home')  # Redirigimos al home después de un login exitoso
            else:
                messages.error(request, 'Error en el login. Verifica tus credenciales.')
        else:
            messages.error(request, 'Formulario inválido')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Vista para registrar nuevos usuarios
def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        nombre = request.POST['nombre']
        carnet = request.POST['carnet']

        # Verificar si las contraseñas coinciden
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')  # Redirigimos al formulario si hay error

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está registrado.')
            return redirect('registro')

        # Crear un nuevo usuario
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = nombre  # Guardamos el nombre
        user.save()

        messages.success(request, f'Cuenta creada para {username}!')
        return redirect('login')  # Redirigimos al login después de registrar al usuario

    return render(request, 'accounts/registro.html')

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('login')  # Redirigimos al login después de cerrar sesión

@login_required
def perfil(request):
    user = request.user  # Obtiene el usuario actualmente autenticado
    return render(request, 'accounts/profile.html', {'user': user})  # Pasa el objeto usuario al template

@login_required
def crear_publicacion(request):
    """Vista para crear una nueva publicación"""
    if request.method == 'POST':
        titulo = request.POST['titulo']
        contenido = request.POST['contenido']

        # Enviar los datos al backend Flask
        response = requests.post(
            f"{BACKEND_URL}/publicacion",
            json={"titulo": titulo, "contenido": contenido},
            cookies=request.COOKIES  # Pasa las cookies para autenticación en Flask
        )

        if response.status_code == 201:
            messages.success(request, "Publicación creada exitosamente")
        else:
            messages.error(request, "Error al crear la publicación")

        return redirect('listar_publicaciones')

    return render(request, 'accounts/crear_publicacion.html')

def listar_publicaciones(request):
    """Vista para obtener y mostrar todas las publicaciones"""
    response = requests.get(f"{BACKEND_URL}/publicaciones")

    if response.status_code == 200:
        publicaciones = response.json()
    else:
        publicaciones = []

    return render(request, 'accounts/listar_publicaciones.html', {'publicaciones': publicaciones})
