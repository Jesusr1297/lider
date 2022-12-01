from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import generic

from .forms import MaterialXMLForm
from orders.models import Material
from .utils import xml_to_model


def budget(request):
    return render(request, 'budgets/budget.html')


class MaterialsView(generic.ListView):
    model = Material
    template_name = 'budgets/materials.html'
    paginate_by = 5


class MaterialsCreateView(SuccessMessageMixin, generic.CreateView):
    model = Material
    template_name = 'budgets/material_form.html'
    success_message = 'Se ha agregado un nuevo material'
    fields = '__all__'
    success_url = reverse_lazy('material-list')


class MaterialUploadXMLView(generic.TemplateView):
    """ View that handles xml upload and updates material model"""
    form_class = MaterialXMLForm
    template_name = 'materials/materialXML_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request, *args, **kwargs):
        # specify arguments that will input in function
        model = Material
        xml = self.request.FILES['xml']

        # pass arguments to function, extracts all products from xml file
        # updates the model with the information obtained
        xml_to_model(xml, model)

        # pass success message and return to list view
        messages.success(self.request, 'material agregado con éxito')
        return redirect('material-list')


class MaterialsDetailView(generic.DetailView):
    model = Material
    template_name = 'budgets/material_detail.html'


class MaterialsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Material
    template_name = 'budgets/material_confirm_delete.html'

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado el material: {self.object.name}')
        return reverse_lazy('material-list')


class MaterialUpdateView(generic.UpdateView):
    model = Material
    fields = '__all__'
    template_name = 'budgets/material_update.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado el material')
        return reverse_lazy('material-list')
