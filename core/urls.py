from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),
    path('clientes/', include('customers.urls')),
    path('trabajos/', include('lider.urls')),
    path('cotizaciones/', include('budgets.urls')),
]
