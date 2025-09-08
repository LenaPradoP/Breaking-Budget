from django.urls import path
from .views import LoginView, DetailView, CreateView, ListUsers

app_name = "users"

urlpatterns = [
    path("login/", LoginView.login_user, name="login"),
    path("home/", LoginView.home, name="home"),
    path("<int:pk>/", DetailView.user_detail, name="user_detail"),
    path("new/", CreateView.new_user, name="new_user"),
    path("create/", CreateView.create_user, name="create_user"),
    path("list_users/", ListUsers.view_users, name="list_users"),
]
