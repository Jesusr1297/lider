from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views import generic

from .forms import MaterialXMLForm
from orders.models import Material
from .utils import xml_to_model


class BudgetsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'budgets/budget.html'


def budget(request):
    return render(request, 'budgets/budget.html')


class MaterialsView(LoginRequiredMixin, generic.ListView):
    model = Material
    template_name = 'materials/material_list.html'
    ordering = ('id',)
    paginate_by = 5


class MaterialsCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Material
    template_name = 'materials/material_form.html'
    success_message = 'Se ha agregado un nuevo material'
    fields = '__all__'
    success_url = reverse_lazy('material-list')


class MaterialUploadXMLView(LoginRequiredMixin, generic.FormView):
    """ View that handles xml upload and updates material model"""
    form_class = MaterialXMLForm
    template_name = 'materials/materialXML_form.html'
    model = Material

    def get_success_url(self):
        return reverse('material-list')

    def form_valid(self, form):
        # if form is valid we extract xml file and upload data to model
        xml = form.cleaned_data['xml']
        xml_to_model(xml, self.model, self.request)
        return super(MaterialUploadXMLView, self).form_valid(form)


class MaterialUploadXMLConfirmView(LoginRequiredMixin, generic.FormView):
    # todo
    pass
    # id_list = list_of_ids_from_checkboxes
    # MyModel.objects.filter(id__in=id_list).update(myattribute=True)


class MaterialsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Material
    template_name = 'budgets/templates/materials/material_detail.html'


class MaterialsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Material
    template_name = 'budgets/templates/materials/material_confirm_delete.html'

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado el material: {self.object.name}')
        return reverse_lazy('material-list')


class MaterialUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Material
    fields = '__all__'
    template_name = 'budgets/templates/materials/material_update.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado el material')
        return reverse_lazy('material-list')
