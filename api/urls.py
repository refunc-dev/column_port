from django.urls import path

from . import views


urlpatterns = [
    path('keywords/', views.KeywordListAPIView.as_view()),
    path('keywords/update/<int:pk>/', views.KeywordUpdateAPIView.as_view()),
    path('ranking/create/', views.KeywordSerpCreateAPIView.as_view())
]