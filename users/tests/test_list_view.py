from django.urls import reverse
from users.models import CustomUser

# 1) Travelers don’t have a list view of Users
def test_traveler_cannot_access_users_list(traveler_client):
    url = reverse("users:view_users")
    resp = traveler_client.get(url)
    assert resp.status_code == 403


# 2) Admins see all of the Users in the list (excluding superusers)
def test_admin_sees_all_non_superusers(admin_client, admin_user, traveler, superuser, db):
    admin_user.first_name, admin_user.last_name = "Alice", "Admin"
    admin_user.save()

    traveler.first_name, traveler.last_name = "Tom", "Traveler"
    traveler.save()

    admin2 = CustomUser.objects.create_user(
        username="admin2", password="pass123",
        role=CustomUser.Role.ADMIN, is_staff=True, is_superuser=False,
        first_name="Bob", last_name="Boss",
    )
    traveler2 = CustomUser.objects.create_user(
        username="traveler2", password="pass123",
        role=CustomUser.Role.TRAVELER, is_staff=False, is_superuser=False,
        first_name="Tina", last_name="Tourist",
    )

    superuser.first_name, superuser.last_name = "Root", "Super"
    superuser.save()

    resp = admin_client.get(reverse("users:view_users"))
    assert resp.status_code == 200
    body = resp.content.decode()

    # Should list all non-superusers by full name
    assert "Alice Admin" in body
    assert "Tom Traveler" in body
    assert "Bob Boss" in body
    assert "Tina Tourist" in body

    # Should NOT list superusers
    assert "Root Super" not in body
