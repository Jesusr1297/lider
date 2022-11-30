from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from . import models
from .forms import OrderModelForm, OrderItemCreateModelForm, OrderItemUpdateModelForm


class OrderListView(generic.ListView):
    model = models.Order
    template_name = 'orders/order_list.html'
    ordering = ['-id']
    paginate_by = 10


class OrderPendingListView(generic.ListView):
    # todo filter between finished and not finished orders
    queryset = models.Order.objects.filter(completed=False)
    template_name = 'orders/order_list.html'
    ordering = ['-id']
    paginate_by = 10


class OrderCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = OrderModelForm
    template_name = 'orders/order_form.html'
    success_message = 'Se ha creado una nueva orden'

    def get_success_url(self, **kwargs):
        return reverse_lazy('orderItem-list', kwargs={'pk': self.object.pk})


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
        return render(request, template_name='orders/orderItem_list.html', context=context)


class OrderItemCreateView(generic.FormView):
    form_class = OrderItemCreateModelForm
    template_name = 'orders/order_form.html'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(OrderItemCreateView, self).get_form_kwargs(**kwargs)
        kwargs.update({'pk': self.kwargs['pk']})
        return kwargs

    def form_valid(self, form):
        print(self.kwargs)
        instance = form.save(commit=False)
        instance.order_id = self.kwargs['pk']
        instance.customer_id = models.Order.objects.get(id=instance.order_id).customer_id
        instance.save()
        return super(OrderItemCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Se ha agregado al pedido')
        return reverse_lazy('orderItem-list', kwargs={'pk': self.kwargs['pk']})


class OrderItemUpdateView(generic.UpdateView):
    template_name = 'orders/orderItem_update.html'
    form_class = OrderItemUpdateModelForm
    model = models.OrderItem

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado el pedido')
        order_id = models.OrderItem.objects.get(id=self.kwargs['pk']).order_id
        return reverse_lazy('orderItem-list', kwargs={'pk': order_id})


class OrderItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.OrderItem

    def get_success_url(self):
        order_id = models.OrderItem.objects.get(id=self.kwargs['pk']).order_id
        return reverse_lazy('orderItem-list', kwargs={'pk': order_id})

