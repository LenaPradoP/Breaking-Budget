from django.urls import path
from .views import LoginView, DetailView, CreateView, DeleteUser

app_name = "users"

urlpatterns = [
    path("login/", LoginView.login_user, name="login"),
    path("home/", LoginView.home, name="home"),
    path("<int:pk>/", DetailView.user_detail, name="user_detail"),
    path("new/", CreateView.new_user, name="new_user"),
    path("create/", CreateView.create_user, name="create_user"),
    path("<int:pk>/", DeleteUser.delete_user, name="delete_user"),


]
