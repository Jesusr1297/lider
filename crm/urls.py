from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderView.as_view(), name='home'),
    path('/detalle/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('/clientes/', CustomersView.as_view(), name='customers'),
    path('/trabajos/', LiderView.as_view(), name='lider'),
    path('/cotizaciones/', budget, name='budgets')


]
