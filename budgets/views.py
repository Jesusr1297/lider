from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from orders.models import Materials
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from .forms import MaterialXMLForm
from orders.models import Materials
from .utils import xml_to_model


# class BudgetView(ListView):
#     model =
#     template_name = 'orders/budget.html'


def budget(request):
    return render(request, 'budgets/budget.html')


class MaterialsView(ListView):
    model = Materials
    template_name = 'budgets/materials.html'


class MaterialsCreateView(SuccessMessageMixin, CreateView):
    model = Materials
    template_name = 'budgets/material_form.html'
    success_message = 'Se ha agregado un nuevo material'
    fields = '__all__'
    success_url = reverse_lazy('material-list')


class MaterialUploadXMLView(TemplateView):
    form_class = MaterialXMLForm
    template_name = 'materials/materialXML_form.html'
    model = Materials

    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #         return redirect('material-list')
    #     return super().dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        xml = self.request.FILES['xml']
        xml_to_model(xml, self.model)
        messages.success(self.request, 'xml agregado con exito')
        return reverse('material-list')


def material_upload_xml(request):
    model = Materials
    form = MaterialXMLForm
    if request.method == 'POST':
        xml = request.FILES['xml']
        xml_to_model(xml, model)
        return redirect('material-list')
    context = {'form': form}
    return render(request, template_name='materials/materialXML_form.html', context=context)


class MaterialsDetailView(DetailView):
    model = Materials
    template_name = 'budgets/material_detail.html'


class MaterialsDeleteView(LoginRequiredMixin, DeleteView):
    model = Materials
    template_name = 'budgets/material_confirm_delete.html'

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado el material: {self.object.name}')
        return reverse_lazy('material-list')


class MaterialUpdateView(UpdateView):
    model = Materials
    fields = '__all__'
    template_name = 'budgets/material_update.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado el material')
        return reverse_lazy('material-list')
