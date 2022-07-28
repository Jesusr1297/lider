from django.urls import path
from .views import *


urlpatterns = [
    path('', CustomersView.as_view(), name='customers'),
    path('detalle/<int:pk>', CustomerDetailView.as_view(), name='customer-detail'),
    path('crear/', CustomerCreateView.as_view(), name='customers-create'),
    path('editar/<int:pk>', CustomerUpdateView.as_view(), name='customer-update'),
    path('eliminar/<int:pk>', CustomerDeleteView.as_view(), name='customer-delete'),
]
