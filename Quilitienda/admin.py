from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Departamento)

class ImageInline(admin.TabularInline):
    model = Imagenes

@admin.register(Product)
class ProductoAdmon(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]