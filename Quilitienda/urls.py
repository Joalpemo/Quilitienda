from django.urls import path

from . import views
from django.conf import settings

app_name = 'forms'	
urlpatterns = [
        #Leave as empty string for base url
	path('Quilitienda/', views.tienda, name="tienda"),
	path('Carrito_de_compras/', views.carrito, name="carrito"),
	path('Pago/', views.pago, name="pago"),
	path('Agregar/',views.Agregar_al_carrito, name='Agregar'),
	path('Salir/',views.salir, name='salir'),
	path('Register/', views.register, name='register'),
	path('ver_producto/<int:id_prod>/',views.ver_producto, name='ver_producto'),
	path('ver_perfil/<int:id_perfil>/',views.ver_perfil, name='ver_perfil'),
	path('modificar_perfil/<int:id_perfil>/',views.modificar_perfil, name='modificar_perfil'),
	path('procesar_pedido/',views.procesar_pedido, name='procesar_pedido'),
	path('ajax/cargar-municipios/', views.cargar_municipios, name='ajax_cargar_municipios'),
]

