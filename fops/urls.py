from django.urls import path
from . import views

app_name = 'fops'

urlpatterns = [
    path('', views.fop_list_view, name='list'),
    path('create/', views.fop_create_view, name='create'),
    path('<int:pk>/edit/', views.fop_update_view, name='update'),
]