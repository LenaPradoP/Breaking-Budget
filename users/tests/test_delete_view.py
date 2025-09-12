from django.urls import reverse
from users.models import CustomUser

# 1) Ensure only Travelers can be deleted (admins can delete travelers)
def test_admin_can_delete_traveler(admin_client, traveler, db):
    url = reverse("users:delete_user", kwargs={"pk": traveler.pk})
    resp = admin_client.post(url, follow=True)   
    assert resp.status_code in (200, 302)
    assert not CustomUser.objects.filter(pk=traveler.pk).exists()

# 2) Ensure Admins cannot be deleted
def test_admin_cannot_delete_admin(admin_client, admin_user, db):
    other_admin = CustomUser.objects.create_user(
        username="admin2",
        password="pass123",
        role=CustomUser.Role.ADMIN,
        is_staff=True,
        is_superuser=False,
    )
    url = reverse("users:delete_user", kwargs={"pk": other_admin.pk})
    resp = admin_client.post(url, follow=True)
    # should NOT delete the other admin
    assert resp.status_code in (200, 302)
    assert CustomUser.objects.filter(pk=other_admin.pk).exists()

# 3) Ensure Admins cannot delete themselves
def test_admin_cannot_delete_self(admin_client, admin_user, db):
    url = reverse("users:delete_user", kwargs={"pk": admin_user.pk})
    resp = admin_client.post(url, follow=True)
    assert resp.status_code in (200, 302)
    assert CustomUser.objects.filter(pk=admin_user.pk).exists()
