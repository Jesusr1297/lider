from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from orders.models import Materials
from django.views.generic import ListView, CreateView, DetailView


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
    pass
