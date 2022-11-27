from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from orders.views import SignUpView, LandingPageView, search_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='home'),
    path('ordenes/', include('orders.urls')),
    path('clientes/', include('customers.urls')),
    path('trabajos/', include('lider.urls')),
    path('cotizaciones/', include('budgets.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', SignUpView.as_view(), name='register-signup'),

    path('busqueda/', search_view, name='search'),

]
