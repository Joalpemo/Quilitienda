from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q 
from .forms import *
from .models import *
import json


def tienda(request):
     if request.user.is_authenticated:
          customer=request.user.customer
          order, created=Order.objects.get_or_create(customer=customer,complete=False)
          items=order.orderitem_set.all()
          Numero_carrito = order.cantidad
     else:
          items=[]
          order= {"total_pago":0, "cantidad":0}
          Numero_carrito = order['cantidad']
     

     buscar= request.GET.get("buscar")
     p = Product.objects.all()
     i=Imagenes.objects.all()
     

     page =request.GET.get('page',1)
     try:
          paginator =Paginator(p,30)
          p =paginator.page(page)
     except:
          raise Http404
     
     if buscar:
          p=Product.objects.filter(
               Q(name__icontains = buscar)|
               Q(marca__nombre__icontains = buscar)|
               Q(categoria__nombre__icontains = buscar)
               ).distinct()
          data ={
          'entity':p,'ima':i,'paginator':paginator,'Numero_carrito':Numero_carrito
          }
          return render(request, 'paginas/buscar.html',data)
          
     data ={
     'entity':p,'ima':i,'paginator':paginator,'Numero_carrito':Numero_carrito
     }
     return render(request, 'paginas/Quilitienda.html',data)


def carrito(request):
     i=Imagenes.objects.all()
     if request.user.is_authenticated:
          customer=request.user.customer
          order, created=Order.objects.get_or_create(customer=customer,complete=False)
          items=order.orderitem_set.all()
     else:
          items=[]
          order= {"total_pago":0, "cantidad":0}

     context = {'items':items,'ima':i, 'order':order}
     return render(request, 'paginas/Carrito_de_compras.html', context)
     

def Agregar_al_carrito(request):
     data = json.loads(request.body)
     productosId = data['productosId']
     action = data['action']

     print('productosId:', productosId)
     print('Action:', action)

     customer = request.user.customer
     product = Product.objects.get(id=productosId)
     order, created=Order.objects.get_or_create(customer=customer,complete=False)
     orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderitem.quantity = (orderitem.quantity +1)
     elif action == 'remover':
          orderitem.quantity = (orderitem.quantity -1)

     orderitem.save()

     if orderitem.quantity <=0:
          orderitem.delete()
     return JsonResponse('Agregado al carrito',safe=False)




def pago(request):
     i=Imagenes.objects.all()
     if request.user.is_authenticated:
          customer=request.user.customer
          order, created=Order.objects.get_or_create(customer=customer,complete=False)
          items=order.orderitem_set.all()
     else:
          items=[]
          order= {"total_pago":0, "cantidad":0}

     context = {'items':items,'ima':i, 'order':order}

     return render(request, 'paginas/Pago.html', context)

def salir(request):
     logout(request)
     messages.success(request, 'Sesion cerrada')
     return redirect('/Quilitienda/')

def register(request):
     formu = CreateUserForm()
     if request.method == 'POST':
          formu = CreateUserForm(request.POST)
          if formu.is_valid():
               formu.save()
               user = formu.cleaned_data.get('username')
               password_login =formu.cleaned_data.get('password1')
               usuario = authenticate(username=user,password=password_login)
               login(request, usuario)
               messages.success(request, 'Cuenta creada ' + user)
               return redirect(to='/Quilitienda/')  
     else:
            formu = CreateUserForm()
     context = {'formu':formu}
     return render(request, 'registration/register.html', context)

def ver_producto(request, id_prod):
     buscar= request.GET.get("buscar")
     p = Product.objects.get(id=id_prod)
     if buscar:
          p=Product.objects.filter(
               Q(name__icontains = buscar)|
               Q(marca__nombre__icontains = buscar)|
               Q(categoria__nombre__icontains = buscar)
               ).distinct()
          data ={
          'entity':p,
          }
          return render(request, 'paginas/buscar.html',data)
     return render(request,'paginas/ver_producto.html',locals())