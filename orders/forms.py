from django import forms
from .models import Order, OrderItem, Customer


class OrderModelForm(forms.ModelForm):
    raw_id_fields = ("lider",)

    class Meta:
        model = Order
        fields = ['customer']


class OrderItemCreateModelForm(forms.ModelForm):
    lider = forms.ModelChoiceField(queryset=OrderItem.objects.none())

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        customer_id = Order.objects.get(id=pk).customer_id
        lider_list = Customer.objects.get(id=customer_id).lider_list
        super(OrderItemCreateModelForm, self).__init__(*args, **kwargs)
        self.fields['lider'].queryset = lider_list

    class Meta:
        model = OrderItem
        fields = ('lider', 'quantity_ordered', 'finished')


class OrderItemUpdateModelForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity_ordered', 'finished')
