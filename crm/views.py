from django.views.generic import ListView
from .models import *


class OrderView(ListView):
    model = Order
    template_name = 'crm/order.html'
