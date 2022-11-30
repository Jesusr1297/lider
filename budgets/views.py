from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from .forms import MaterialXMLForm
from orders.models import Material
from .utils import xml_to_model


# class BudgetView(ListView):
#     model =
#     template_name = 'orders/budget.html'


def budget(request):
    return render(request, 'budgets/budget.html')


class MaterialsView(ListView):
    model = Material
    template_name = 'budgets/materials.html'
    paginate_by = 5


class MaterialsCreateView(SuccessMessageMixin, CreateView):
    model = Material
    template_name = 'budgets/material_form.html'
    success_message = 'Se ha agregado un nuevo material'
    fields = '__all__'
    success_url = reverse_lazy('material-list')


class MaterialUploadXMLView(TemplateView):
    form_class = MaterialXMLForm
    template_name = 'materials/materialXML_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request, *args, **kwargs):
        model = Material
        xml = self.request.FILES['xml']
        xml_to_model(xml, model)
        messages.success(self.request, 'material agregado con éxito')
        return redirect('material-list')


class MaterialsDetailView(DetailView):
    model = Material
    template_name = 'budgets/material_detail.html'


class MaterialsDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = 'budgets/material_confirm_delete.html'

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado el material: {self.object.name}')
        return reverse_lazy('material-list')


class MaterialUpdateView(UpdateView):
    model = Material
    fields = '__all__'
    template_name = 'budgets/material_update.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado el material')
        return reverse_lazy('material-list')
