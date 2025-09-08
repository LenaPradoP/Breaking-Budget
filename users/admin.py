from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomerUserAdmin(UserAdmin):
    # Use our forms
    add_form = CustomUserCreationForm      # for the Add page (has password1/password2)
    form = CustomUserChangeForm            # for the Edit page
    model = CustomUser

    # Columns on the list page
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")

    # ----- EDIT PAGE -----
    # Add your custom field(s) to the edit page layout
    fieldsets = (
        (None, {"fields": ("username", "password")}),  # 'password' is the hashed field
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Custom fields", {"fields": ("role",)}),       # <<-- show 'role' here
    )

    # ----- ADD PAGE -----
    # On the Add page we list form fields; password is split into password1/password2
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)
