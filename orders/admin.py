from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.Lider)
admin.site.register(models.Material)
admin.site.register(models.OrderItem)
admin.site.register(models.Supplier)
