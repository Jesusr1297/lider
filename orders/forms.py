from django import forms
from .models import Order, OrderItem, Customer, Lider

date_widget = {
    'field': forms.DateInput(format=('%m/%d/%Y'),
                             attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                    'type': 'date'}),
}


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'expected_delivery_date']
        widgets = {
            'expected_delivery_date': date_widget['field']
        }


class OrderUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['completed', 'delivered', 'date_delivered', 'paid', 'date_paid']


class OrderItemCreateModelForm(forms.ModelForm):
    lider = forms.ModelChoiceField(queryset=OrderItem.objects.none())

    def __init__(self, *args, **kwargs):
        # We need to override the __init__ method in order to change choices
        # the user can have in the form

        # removing pk from kwargs and assign to variable
        # pk is key to query lider_list for specific customer
        # pk is the order unique id value
        pk = kwargs.pop('pk')

        # with the order id we can query Order model to obtain customer related
        # to that order and ask for id
        customer_id = Order.objects.get(id=pk).customer_id

        # with customer id we can query Customer model to obtain the list of
        # lider related to that customer, this method was previously defined
        # in Customer model (lider_list)
        lider_list = Customer.objects.get(id=customer_id).lider_list

        # instantiate this form and call __init__ method
        super(OrderItemCreateModelForm, self).__init__(*args, **kwargs)

        # override lider field in form passing from null to the list we query
        self.fields['lider'].queryset = lider_list

    class Meta:
        model = OrderItem
        fields = ('lider', 'quantity_ordered', 'unit_price', 'finished')


class OrderItemUpdateModelForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity_ordered', 'finished')
