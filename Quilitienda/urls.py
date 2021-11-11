from django.urls import path

from . import views
from django.conf import settings

app_name = 'forms'	
urlpatterns = [
        #Leave as empty string for base url
	path('Quilitienda/', views.tienda, name="tienda"),
	path('Carrito_de_compras/', views.carrito, name="carrito"),
	path('Pago/', views.pago, name="pago"),
	path('Agregar/',views.Agregar_carrito, name='Agregar'),
	path('Salir/',views.salir, name='salir'),
	path('Register/', views.register, name='register'),
	path('ver_producto/<int:id_prod>/',views.ver_producto, name='ver_producto'),
]

