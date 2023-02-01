from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = models.Order
    template_name = 'orders/order_complete_list.html'
    ordering = ['-id']


class OrderPendingListView(LoginRequiredMixin, generic.ListView):
    queryset = models.Order.objects.filter(orderitem__finished=False).distinct()
    template_name = 'orders/order_list.html'
    paginate_by = 10


class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = forms.OrderModelForm
    template_name = 'orders/order_form.html'
    success_message = 'Se ha creado una nueva orden'

    def get_success_url(self, **kwargs):
        return reverse_lazy('orderItem-list', kwargs={'pk': self.object.pk})


class OrderCreateFromCustomerView(LoginRequiredMixin, generic.TemplateView):
    """Create a new order from customer detail view"""

    def get(self, request, *args, **kwargs):
        customers_id = kwargs['pk']
        new_order = models.Order.objects.create(customer_id=customers_id)
        return redirect('orderItem-list', new_order.id)


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Order
    template_name = 'orders/order_detail.html'


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'orders/order_update.html'
    form_class = forms.OrderUpdateModelForm
    model = models.Order

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado la orden')
        return reverse_lazy('order-detail', kwargs={'pk': self.kwargs['pk']})


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Order

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado la orden: {self.object.id:03d}')
        return reverse_lazy('home')


class OrderItemListView(LoginRequiredMixin, generic.TemplateView):

    def get(self, request, *args, **kwargs):
        context = {
            'items': models.OrderItem.objects.filter(order_id=kwargs['pk']),
            'order': models.Order.objects.get(id=kwargs['pk'])
        }
        return render(request, template_name='orders/orderItem_list.html', context=context)


class OrderItemCreateView(LoginRequiredMixin, generic.FormView):
    form_class = forms.OrderItemCreateModelForm
    template_name = 'orders/order_form.html'

    def get_form_kwargs(self, **kwargs):
        """ We need pass custom kwargs to form (because working with FormView"""

        # Instantiate kwargs by calling the function with super
        kwargs = super(OrderItemCreateView, self).get_form_kwargs(**kwargs)

        # updating values, in this case pk, it's what we need to pass to form
        kwargs.update({'pk': self.kwargs['pk']})

        # returning updated dictionary
        return kwargs

    def form_valid(self, form):
        # Before updating the model we add missing fields that
        # user cannot write for security reasons
        instance = form.save(commit=False)
        instance.order_id = self.kwargs['pk']
        instance.customer_id = models.Order.objects.get(id=instance.order_id).customer_id
        instance.save()
        return super(OrderItemCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Se ha agregado al pedido')
        return reverse_lazy('orderItem-list', kwargs={'pk': self.kwargs['pk']})


class OrderItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'orders/orderItem_update.html'
    form_class = forms.OrderItemUpdateModelForm
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


class OrderMarkAsCompleted(LoginRequiredMixin, generic.TemplateView):
    """Mark order as completed by changing all its orderItem status"""

    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_item_qs = models.OrderItem.objects.filter(order_id=order_id)
        for order_item in order_item_qs:
            order_item.finished = True
            order_item.save()
        return redirect('orderItem-list', order_id)
