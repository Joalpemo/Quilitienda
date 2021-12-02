import json
from .models import *

def cookiecart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
	print ('Cart',cart)
	items = []
	order = {"total_pago":0, "cantidad":0}
	Numero_carrito = order['cantidad']

	for i in cart:
		try:
		    Numero_carrito += cart[i]['quantity']
		    producto = Product.objects.get(id=i)
		    total = (producto.price * cart[i]['quantity'])

		    order['total_pago'] +=total
		    order['cantidad'] +=cart[i]['quantity']

		    item = {
		    'product':{
		         'id':producto.id,
		         'name':producto.name,
		         'price':producto.price,
		         },
		    'quantity': cart[i]['quantity'],
		    'total_producto':total
		    }
		    items.append(item)
		except:
		    pass
	return{'Numero_carrito': Numero_carrito, 'items':items, 'order':order,'cart':cart}


def cartData(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order, created=Order.objects.get_or_create(customer=customer,complete=False)   
		items=order.orderitem_set.all()
		Numero_carrito = order.cantidad

	else:
		cookieData = cookiecart(request)
		Numero_carrito = cookieData['Numero_carrito']
		order = cookieData['order']
		items = cookieData['items']

	return{'Numero_carrito': Numero_carrito, 'items':items, 'order':order}