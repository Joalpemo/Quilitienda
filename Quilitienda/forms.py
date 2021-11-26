from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User	
from django.forms import ModelForm
from .models import *
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class RegistrarForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
        'user',
        'email',
        'celular',
        'direccion',
        'departamento',
        'nombre',
        'apellido',
        'foto',
        'municipio']
