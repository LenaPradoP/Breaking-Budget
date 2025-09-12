from django.urls import reverse
from users.models import CustomUser

# 1) Admin can GET the form
def test_admin_can_get_new_user_form(admin_client):
    url = reverse("users:new_user")
    resp = admin_client.get(url)
    assert resp.status_code == 200

# 2) Traveler cannot GET the form
def test_traveler_cannot_get_new_user_form(traveler_client):
    url = reverse("users:new_user")
    resp = traveler_client.get(url)
    assert resp.status_code == 403

# 3) Admin can create a Traveler (happy path)
def test_admin_can_create_traveler(admin_client, db):
    url = reverse("users:create_user")
    payload = {
        "username": "newtrav",
        "email": "newtrav@breakingbudget.com",
        "first_name": "New",
        "last_name": "Traveler",
        "password1": "StrongP@ssw0rd123",
        "password2": "StrongP@ssw0rd123",
    }
    resp = admin_client.post(url, data=payload, follow=True)
    assert resp.status_code in (200, 302)
    u = CustomUser.objects.get(username="newtrav")
    assert u.role == CustomUser.Role.TRAVELER  # role is forced

# 4) Traveler cannot create users (POST → 403)
def test_traveler_cannot_create_user(traveler_client, db):
    url = reverse("users:create_user")
    payload = {
        "username": "should_not_create",
        "email": "should_not_create@breakingbudget.com",
        "first_name": "Should",
        "last_name": "Not",
        "password1": "StrongP@ssw0rd123",
        "password2": "StrongP@ssw0rd123",
    }
    resp = traveler_client.post(url, data=payload, follow=True)
    # Your view raises PermissionDenied → 403
    assert resp.status_code == 403
    assert not CustomUser.objects.filter(username="should_not_create").exists()

# 5) Malicious POST cannot elevate role — still created as Traveler
def test_admin_cannot_force_admin_role_via_post(admin_client, db):
    url = reverse("users:create_user")
    payload = {
        "username": "sneaky",
        "email": "sneaky@example.com",
        "first_name": "Sneaky",
        "last_name": "User",
        "password1": "StrongP@ssw0rd123",
        "password2": "StrongP@ssw0rd123",
        # even if someone injects this field in the request:
        "role": "admin",
    }
    resp = admin_client.post(url, data=payload, follow=True)
    assert resp.status_code in (200, 302)
    user = CustomUser.objects.get(username="sneaky")
    assert user.role == CustomUser.Role.TRAVELER  # form/view ignores injected role
