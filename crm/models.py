from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.
class Customer(models.Model):
    name_company = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    address = models.CharField(max_length=100, null=True)
    shipping = models.BooleanField()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lider = models.CharField('Numero de Lider', max_length=4, validators=[RegexValidator(r'^\d{1,10}$')])
