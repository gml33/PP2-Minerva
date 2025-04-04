from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user','rol','comentario']


class pacienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "apellido", 'dni']
    search_fields = ["nombre", 'apellido']
    list_filter = ["dni"]
    list_per_page = 50
    verbose_name_plural = 'Pacientes'

class periodicoAdmin(admin.ModelAdmin):
    model=Periodico
    list_display = ['nombre', 'url']
    search_fields = ['nombre']
    list_per_page = 20
    verbose_name_plural = 'Periodicos'



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Periodico, periodicoAdmin)
