from django.urls import path

from projects import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_top, name='project_top'),
    path('<int:project_id>/article-manager/', views.article_manager, name='article_manager'),
    path('<int:project_id>/reports/weekly/', views.report_weekly, name='report_weekly'),
    path('<int:project_id>/reports/monthly/', views.report_monthly, name='report_monthly'),
]