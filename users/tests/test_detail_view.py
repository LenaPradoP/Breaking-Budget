from django.urls import reverse
from users.models import CustomUser

# --- Travelers ---

def test_traveler_can_view_own_detail(traveler_client, traveler):
    url = reverse("users:user_detail", kwargs={"pk": traveler.pk})
    resp = traveler_client.get(url)
    assert resp.status_code == 200
    assert traveler.username in resp.content.decode()

def test_traveler_cannot_view_other_user_detail(traveler_client, admin_user):
    url = reverse("users:user_detail", kwargs={"pk": admin_user.pk})
    resp = traveler_client.get(url)
    assert resp.status_code == 403


# --- Admins ---

def test_admin_can_view_traveler_detail(admin_client, traveler):
    url = reverse("users:user_detail", kwargs={"pk": traveler.pk})
    resp = admin_client.get(url)
    assert resp.status_code == 200
    assert traveler.username in resp.content.decode()

def test_admin_can_view_admin_detail(admin_client, admin_user, db):
    # another admin to view
    other_admin = CustomUser.objects.create_user(
        username="admin2",
        password="pass123",
        role=CustomUser.Role.ADMIN,
        is_staff=True,
        is_superuser=False,
    )
    url = reverse("users:user_detail", kwargs={"pk": other_admin.pk})
    resp = admin_client.get(url)
    assert resp.status_code == 200
    assert "admin2" in resp.content.decode()

def test_admin_cannot_view_superuser_detail(admin_client, superuser):
    # Detail view fetches with is_superuser=False, so superuser targets 404
    url = reverse("users:user_detail", kwargs={"pk": superuser.pk})
    resp = admin_client.get(url)
    assert resp.status_code == 404
