from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('crear/', views.OrderCreateView.as_view(), name='order-create'),
    path('detalle/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('editar/<int:pk>/', views.OrderUpdateView.as_view(), name='order-update'),
    path('eliminar/<int:pk>/', views.OrderDeleteView.as_view(), name='order-delete'),

    path('ver-orden/<int:pk>/', views.OrderItemListView.as_view(), name='orderItem-list'),
    path('crear-orden/<int:pk>/', views.OrderItemCreateView.as_view(), name='orderItem-create'),
    path('editar-orden/<int:pk>/', views.OrderItemUpdateView.as_view(), name='orderItem-update'),
    path('eliminar-orden/<int:pk>/', views.OrderItemDeleteView.as_view(), name='orderItem-delete'),

    path('crear/<int:pk>/', views.OrderCreateFromCustomerView.as_view(), name='order-create-from-customer'),
]
