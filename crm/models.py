from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.
class Customer(models.Model):
    name_company = models.CharField(verbose_name='Nombre/Empresa', max_length=50)
    email = models.EmailField(verbose_name='Correo', null=True)
    phone_number = models.CharField(verbose_name='Telefono', max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    address = models.CharField(verbose_name='Domicilio', max_length=100, null=True)
    shipping = models.BooleanField(verbose_name='Entrega a domicilio')

    def __str__(self):
        return self.name_company


class Lider(models.Model):
    lider = models.CharField('Numero de Lider', max_length=4,
                             validators=[RegexValidator(r'^\d{1,10}$')], primary_key=True)

    def __str__(self):
        return self.lider


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lider = models.ForeignKey(Lider, on_delete=models.CASCADE)
    date_ordered = models.DateField('Fecha ordenada', auto_now=True)

    def __str__(self):
        return f'{self.id:03d} {self.lider} {str(self.customer).title()}'
