from django.urls import path
from . import views

app_name = 'timesheet'

urlpatterns = [
    path('', views.timesheet_list_view, name='list'),
]