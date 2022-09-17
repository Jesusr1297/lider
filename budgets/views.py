from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from orders.models import Materials
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


# class BudgetView(ListView):
#     model =
#     template_name = 'orders/budget.html'


def budget(request):
    return render(request, 'budgets/budget.html')


class MaterialsView(ListView):
    model = Materials
    template_name = 'budgets/materials.html'
    paginate_by = 15


class MaterialsCreateView(SuccessMessageMixin, CreateView):
    model = Materials
    template_name = 'budgets/material_form.html'
    success_message = 'Se ha agregado un nuevo material'
    fields = '__all__'
    success_url = reverse_lazy('materials')


class MaterialsDetailView(DetailView):
    model = Materials
    template_name = 'budgets/material_detail.html'


class MaterialsDeleteView(LoginRequiredMixin, DeleteView):
    model = Materials
    template_name = 'budgets/material_confirm_delete.html'

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado el material: {self.object.name}')
        return reverse_lazy('materials')


class MaterialUpdateView(UpdateView):
    model = Materials
    fields = '__all__'
    template_name = 'budgets/material_update.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado el material')
        return reverse_lazy('materials')

