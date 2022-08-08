from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .forms import UserRegisterForm



class OrderView(ListView):
    model = Order
    template_name = 'orders/order.html'
    ordering = ['-id']
    paginate_by = 2


class OrderCreateView(SuccessMessageMixin, CreateView):
    model = Order
    fields = ['lider_id', 'customer', 'quantity_ordered']
    success_url = reverse_lazy('home')
    success_message = 'Se ha creado una nueva orden'


class OrderDetailView(DetailView):
    model = Order


class OrderUpdateView(UpdateView):
    model = Order
    fields = '__all__'

    """
    Se utiliza la funcion get_success_url en lugar del metodo success_url para poder agregar
    el mensaje de actualizacion en el color que necesitamos, ya que SuccessMessageMixin solo 
    nos permite agregar mensajes de SUCCESS, en esto caso nosotros queremos uno de INFO.
    """

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Se ha actualizado la orden')
        return reverse_lazy('home')


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    """
    Se puede usar directamente success_url para regresar al menu principal, 
    pero al nosotros querer agregar un mensaje, sobre escribimos el metodo
    y agregamos el mensaje en get_success_url
    """
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        messages.error(self.request, f'Se ha eliminado la orden: {self.object.id:03d}')
        return reverse_lazy('home')


def search_view(request):
    if request.method == 'GET' and request.GET.get('q') is not '':
        q = request.GET.get('q') if request.GET.get('q') is not None else ''
        orders = Order.objects.filter(Q(customer__name_company__icontains=q) |
                                      Q(lider_id__lider_id__icontains=q))
        customers = Customer.objects.filter(Q(name_company__icontains=q))
        lider = Lider.objects.filter(Q(lider_id__icontains=q) |
                                     Q(doc_description__icontains=q) |
                                     Q(doc_inks__icontains=q))

        context = {
            'orders': orders.order_by('-id'),
            'customers': customers,
            'lider': lider
        }
    else:
        context = {}

    return render(request, 'search/search.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'La cuenta {username} se ha creado exitosamente. Puedes iniciar sesion')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
