from django.urls import path

from ranking import views

urlpatterns = [
    path('', views.ranking_top, name='ranking_top'),
    path('all/', views.ranking_all, name='ranking_all'),
    path('range/', views.ranking_range, name='ranking_range'),
    path('score/', views.ranking_score, name='ranking_score'),
    path('all/add/', views.ranking_all_add, name='ranking_all_add'),
    path('all/delete/', views.ranking_all_delete, name='ranking_all_delete'),
]