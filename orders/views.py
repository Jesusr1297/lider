from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from . import models
from .forms import OrderModelForm, OrderItemModelForm


class SignUpView(SuccessMessageMixin, generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_message = 'Usuario creado con exito'

    def get_success_url(self):
        return reverse_lazy('login')


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class OrderListView(generic.ListView):
    model = models.Order
    template_name = 'orders/order_list.html'
    ordering = ['id']
    paginate_by = 10


class OrderCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = OrderModelForm
    template_name = 'orders/order_form.html'
    success_message = 'Se ha creado una nueva orden'

    def get_success_url(self, **kwargs):
        return reverse_lazy('orderItem-detail', kwargs={'pk': self.object.pk})


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


class OrderItemListView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        context = {
            'items': models.OrderItem.objects.filter(order_id=kwargs['pk']),
            'order': models.Order.objects.get(id=kwargs['pk'])
        }
        return render(request, template_name='orders/cart.html', context=context)


class OrderItemAddView(generic.CreateView):
    form_class = OrderItemModelForm
    template_name = 'orders/order_form.html'

    # def get_context_data(self, **kwargs):
    #     customer = models.Customer.objects.get(order=self.kwargs['pk'])
    #     return {'customer': customer}

    # def get_queryset(self):
    #     qs = models.OrderItem.objects.filter(lider__in=self.object.lider.lider_list)
    #     return qs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.order_id = self.kwargs['pk']
        instance.save()
        return super(OrderItemAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('orderItem-detail', kwargs={'pk': self.kwargs['pk']})


class OrderItemUpdateView(generic.UpdateView):
    template_name = 'orders/orderItem_update.html'
    model = models.OrderItem
    fields = ('lider', 'quantity_ordered', 'finished')

    def get_success_url(self, **kwargs):
        return reverse_lazy('orderItem-detail', kwargs={'pk': self.kwargs['pk']})


def search_view(request):
    # TODO fix search view
    if request.method == 'GET' and request.GET.get('q') != '':
        q = request.GET.get('q') if request.GET.get('q') is not None else ''
        orders = models.Order.objects.filter(Q(customer__name_company__icontains=q) |
                                             Q(orderitem__lider_id__icontains=q))
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
