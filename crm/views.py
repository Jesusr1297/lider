from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class OrderView(ListView):
    model = Order
    template_name = 'crm/order.html'
    ordering = ['-id']


class OrderCreateView(CreateView):
    model = Order
    fields = ['lider', 'customer', 'quantity_ordered']
    success_url = reverse_lazy('home')


class OrderDetailView(DetailView):
    model = Order


class OrderUpdateView(SuccessMessageMixin, UpdateView):

    model = Order
    fields = '__all__'
    success_url = reverse_lazy('home')
    success_message = 'Se ha actualizado la orden'


class OrderDeleteView(DeleteView):
    model = Order
    """
    Se puede usar directamente success_url para regresar al menu principal, 
    pero al nosotros querer agregar un mensaje, sobre escribimos el metodo
    y agregamos el mensaje en get_success_url
    """
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        messages.warning(self.request, f'Se ha eliminado la orden: {self.object.id:03d}')
        return reverse_lazy('home')


class CustomersView(ListView):
    model = Customer
    template_name = 'crm/customers.html'


class LiderView(ListView):
    model = Lider
    template_name = 'crm/lider.html'


# class BudgetView(ListView):
#     model =
#     template_name = 'crm/budget.html'

def budget(request):
    return render(request, 'crm/budget.html')


