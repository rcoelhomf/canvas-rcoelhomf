from django.urls import path
from .views import UserView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('accounts/', UserView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
]
