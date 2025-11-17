from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('races/', views.race_list, name='race_list'),
    path('register/', views.register, name='register'),
    path('race/<int:race_id>/participants/', views.participants, name='participants'),
    path('race/<int:race_id>/export/', views.export_csv, name='export_csv'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
