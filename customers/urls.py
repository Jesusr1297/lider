from django.urls import path
from . import views


urlpatterns = [
    path('', views.CustomersView.as_view(), name='customers'),
    path('detalle/<int:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('crear/', views.CustomerCreateView.as_view(), name='customers-create'),
    path('editar/<int:pk>', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('eliminar/<int:pk>', views.CustomerDeleteView.as_view(), name='customer-delete'),
]
