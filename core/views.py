from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from orders import models


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('auth-home')
        return super().dispatch(request, *args, **kwargs)


class AuthenticatedLandingPage(generic.TemplateView):
    template_name = 'auth_landing.html'
    context_object_name = 'name'

    def get_context_data(self, **kwargs):
        context = super(AuthenticatedLandingPage, self).get_context_data(**kwargs)
        context['num_customers'] = models.Customer.objects.count()
        context['num_pending_orders'] = models.Order.objects.count()
        return context


class SignUpView(SuccessMessageMixin, generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_message = 'Usuario creado con éxito'

    def get_success_url(self):
        return reverse_lazy('login')


class SearchView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if q != '':
            orders = models.Order.objects.filter(Q(id__contains=q))
            customers = models.Customer.objects.filter(Q(name_company__icontains=q))
            liders = models.Lider.objects.filter(Q(lider_id__icontains=q)
                                                 | Q(doc_description__icontains=q)
                                                 )
            material = models.Material.objects.filter(Q(name__icontains=q))
            context = {'orders': orders, 'customers': customers, 'liders': liders, 'materials': material}
            return render(request, template_name=self.template_name, context=context)
        return render(request, template_name=self.template_name, context={})


def handler404(request, exception):
    return render(request, '404.html', status=404)
