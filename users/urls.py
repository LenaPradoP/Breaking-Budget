from django.urls import path
from .views import LoginView, DetailView, CreateView, ListUsers, UpdateView, DeleteUser

app_name = "users"

urlpatterns = [
    path("login/", LoginView.login_user, name="login"),
    path("home/", LoginView.home, name="home"),
    path("logout/", LoginView.logout_user, name="logout"),
    path("<int:pk>/", DetailView.user_detail, name="user_detail"),
    path("new/", CreateView.new_user, name="new_user"),
    path("create/", CreateView.create_user, name="create_user"),
    path("list/", ListUsers.view_users, name="view_users"),
    path("<int:pk>/edit/", UpdateView.edit_user, name="edit_user"),
    path("<int:pk>/update/", UpdateView.update_user, name="update_user"),
    path("<int:pk>/delete/", DeleteUser.delete_user, name="delete_user"),
]
