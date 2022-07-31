from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from orders.models import Lider


class LiderView(ListView):
    model = Lider
    template_name = 'lider/lider.html'


class LiderCreateView(SuccessMessageMixin, CreateView):
    model = Lider
    template_name = 'lider/lider_form.html'
    success_message = 'Se ha creado un nuevo LIDER'
    success_url = reverse_lazy('lider')
    fields = '__all__'


class LiderDetailView(DetailView):
    model = Lider
    template_name = 'lider/lider_detail.html'


