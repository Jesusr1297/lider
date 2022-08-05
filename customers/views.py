from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from orders.models import *


class CustomersView(ListView):
    model = Customer
    template_name = 'customers/customers.html'
    ordering = ['-id']
    paginate_by = 2


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'


class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    template_name = 'customers/customer_form.html'
    fields = '__all__'
    success_url = reverse_lazy('customers')
    success_message = 'Se ha creado un nuevo cliente'


class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'customers/customer_update.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado cliente correctamente')
        return reverse_lazy('customers')


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado al cliente: {self.object.name_company}')
        return reverse_lazy('customers')
