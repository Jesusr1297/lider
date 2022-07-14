from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import *
from django.shortcuts import render


class OrderView(ListView):
    model = Order
    template_name = 'crm/order.html'


class OrderDetailView(DetailView):
    model = Order


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


