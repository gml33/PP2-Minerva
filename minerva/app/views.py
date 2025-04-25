from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.core.paginator import Paginator
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from .models import *
from django.http  import JsonResponse
from django.core import serializers

def home(request):
    return render(request, 'registro/index.html')

def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:my-login')
    context={'form':form}
    return render(request, 'registro/register.html', context=context)

def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                #bot.send_message(chat_id, text='Logueado')
                return redirect('app:dashboard')
    context = {'form':form}
    return render(request, 'registro/my-login.html', context=context)

@login_required(login_url='app:my-login')
def dashboard(request):
    try:
        profile_usuario = request.user.profile
        rol_usuario = profile_usuario.rol
        print(f"Rol del usuario: {rol_usuario}")
    except Profile.DoesNotExists:
        rol_usuario = None
#----------periodicos-------------------------------------------
    periodicos_all = Periodico.objects.all().order_by('-nombre')
    paginator = Paginator(periodicos_all, 20)
    page_periodicos = request.GET.get('page')
    periodicos = paginator.get_page(page_periodicos)
#-----------Links------------------------------------------
    links_all = link.objects.all().order_by('-fecha')
    paginator = Paginator(links_all, 50)
    page_links = request.GET.get('links')
    links = paginator.get_page(page_links)
#-----------armo el contexto-------------------------
    context = {'periodicos': periodicos,
               'links':links,
               'rol_usuario': rol_usuario}
    return render(request, 'app/dashboard.html', context=context)

def user_logout(request):
    auth.logout(request)
    return redirect('app:my-login')

#----------------------------Periodicos--------------------
@login_required(login_url='my-login')
def agregar_periodico(request):
    data = {
        'form': periodicoForm()
    }
    if request.method == 'POST':
        formulario = periodicoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()            
            return redirect(to="app:dashboard")
        else:
            data["form"] = formulario
    return render(request, 'app/periodico/alta.html', data)

#----------------------links-----------------------------------------

@login_required(login_url='my-login')
def agregar_link(request):
    data = {
        'form': linkForm()
    }
    if request.method == 'POST':
        formulario = linkForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()            
            return redirect(to="app:dashboard")
        else:
            data["form"] = formulario
    return render(request, 'app/link/alta.html', data)