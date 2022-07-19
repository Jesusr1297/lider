from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderView.as_view(), name='home'),
    path('detalle/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('crear/', OrderCreateView.as_view(), name='order-create'),
    path('editar/<int:pk>', OrderUpdateView.as_view(), name='order-update'),
    path('eliminar/<int:pk>', OrderDeleteView.as_view(), name='order-delete'),
    path('clientes/', CustomersView.as_view(), name='customers'),
    path('trabajos/', LiderView.as_view(), name='lider'),
    path('cotizaciones/', budget, name='budgets')


]
