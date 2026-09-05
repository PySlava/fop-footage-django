from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.notice_list_view, name='list'),
    path('notice/', views.notice_list_view, name='notice_list'),
    path('<int:pk>/download-docx/', views.download_employment_notice_view, name='download_employment_notice'),
]