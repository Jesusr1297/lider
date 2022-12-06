from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.SupplierListView.as_view(), name='supplier-list'),
    path('crear/', views.SupplierCreateView.as_view(), name='supplier-create'),
    path('detalle/<slug:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
]
