from django.urls import path
from .views import LoginView, DetailView, CreateView, UpdateView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.login_user, name="login"),
    path("home/", LoginView.home, name="home"),
    path("<int:pk>/", DetailView.user_detail, name="user_detail"),
    path("new/", CreateView.new_user, name="new_user"),
    path("create/", CreateView.create_user, name="create_user"),
    path("<int:pk>/edit/", UpdateView.edit_user, name="edit_user"),
    path("<int:pk>/update/", UpdateView.update_user, name="update_user"),

    #Just to try update_user works. Delete after User Detail is implemented. 
    path("<int:pk>/password-changed/", UpdateView.password_changed_success, name="password_changed"),



]
