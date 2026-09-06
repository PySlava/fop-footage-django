from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.notice_list_view, name='list'),
    path('notice/', views.notice_list_view, name='notice_list'),
    path('<int:employee_id>/download-docx/', views.download_employment_notice_view, name='download_employment_notice'),
    path('<int:employee_id>/download-contract/', views.download_labor_contract_view, name='download_labor_contract'),
    path('<int:employee_id>/order/<str:order_type>/', views.download_order_docx_view, name='download_order'),
    path('dps-notification/<int:employee_id>/xml/', views.download_dps_notification_xml, name='dps_notification_xml'),
]