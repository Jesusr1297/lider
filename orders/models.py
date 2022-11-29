import datetime

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

    @property
    def lider_list(self):
        return Lider.objects.filter(customer=self.id)


class Lider(models.Model):
    lider_id = models.CharField('Numero de Lider', max_length=4,
                                validators=[RegexValidator(r'^\d{1,10}$')], primary_key=True)
    doc_description = models.CharField(verbose_name='Descripcion del formato',
                                       max_length=250, default='NOTA DE VENTA')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default='')
    doc_inks = models.CharField(max_length=14, choices=[('negra', 'NEGRA'),
                                                        ('reflex', 'AZUL REFLEX'),
                                                        ('rojo032', 'ROJO 032CV'),
                                                        ('naranjaDirecto', 'NARANJA DIRECTO')
                                                        ],
                                default='reflex')

    def __str__(self):
        return f'{self.lider_id} - {self.doc_description.lower()}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateField('Fecha ordenada', auto_now=True)
    expected_delivery_date = models.DateField('Fecha esperada de Entrega', auto_now=True)
    completed = models.BooleanField(verbose_name='Terminado', default=False)
    delivered = models.BooleanField(verbose_name='entregado', default=False)
    paid = models.BooleanField(verbose_name='pagado', default=False)

    def __str__(self):
        return f'{self.id:03d} - {self.customer}'


class Materials(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Nombre del Material', null=True)
    quantity_ordered = models.FloatField(verbose_name='Cantidad', default=0)
    unit_code = models.CharField(max_length=5, verbose_name='Codigo Unidad', default='')
    unit_price = models.FloatField(verbose_name='Precio', default=0)
    vat = models.CharField(max_length=4, choices=[('1.16', '16%'),
                                                  ('1.08', '8%'),
                                                  ('1', 'N/A')],
                           default=1.08, verbose_name='Precio con IVA')

    @property
    def get_vat_price(self):
        return float(self.vat) * self.unit_price

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    lider = models.ForeignKey(Lider, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    quantity_ordered = models.IntegerField()
    finished = models.BooleanField()

    @property
    def status(self):
        return 'Terminado' if self.finished else 'Pendiente'

    def __str__(self):
        return f'{self.order} - {self.lider}'


class Quotation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    material = models.ForeignKey(Materials, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id
