from django import forms
from .models import Order, OrderItem


class OrderModelForm(forms.ModelForm):
    raw_id_fields = ("lider", )
    class Meta:
        model = Order
        fields = ['customer']


class OrderItemModelForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['lider', 'quantity_ordered', 'finished']
