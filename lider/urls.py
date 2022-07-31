from django.urls import path
from .views import (LiderView, LiderCreateView, LiderDetailView)

urlpatterns = [
    path('', LiderView.as_view(), name='lider'),
    path('crear/', LiderCreateView.as_view(), name='lider-create'),
    path('detalle/<int:pk>/', LiderDetailView.as_view(), name='lider-detail'),

]
