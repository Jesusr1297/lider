from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from . import models


class SignUpView(SuccessMessageMixin, generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_message = 'Usuario creado con exito'

    def get_success_url(self):
        return reverse_lazy('login')


class OrderView(generic.ListView):
    model = models.Order
    template_name = 'orders/order_list.html'
    ordering = ['id']
    paginate_by = 3


class OrderCreateView(SuccessMessageMixin, generic.CreateView):
    model = models.Order
    fields = ['lider_id', 'customer', 'quantity_ordered']
    success_url = reverse_lazy('home')
    success_message = 'Se ha creado una nueva orden'


class OrderDetailView(generic.DetailView):
    model = models.Order
    template_name = 'orders/order_detail.html'


class OrderUpdateView(generic.UpdateView):
    model = models.Order
    fields = '__all__'
    template_name = 'orders/order_update.html'

    """
    Se utiliza la funcion get_success_url en lugar del metodo success_url para poder agregar
    el mensaje de actualizacion en el color que necesitamos, ya que SuccessMessageMixin solo 
    nos permite agregar mensajes de SUCCESS, en esto caso nosotros queremos uno de INFO.
    """

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado la orden')
        return reverse_lazy('order-detail', kwargs={'pk': self.get_object().id})


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Order
    """
    Se puede usar directamente success_url para regresar al menu principal, 
    pero al nosotros querer agregar un mensaje, sobre escribimos el metodo
    y agregamos el mensaje en get_success_url
    """

    # success_url = reverse_lazy('home')

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado la orden: {self.object.id:03d}')
        return reverse_lazy('home')


class CartView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        items = models.OrderItem.objects.filter(order_id=kwargs['pk'])
        return render(request, template_name='orders/cart.html', context={'items': items})


def search_view(request):
    if request.method == 'GET' and request.GET.get('q') != '':
        q = request.GET.get('q') if request.GET.get('q') is not None else ''
        orders = models.Order.objects.filter(Q(customer__name_company__icontains=q) |
                                             Q(lider_id__lider_id__icontains=q))
        customers = models.Customer.objects.filter(Q(name_company__icontains=q))
        lider = models.Lider.objects.filter(Q(lider_id__icontains=q) |
                                            Q(doc_description__icontains=q) |
                                            Q(doc_inks__icontains=q))
        material = models.Materials.objects.filter(Q(name__icontains=q))

        context = {
            'orders': orders.order_by('-id'),
            'customers': customers,
            'lider': lider,
            'materials': material,
        }
    else:
        context = {}

    return render(request, 'search.html', context)
