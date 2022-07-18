from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from django.shortcuts import render
from django.urls import reverse


class OrderView(ListView):
    model = Order
    template_name = 'crm/order.html'
    ordering = ['-id']


class OrderCreateView(CreateView):
    model = Order
    fields = ['lider', 'customer', 'quantity_ordered']

    def get_success_url(self):
        return reverse('home')


class OrderDetailView(DetailView):
    model = Order


class OrderUpdateView(UpdateView):
    model = Order
    fields = '__all__'

    def get_success_url(self):
        return reverse('home')


class OrderDeleteView(DeleteView):
    model = Order

    def get_success_url(self):
        return reverse('home')


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


