import pytest
from users.models import CustomUser

@pytest.fixture
def admin_user(db):
    """A normal admin (not superuser)."""
    return CustomUser.objects.create_user(
        username="admin1",
        password="pass123",
        role=CustomUser.Role.ADMIN,
        is_staff=True,
        is_superuser=False,
    )

@pytest.fixture
def traveler(db):
    """A regular traveler."""
    return CustomUser.objects.create_user(
        username="trav1",
        password="pass123",
        role=CustomUser.Role.TRAVELER,
        is_staff=False,
        is_superuser=False,
    )

@pytest.fixture
def superuser(db):
    """A Django superuser (hidden from your web UI)."""
    return CustomUser.objects.create_user(
        username="root",
        password="pass123",
        role=CustomUser.Role.TRAVELER,  # all Users are created as Traveler role by default, that is fine
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def admin_client(client, admin_user):
    """A test client already logged in as admin."""
    client.force_login(admin_user)  
    return client

@pytest.fixture
def traveler_client(client, traveler):
    """A test client already logged in as traveler."""
    client.force_login(traveler)
    return client
