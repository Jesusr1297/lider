from django.shortcuts import render
from orders.models import Materials
from django.views.generic import ListView

# class BudgetView(ListView):
#     model =
#     template_name = 'orders/budget.html'


def budget(request):
    return render(request, 'budgets/budget.html')


class MaterialsView(ListView):
    model = Materials
    template_name = 'budgets/material_detail.html'
