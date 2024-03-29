from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from orders.models import Lider


class LiderView(LoginRequiredMixin, ListView):
    model = Lider
    template_name = 'lider/lider_list.html'
    ordering = ['-lider_id']


class LiderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lider
    template_name = 'lider/lider_form.html'
    success_message = 'Se ha creado un nuevo LIDER'
    success_url = reverse_lazy('lider')
    fields = '__all__'


class LiderDetailView(LoginRequiredMixin, DetailView):
    model = Lider
    template_name = 'lider/lider_detail.html'


class LiderUpdateView(LoginRequiredMixin, UpdateView):
    model = Lider
    template_name = 'lider/lider_update.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado LIDER')
        return reverse_lazy('lider')


class LiderDeleteView(LoginRequiredMixin, DeleteView):
    model = Lider
    template_name = 'lider/lider_confirm_delete.html'
    login_url = 'login'

    def get_success_url(self):
        messages.add_message(self.request, messages.ERROR, f'Se ha eliminado LIDER {self.object.lider_id}')
        return reverse_lazy('lider')
