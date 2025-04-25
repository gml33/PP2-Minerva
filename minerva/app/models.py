from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from unittest.util import _MAX_LENGTH
from datetime import datetime

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol_choices = (
        ('-','-'),
        ('admin','admin'),
        ('prensa','prensa'),
        ('clasificacion','clasificacion'),
        ('redaccion','redaccion'),
        ('mapas','mapas'),
        ('estadistica','estadistica'),
        ('edicion','edicion'),
        ('publicacion','publicacion'))
    rol = models.CharField(max_length=25, choices=rol_choices, default='-')
    nombre_rol = models.CharField(max_length=25, blank=True)
    comentario = models.TextField(blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.rol}'
    

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    class Meta:
        verbose_name= "Profile"
        verbose_name_plural = "Profiles"


class Periodico(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    logo = models.ImageField(upload_to='logos', max_length=200, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name= "Periodico"
        verbose_name_plural = "Periodicos"

class link(models.Model):
    url = models.URLField(max_length=200)
    periodico = models.ForeignKey(Periodico, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    responsableAcopio = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.aprobado} - {self.url}"
    
    class Meta:
        verbose_name= "Link"
        verbose_name_plural = "Links"
    
class actividad(models.Model):
    usuario = models.OneToOneField(Profile, on_delete=models.CASCADE)
    tipo_choices = (
        ('alta','alta'),
        ('baja','baja'),
        ('modificacion','modificacion'),
        ('consulta','consulta'),
        ('lista','lista'))
    tipo = models.CharField(max_length=20, choices=tipo_choices, default='consulta')
    entidad = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.usuario} - {self.tipo} - {self.entidad}"
    
    class Meta:
        verbose_name= "Actividad"
        verbose_name_plural = "Actividades"
