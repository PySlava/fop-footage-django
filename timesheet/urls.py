from django.urls import path
from . import views

app_name = 'timesheet'

urlpatterns = [
    path('', views.timesheet_list_view, name='list'),
    path('export/xlsx/', views.download_timesheet_xlsx_view, name='timesheet_xlsx'),
]