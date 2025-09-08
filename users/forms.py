from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Used by the web login view
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# Used by the Django admin to add new users
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "username", "role")  


# Used by the Django admin to edit users
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "username", "role")  

class CustomUserWebCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")  

    def save(self, commit=True):
        user = super().save(commit=False)  
        user.role = getattr(CustomUser.Role, "TRAVELER", "traveler")
        if commit:
            user.save()
        return user
