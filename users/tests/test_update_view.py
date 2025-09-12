from django.urls import reverse
from django.test import Client
from users.models import CustomUser

# --- 1) Users can only edit their own password ---
def test_user_can_change_own_password(client, db):
    OLD = "OldP@ss123"
    NEW = "NewP@ss123!"
    # Create user with a known password
    user = CustomUser.objects.create_user(
        username="traveler1",
        password=OLD,
        role=CustomUser.Role.TRAVELER,
    )
    # Log in with OLD
    assert client.login(username="traveler1", password=OLD)

    # Change to NEW via the view
    url = reverse("users:update_user", kwargs={"pk": user.pk})
    payload = {"old_password": OLD, "new_password1": NEW, "new_password2": NEW}
    resp = client.post(url, data=payload, follow=True)
    assert resp.status_code in (200, 302)

    # Verify NEW works (and OLD doesn’t)
    fresh = Client()
    assert fresh.login(username="traveler1", password=NEW)
    assert not fresh.login(username="traveler1", password=OLD)


# --- 2) Admins can only edit Travelers' information, NOT passwords ---
def test_admin_edits_traveler_profile_not_password(admin_client, traveler, db):
    # Set a known password that must remain unchanged
    ORIGINAL_PW = "StaySame1!"
    traveler.set_password(ORIGINAL_PW)
    traveler.save()

    url = reverse("users:update_user", kwargs={"pk": traveler.pk})
    payload = {
        # AdminUserEditForm fields:
        "username": traveler.username,
        "email": "updated@breakingbudget.com",
        "first_name": "Updated",
        "last_name": "Traveler",
        # Try to sneak in password fields (should be ignored)
        "new_password1": "ShouldNotChange!1",
        "new_password2": "ShouldNotChange!1",
    }
    resp = admin_client.post(url, data=payload, follow=True)
    assert resp.status_code in (200, 302)

    # Profile changed
    traveler.refresh_from_db()
    assert traveler.email == "updated@breakingbudget.com"
    assert traveler.first_name == "Updated"
    assert traveler.last_name == "Traveler"

    # Password unchanged (admin cannot change a traveler's password via this view)
    fresh = Client()
    assert fresh.login(username=traveler.username, password=ORIGINAL_PW)


# --- 3) Admins cannot edit anything on other Admins ---
def test_admin_cannot_edit_other_admin(admin_client, db):
    other_admin = CustomUser.objects.create_user(
        username="admin2",
        password="pass123",
        role=CustomUser.Role.ADMIN,
        is_staff=True,
        is_superuser=False,
    )

    # GET edit page blocked
    resp_get = admin_client.get(reverse("users:edit_user", kwargs={"pk": other_admin.pk}))
    assert resp_get.status_code == 403

    # POST update blocked
    resp_post = admin_client.post(
        reverse("users:update_user", kwargs={"pk": other_admin.pk}),
        data={"username": "hacked"},
        follow=True,
    )
    assert resp_post.status_code == 403
