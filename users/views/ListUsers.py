from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import CustomUser
from ..forms import UserFilterForm


@login_required
def view_users(request):
    is_admin = request.user.is_superuser or request.user.role == "admin"
    if not is_admin:
        raise PermissionDenied("You don't have permission to see this page")

    # Hide superusers from the web list
    users = CustomUser.objects.filter(is_superuser=False).order_by("username")

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
        role = form.cleaned_data.get('role')
        order_by = form.cleaned_data.get('order_by')

        if role:
            users = users.filter(role=role)

        users = users.order_by(order_by or 'username')  # fallback to username

    return form, users
