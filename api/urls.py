from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('keywords/', views.KeywordListAPIView.as_view()),
    path('keywords/update/<int:pk>/', views.KeywordUpdateAPIView.as_view()),
    path('ranking/create/', views.KeywordSerpCreateAPIView.as_view())
]