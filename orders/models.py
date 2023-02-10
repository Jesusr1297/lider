from django.core.validators import RegexValidator
from django.db import models

import datetime


class Customer(models.Model):
    name_company = models.CharField(verbose_name='Nombre/Empresa', max_length=50)
    address = models.CharField(verbose_name='Domicilio', max_length=100, null=True)
    shipping = models.BooleanField(verbose_name='Entrega a domicilio')

    def __str__(self):
        return self.name_company

    @property
    def lider_list(self):
        return Lider.objects.filter(customer=self.id)

    @property
    def delivery(self):
        return 'Entrega a Domicilio' if self.shipping else 'Recoge en Tienda'

    @property
    def contact_list(self):
        return CustomerContact.objects.filter(company_id=self.id)


class CustomerContact(models.Model):
    company = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Nombre de quien ordena', max_length=50)
    department = models.CharField(verbose_name='Departamento', null=True, blank=True, max_length=30)
    contact = models.CharField(verbose_name='Telefono o Correo', max_length=30)

    def __str__(self):
        return self.name


class Lider(models.Model):
    lider_id = models.CharField('Numero de Lider', max_length=4,
                                validators=[RegexValidator(r'^\d{1,10}$')], primary_key=True)
    doc_description = models.CharField(verbose_name='Descripcion del formato',
                                       max_length=250)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default='')

    def __str__(self):
        return f'{self.lider_id} - {self.doc_description.lower()}'

    @property
    def last_ordered(self):
        last_orderitem = Order.objects.filter(orderitem__lider__lider_id=self.lider_id).last()
        return last_orderitem.date_ordered if last_orderitem else "No ordenado"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente')
    # contact = models.ForeignKey(CustomerContact, on_delete=models.CASCADE, verbose_name='Quien Ordena')
    date_ordered = models.DateField('Fecha ordenada', auto_now=True)
    expected_delivery_date = models.DateField('Fecha esperada de Entrega',
                                              default=(datetime.datetime.now() + datetime.timedelta(days=3)))

    delivered = models.DateField(verbose_name='Fecha de Entrega', null=True, blank=True)

    paid = models.DateField(verbose_name='Fecha de Pago', null=True, blank=True)

    invoice = models.IntegerField(verbose_name='Factura Asociada', null=True, blank=True)
    comment = models.TextField(verbose_name='Comentarios', blank=True, null=True)

    def __str__(self):
        return f'{self.id:03d} - {self.customer}'

    @property
    def completed(self):
        order_items = OrderItem.objects.filter(order_id=self.id)
        order_item_count = order_items.count()
        order_item_finished = order_items.filter(finished=True).count()
        return order_item_count == order_item_finished

    @property
    def delivered_str(self):
        return self.delivered if self.delivered else 'No Entregado'

    @property
    def get_subtotal(self):
        items = OrderItem.objects.filter(order_id=self.id)
        items_sum = sum(item.price for item in items)
        return items_sum

    @property
    def get_total(self):
        return self.get_subtotal * 1.08

    @property
    def lider_list(self):
        return Lider.objects.filter(orderitem__order=self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    lider = models.ForeignKey(Lider, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    quantity_ordered = models.IntegerField(verbose_name='Cantidad')
    finished = models.BooleanField('Terminado')
    unit_price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=4,
                                     verbose_name='Precio Unitario')
    comment = models.TextField(null=True, blank=True)

    @property
    def status(self):
        return 'Terminado' if self.finished else 'Pendiente'

    @property
    def price(self):
        return int(self.quantity_ordered) * float(self.unit_price) if self.unit_price else 0

    def __str__(self):
        return f'{self.order} - {self.lider} - {self.id}'


class Supplier(models.Model):
    id = models.CharField(max_length=13, primary_key=True, verbose_name='RFC')
    name = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Budget(models.Model):
    pass


class Material(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Nombre del Material', null=True)

    supplier_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

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


class Quotation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id
