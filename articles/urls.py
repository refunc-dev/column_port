from django.urls import path

from articles import views

urlpatterns = [
    path('<int:article_id>/', views.keyword_new, name='keyword_new'),
]