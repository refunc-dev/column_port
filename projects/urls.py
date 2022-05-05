from django.urls import path

from projects import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('new/', views.project_new, name='project_new'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
]