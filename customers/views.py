from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from orders.models import *


class CustomersView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/customers.html'
    ordering = ['-id']
    paginate_by = 5


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        customer_id = kwargs['object'].id
        queryset = Lider.objects.filter(customer_id=customer_id).order_by('-lider_id')

        context.update({
            "lider_list": queryset
        })
        return context


class CustomerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Customer
    template_name = 'customers/customer_form.html'
    fields = '__all__'
    success_url = reverse_lazy('customers')
    success_message = 'Se ha creado un nuevo cliente'


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'customers/customer_update.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado cliente correctamente')
        return reverse_lazy('customer-detail', kwargs={'pk': self.get_object().id})


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado al cliente: {self.object.name_company}')
        return reverse_lazy('customers')


class CustomerContactDetailView(LoginRequiredMixin, DetailView):
    model = CustomerContact
    template_name = 'customers/customer_contact_detail.html'


class CustomerContactUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomerContact
    template_name = 'customers/customer_contact_form.html'
    fields = ('name', 'department', 'contact')

    def get_success_url(self):
        pk = self.kwargs['pk']
        messages.info(self.request, 'Se ha actualizado el contacto')
        return reverse_lazy('customer-contact-detail', kwargs={'pk':pk})
