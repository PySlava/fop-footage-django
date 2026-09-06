from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('', views.salary_list_view, name='list'),
    path('calculate/', views.calculate_salaries_view, name='calculate'),
    path('payslip/<int:pk>/pdf/', views.download_payslip_pdf_view, name='payslip_pdf'),
    path('calculator/', views.vacation_sick_calculator_view, name='calculator'),
]