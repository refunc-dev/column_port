from django.urls import path

from articles import views

urlpatterns = [
    path('<int:article_id>/', views.article_detail, name='article_detail'),
    path('<int:article_id>/delete_keywords/', views.delete_keywords, name='delete_keywords'),
]