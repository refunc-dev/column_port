from django.urls import path

from articles import views

urlpatterns = [
    path('', views.top, name='article_top'),
    path('add/', views.add, name='article_add'),
    path('<str:article_id>/', views.settings, name='article_settings'),
    path('<str:article_id>/update/', views.update, name='article_update'),
    path('<str:article_id>/delete/', views.delete, name='article_delete'),
    path('<str:article_id>/keywords/add/', views.add_keywords, name='article_add_keywords'),
    path('<str:article_id>/keywords/delete/', views.delete_keywords, name='article_delete_keywords'),
]