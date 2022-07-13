from django.urls import path

from analytics import views

urlpatterns = [
    path('', views.analytics_top, name='analytics_top'),
    path('weekly/', views.analytics_weekly, name='analytics_weekly'),
    path('monthly/', views.analytics_monthly, name='analytics_monthly'),
]