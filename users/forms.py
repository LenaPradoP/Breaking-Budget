from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# Used by the Django admin to add new users
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "role")  


# Used by the Django admin to edit users
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")  

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

# For admins to edit travelers' account details, excluding password and role
class AdminUserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")

# For admins to filter and order the users list
class UserFilterForm(forms.Form):
    ROLE_CHOICES = [
        ('', 'Filter by'), 
        ('traveler', 'Traveler'),
        ('admin', 'Admin'),
    ]
    
    ORDER_CHOICES = [
        ('', 'Order by'), 
        ('role', 'Admins first'),
        ('-role', 'Travelers first'), 
        ('date_joined', 'Older first'),  
        ('-date_joined', 'Newer first'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=False, 
        widget=forms.Select(attrs={
            'id': 'role-filter',
        })
    )
    
    order_by = forms.ChoiceField(
        choices=ORDER_CHOICES,
        required=False, 
        widget=forms.Select(attrs={
            'id': 'order-filter',
        })
    )
