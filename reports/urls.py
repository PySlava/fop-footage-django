from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.notice_list_view, name='list'),  # Повернули name='list'
    path('notice/', views.notice_list_view, name='notice_list'),
    path('<int:employee_id>/download-docx/', views.download_employment_notice_view, name='download_employment_notice'),
    path('dps-notification/<int:employee_id>/xml/', views.download_dps_notification_xml, name='dps_notification_xml'),
]