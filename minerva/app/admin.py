from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user','rol','comentario']

class periodicoAdmin(admin.ModelAdmin):
    model=Periodico
    list_display = ['nombre', 'url']
    search_fields = ['nombre']
    list_per_page = 20
    verbose_name_plural = 'Periodicos'

class linkAdmin(admin.ModelAdmin):
    models=link
    list_display = ['responsableAcopio','fecha','url']
    search_fields = ['responsableAcopio','url','fecha']
    list_per_page=20
    verbose_name_plural = 'Links'

class actividadAdmin(admin.ModelAdmin):
    models=actividad
    list_display = ['usuario','tipo','entidad','fecha']
    search_fields = ['usuario','fecha']
    list_per_page=20
    verbose_name_plural = 'Actividades'



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Periodico, periodicoAdmin)
admin.site.register(link, linkAdmin)
admin.site.register(actividad, actividadAdmin)
