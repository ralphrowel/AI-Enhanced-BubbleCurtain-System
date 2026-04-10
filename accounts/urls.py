#account 

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
path("login/", views.login_view),
path("register/", RegisterView.as_view(), name="register"),

path("token/", TokenObtainPairView.as_view()),
path("token/refresh/", TokenRefreshView.as_view()),
]