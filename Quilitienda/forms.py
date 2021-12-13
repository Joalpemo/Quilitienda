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
        'email',
        'celular',
        'direccion',
        'departamento',
        'nombre',
        'apellido',
        'foto',
        'documento',
        'municipio'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()
        
        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['municipio'].queryset = Municipio.objects.filter(departamento_id=departamento_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        

class Sin_perfil(ModelForm):
    class Meta:
        model = Customer
        fields = [
        'celular',
        'direccion',
        'departamento',
        'nombre',
        'apellido',
        'municipio',
        'documento'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()

        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['municipio'].queryset = Municipio.objects.filter(departamento_id=departamento_id).order_by('name')
            except (ValueError, TypeError):
                pass  


class Perfil_total(ModelForm):
    class Meta:
        model = Customer
        fields = [
        'celular',
        'direccion',
        'departamento',
        'municipio',
        'documento'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()

        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['municipio'].queryset = Municipio.objects.filter(departamento_id=departamento_id).order_by('name')
            except (ValueError, TypeError):
                pass
        
        