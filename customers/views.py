from django.shortcuts import render
from django.views.generic import ListView

from orders.models import *


class CustomersView(ListView):
    model = Customer
    template_name = 'customers/customers.html'
