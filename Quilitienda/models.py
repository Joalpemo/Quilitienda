from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Departamento(models.Model):
	name = models.CharField(max_length=100,null =True, blank =True)
	codigo = models.IntegerField(null =True, blank =True)
	def __str__(self):
		return self.name

class Municipio(models.Model):
	departamento = models.ForeignKey(Departamento,on_delete = models.SET_NULL, null =True, blank =True)
	name = models.CharField(max_length=100,null =True, blank =True)
	codigo = models.IntegerField(null =True, blank =True)
	def __str__(self):
		return self.name

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null =True, blank =True)
	nombre = models.CharField(max_length=200, null =True, blank =True)
	apellido = models.CharField(max_length=200, null =True, blank =True)
	email = models.CharField(max_length=200, null =True, blank =True)
	celular = models.IntegerField(null =True, blank =True)
	direccion = models.CharField(max_length=200, null =True, blank =True)
	foto = models.ImageField(upload_to='foto',null =True, blank =True)
	departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
	municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL,null=True,blank=True)
	def __str__(self):
		return self.name



class Categoria(models.Model):
	nombre      = models.CharField(max_length =100)
	def __str__(self):
		return self.nombre

class Marca(models.Model):
	nombre     = models.CharField(max_length =100)
	def __str__(self):
		return self.nombre

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField(null =True, blank =True)
	digital = models.BooleanField(default=False,null=True, blank=True)
	stock       = models.IntegerField(null =True, blank =True)
	descripcion = models.CharField(max_length =500,null =True, blank =True)
	categoria   = models.ManyToManyField(Categoria)
	marca       = models.ForeignKey(Marca,on_delete = models.SET_NULL, null =True, blank =True)
	def __str__(self):
		return self.name

	@property
	def imagenURL(self):
		try:
			url= self.imagen.url
		except:
			url=''
		return url
def Galeria(instance, filename):
	return f"Productos/{instance.Producto.name}/imagenes/{filename}"


class Imagenes(models.Model):
	Imagenes = models.ImageField(upload_to=Galeria)
	Producto = models.ForeignKey(Product,on_delete = models.CASCADE, related_name="Productos",null =True, blank =True)

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def total_pago(self):
		orderitems=self.orderitem_set.all()
		total=sum([item.total_producto for item in orderitems])
		return total

	@property
	def cantidad(self):
		orderitems=self.orderitem_set.all()
		total=sum([item.quantity for item in orderitems])
		return total
	

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def total_producto(self):
		total= self.product.price*self.quantity
		return total
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

