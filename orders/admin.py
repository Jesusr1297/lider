from django.contrib import admin
from .models import Customer, Order, Lider, Materials

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Lider)
admin.site.register(Materials)
