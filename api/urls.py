from django.urls import path

from . import views


urlpatterns = [
    path('keywords/', views.KeywordAPI.as_view()),
    path('ranking/create/', views.KeywordSerpCreateAPIView.as_view())
]