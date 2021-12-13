from django.shortcuts import render, redirect,get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q 
from .models import *
from .forms import *
from .utils import*
import datetime
import json


def prueba (request):
     return render(request,'paginas/prueba.html')

#Principal
def tienda(request):
     data = cartData(request)
     Numero_carrito = data['Numero_carrito']

     p = Product.objects.all()
     iman=Imagenes.objects.all()

     page =request.GET.get('page',1)
     try:
          paginator =Paginator(p,30)
          p =paginator.page(page)
     except:
          raise Http404
     
     data ={
     'entity':p,'ima':iman,'paginator':paginator,'Numero_carrito':Numero_carrito
     }

     buscar = request.GET.get("buscar")
     if buscar:
          p=Product.objects.filter(
               Q(name__icontains = buscar)|
               Q(marca__nombre__icontains = buscar)|
               Q(categoria__nombre__icontains = buscar)
               ).distinct()
          data ={
          'entity':p,'ima':iman
          }
          return render(request, 'paginas/buscar.html',data)
     return render(request, 'paginas/Quilitienda.html',data)
#------------------------------------------------------------

#Carrito
def carrito(request):
     iman=Imagenes.objects.all()
     p = Product.objects.all()

     data = cartData(request)
     Numero_carrito = data['Numero_carrito']
     items = data['items']
     order = data['order']

     context = {'items':items,'ima':iman, 'order':order,'Numero_carrito':Numero_carrito}
     buscar = request.GET.get("buscar")
     if buscar:
          p=Product.objects.filter(
               Q(name__icontains = buscar)|
               Q(marca__nombre__icontains = buscar)|
               Q(categoria__nombre__icontains = buscar)
               ).distinct()
          data ={
          'entity':p,'ima':iman
          }
          return render(request, 'paginas/buscar.html',data)
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
          if orderitem.quantity == 1:
               messages.success(request, 'Articulo añadido al carrito ')
     elif action == 'remover':
          orderitem.quantity = (orderitem.quantity -1)

     orderitem.save()

     if orderitem.quantity <=0:
          orderitem.delete()
          messages.success(request, 'Articulo eliminado del carrito')
     return JsonResponse('Agregado al carrito',safe=False)
#------------------------------------------------------------


#Pago
def pago(request):
     iman=Imagenes.objects.all()
     data = cartData(request)
     Numero_carrito = data['Numero_carrito']
     items = data['items']
     order = data['order']

     if request.user.is_authenticated:
          usuario= request.user.customer
          if usuario.apellido == None and usuario.nombre == None and usuario.documento == None:
               x=1
               context = {'items':items,'ima':iman, 'order':order, 'Numero_carrito':Numero_carrito,'x':x, 'usuario':Sin_perfil(instance=usuario)}
          else:
               x=0
               context = {'items':items,'ima':iman, 'order':order, 'Numero_carrito':Numero_carrito,'x':x, 'usuario':Perfil_total(instance=usuario)}
     buscar = request.GET.get("buscar")
     if buscar:
          p=Product.objects.filter(
               Q(name__icontains = buscar)|
               Q(marca__nombre__icontains = buscar)|
               Q(categoria__nombre__icontains = buscar)
               ).distinct()
          data ={
          'entity':p,'ima':iman
          }
          return render(request, 'paginas/buscar.html',data)
     return render(request, 'paginas/Pago.html', context)

def procesar_pedido(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     depa=get_object_or_404(Departamento,id=data['shipping']['departamento'])
     muni=get_object_or_404(Municipio,id=data['shipping']['municipio'])
     di=data['form']['documento']
     document=int(di)
     if request.user.is_authenticated:
          customer=request.user.customer
          order, created=Order.objects.get_or_create(customer=customer,complete=False)   
          total = data['form']['total']
          x =data['x']
          order.transaction_id = transaction_id
          if total == order.total_pago:
               order.complete = True
          order.save()

          if order.shipping == True:
               perfil=customer.id
               ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    direccion=data['shipping']['direccion'],
                    municipio=muni,
                    departamento=depa,
                    )
          if x == '1':
               completar_perfil =Customer.objects.get(id=perfil)
               completar_perfil.nombre=data['form']['nombre']
               completar_perfil.apellido=data['form']['apellido']
               completar_perfil.documento=document
               completar_perfil.celular=data['form']['celular']
               completar_perfil.direccion=data['shipping']['direccion']
               completar_perfil.municipio=muni
               completar_perfil.departamento=depa
               completar_perfil.save()
                    

     return JsonResponse('Pago completado',safe=False)
#------------------------------------------------------------

#Registro y Cierre de sesion
def salir(request):
     logout(request)
     messages.success(request, 'Sesion cerrada')
     return redirect('/Quilitienda/')

def register(request):
     data = cookiecart(request)
     items = data['items']
     Cart = data['cart']

     formu = CreateUserForm()
     if request.method == 'POST':
          formu = CreateUserForm(request.POST)
          if formu.is_valid():
               formu.save()

               usuario_creado = User.objects.last()
               costumer_nuevo = Customer()
               costumer_nuevo.user = usuario_creado
               costumer_nuevo.name = usuario_creado.username
               costumer_nuevo.email = usuario_creado.email
               costumer_nuevo.save()

               user = formu.cleaned_data.get('username')
               email = formu.cleaned_data.get('email')
               password_login =formu.cleaned_data.get('password1')
               usuario = authenticate(username=user,password=password_login)
               login(request, usuario)
               if Cart == {}:
                    messages.success(request, 'Cuenta creada ' + user)
                    return redirect(to='/Quilitienda/')
               else:
                    order = Order.objects.create(
                         customer=costumer_nuevo,
                         complete=False,

                         )
                    for item in items:
                         product =Product.objects.get(id=item['product']['id'])
                         orderitem =OrderItem.objects.create(
                              product=product,
                              order=order,
                              quantity=item['quantity'],
                              )
                    messages.success(request, 'Cuenta creada ' + user)
                    return redirect(to='/Pago/')  
     else:
            formu = CreateUserForm()
     context = {'formu':formu}
     return render(request, 'registration/register.html', context)
#------------------------------------------------------------

#Detalles de prodcuto
def ver_producto(request, id_prod):
     iman=Imagenes.objects.all()
     buscar= request.GET.get("buscar")
     p = Product.objects.get(id=id_prod)
     data = cartData(request)
     Numero_carrito = data['Numero_carrito']

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

     context = {'p':p,'ima':iman, 'Numero_carrito':Numero_carrito}

     return render(request,'paginas/ver_producto.html',context)
#------------------------------------------------------------

#Perfil
def ver_perfil(request,id_perfil):
     usuario =Customer.objects.get(user_id=id_perfil)
     
     data = cartData(request)
     Numero_carrito = data['Numero_carrito']

     buscar = request.GET.get("buscar")
     if buscar:
          p=Product.objects.filter(
               Q(name__icontains = buscar)|
               Q(marca__nombre__icontains = buscar)|
               Q(categoria__nombre__icontains = buscar)
               ).distinct()
          data ={
          'entity':p,'ima':iman
          }
          return render(request, 'paginas/buscar.html',data)
     if usuario.foto == '':
          fot=1
     data ={'usuario':usuario,'fot':fot, 'Numero_carrito':Numero_carrito}
     return render(request,'paginas/perfil.html', data)

def modificar_perfil(request,id_perfil):
     usuario=get_object_or_404(Customer, user_id=id_perfil)
     data={
     'form':RegistrarForm(instance=usuario)
     }
     perfil=id_perfil
     if request.method == 'POST':
          modificar=RegistrarForm(data=request.POST, instance=usuario)
          if modificar.is_valid():
               modificar.save()
               messages.success(request, 'Datos actualizados ')
               return ver_perfil(request, perfil)
          data["forms"]=modificar

     return render(request,'paginas/modificar_perfil.html',data)
#--------------------------------------------------------------

#Select Anidado
def cargar_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    municipios = Municipio.objects.filter(departamento_id=departamento_id)
    print(departamento_id)
    return JsonResponse(list(municipios.values('id', 'name')), safe=False)

#------------------------------------------------------------