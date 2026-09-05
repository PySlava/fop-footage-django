from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list_view, name='list'),
    path('create/', views.employee_create_view, name='create'),
    path('orders/', views.orders_list_view, name='orders_list'),
    path('<int:pk>/actions/', views.employee_actions_view, name='employee_actions'),
]