from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('', views.salary_list_view, name='list'),
    path('calculate/', views.calculate_salaries_view, name='calculate'),
]