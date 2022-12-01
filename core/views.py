from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from orders import models


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class SignUpView(SuccessMessageMixin, generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_message = 'Usuario creado con éxito'

    def get_success_url(self):
        return reverse_lazy('login')


class SearchView(generic.TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if q != '':
            orders = models.Order.objects.filter(Q(id__contains=q))
            customers = models.Customer.objects.filter(Q(name_company__icontains=q))
            liders = models.Lider.objects.filter(Q(lider_id__icontains=q)
                                                 | Q(doc_description__icontains=q)
                                                 | Q(doc_inks__icontains=q))
            material = models.Material.objects.filter(Q(name__icontains=q))
            context = {'orders': orders, 'customers': customers, 'liders': liders, 'materials': material}
            return render(request, template_name=self.template_name, context=context)
        return render(request, template_name=self.template_name, context={})
