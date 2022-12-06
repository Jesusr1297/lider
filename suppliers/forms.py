from django import forms
from orders.models import Supplier

class SupplierModelForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'city')