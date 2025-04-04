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
        ('admin','admin'),
        ('editor','editor'),
        ('usuario','usuario'))
    rol = models.CharField(max_length=25, choices=rol_choices, default='usuario')
    comentario = models.TextField(blank=True)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Periodico(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    logo = models.ImageField(upload_to='logos', max_length=200, blank=True)

    def __str__(self):
        return self.nombre