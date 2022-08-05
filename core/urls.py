from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),
    path('clientes/', include('customers.urls')),
    path('trabajos/', include('lider.urls')),
    path('cotizaciones/', include('budgets.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
