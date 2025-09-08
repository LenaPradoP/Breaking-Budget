from django.urls import path
from .views import LoginView, DetailView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.login_user, name="login"),
    path("home/", LoginView.home, name="home"),
    path("<int:pk>/", DetailView.user_detail, name="user_detail"),
   
]
