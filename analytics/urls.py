from django.urls import path

from analytics import views

urlpatterns = [
    path('', views.analytics_top, name='analytics_top'),
    path('weekly/', views.analytics_weekly, name='analytics_weekly'),
    path('monthly/', views.analytics_monthly, name='analytics_monthly'),
    path('regex/add/', views.regex_add, name='regex_add'),
    path('regex/settings/', views.regex_settings, name='regex_settings'),
]