from django.shortcuts import render
from django.views.generic import ListView

from orders.models import Lider


class LiderView(ListView):
    model = Lider
    template_name = 'lider/lider.html'
