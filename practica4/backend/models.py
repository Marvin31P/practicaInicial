# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carnet = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
