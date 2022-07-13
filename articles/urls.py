from django.urls import path

from articles import views

urlpatterns = [
    path('', views.top, name='article_top'),
    path('<str:article_id>/', views.settings, name='article_settings'),
    path('<str:article_id>/remove_keywords/', views.remove_keywords, name='article_remove_keywords'),
]