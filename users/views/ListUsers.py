from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import CustomUser
from ..forms import UserFilterForm


@login_required
def view_users(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    role = getattr(request.user, "role", None)
    is_admin = (
        (hasattr(CustomUser, "Role") and role == CustomUser.Role.ADMIN) or (role == "admin")
    )
    if not is_admin:
        raise PermissionDenied
    users = CustomUser.objects.all().order_by("username")

    form, users = apply_user_filters_and_ordering(request, users)

    context = {
        "users": users,
        "form": form,
    }
    
    return render(request, 'users/list_users.html', context)

def apply_user_filters_and_ordering(request, initial_queryset):
    """
    Helper function that applies filters and ordering to an existing queryset.
    
    Args:
        request: HttpRequest object
        initial_queryset: The base queryset to filter/order
    
    Returns:
        tuple: (form, filtered_queryset)
    """
    form = UserFilterForm(request.GET)
    
    users = initial_queryset
    
    if form.is_valid():
        if form.cleaned_data['role']:
            users = users.filter(role=form.cleaned_data['role'])
        
        if form.cleaned_data['order_by']:
            users = users.order_by(form.cleaned_data['order_by'])
    
    return form, users