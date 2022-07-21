from django.urls import path
from .views import *

urlpatterns = [
    path('', LiderView.as_view(), name='lider'),
]
