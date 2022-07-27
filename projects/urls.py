from django.urls import path

from projects import views

urlpatterns = [
    path('', views.project_top, name='project_top'),
    path('settings/', views.project_settings, name='project_settings'),
    path('settings/delete/', views.project_settings_delete, name='project_settings_delete'),
    path('settings/analytics/', views.project_settings_analytics, name='project_settings_analytics'),
    path('settings/members/', views.project_settings_members, name='project_settings_members'),
    path('settings/members/delete/', views.project_settings_members_delete, name='project_settings_members_delete'),
    path('settings/competitors/', views.project_settings_competitors, name='project_settings_competitors'),
    path('settings/competitors/delete/', views.project_settings_competitors_delete, name='project_settings_competitors_delete'),
]