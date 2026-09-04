from django.urls import path
from . import views

urlpatterns = [
    path('', views.fop_list, name='fop_list'),
    path('add/', views.fop_create, name='fop_create'),
]