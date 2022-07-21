from django.urls import path
from .views import *


urlpatterns = [
    path('', CustomersView.as_view(), name='customers'),
]
