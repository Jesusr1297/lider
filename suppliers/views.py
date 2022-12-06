from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

# Create your views here.
from orders.models import Supplier
from .forms import SupplierModelForm


class SupplierListView(generic.ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'


class SupplierDetailView(generic.DetailView):
    template_name = 'suppliers/supplier_detail.html'
    model = Supplier
    #
    # def get_queryset(self):
    #     print(self.request, self.kwargs)
    #     return Supplier.objects.get(id=self.kwargs['pk'])



class SupplierCreateView(generic.CreateView):
    form_class = SupplierModelForm
    template_name = 'suppliers/supplier_create_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Se ha agregado un proveedor')
        return reverse('suppliers:supplier-list')
