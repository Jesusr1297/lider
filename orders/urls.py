from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('detalle/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('crear/', OrderCreateView.as_view(), name='order-create'),
    path('editar/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('eliminar/<int:pk>/', OrderDeleteView.as_view(), name='order-delete'),
    path('busqueda/', search_view, name='search'),

    path('crear-order/<int:pk>/', OrderItemAddView.as_view(), name='orderItem-add'),
    path('editar-orden/<int:pk>/', OrderItemUpdateView.as_view(), name='orderItem-update'),
]
