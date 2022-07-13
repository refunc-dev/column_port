from django.urls import path

from projects import views

urlpatterns = [
    path('', views.project_top, name='project_top'),
    path('settings/', views.project_settings, name='project_settings'),
]