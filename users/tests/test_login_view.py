from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY  # "_auth_user_id"

User = get_user_model()


def _make_user(username="joaco", password="Str0ngP@ss!1"):
    user = User.objects.create_user(username=username, password=password)
    return user, password


def test_login_get_shows_authentication_form(client, db):
    """GET /login returns 200 and includes the form in context."""
    resp = client.get(reverse("login"))
    assert resp.status_code == 200
    # The login template should receive a 'form' (AuthenticationForm)
    ctx = resp.context[0] if isinstance(resp.context, list) else resp.context
    assert "form" in ctx


def test_login_post_with_valid_credentials_redirects_and_sets_session(client, db):
    """
    Valid POST should:
      - redirect (302) to expenses:list_expenses
      - set Django auth session key (= proves django.contrib.auth.login was used)
    """
    user, pwd = _make_user()
    url = reverse("login")

    resp = client.post(url, data={"username": user.username, "password": pwd})
    assert resp.status_code == 302
    assert resp.headers["Location"] == reverse("expenses:list_expenses")

    # Session has the auth user id if login() was called
    assert SESSION_KEY in client.session
    assert client.session[SESSION_KEY] == str(user.pk)


def test_login_post_with_invalid_credentials_shows_errors(client, db):
    """Invalid POST returns 200 with the form and non-field errors."""
    user, _ = _make_user()
    url = reverse("login")

    resp = client.post(url, data={"username": user.username, "password": "wrong"})
    assert resp.status_code == 200

    ctx = resp.context[0] if isinstance(resp.context, list) else resp.context
    form = ctx["form"]
    assert form.errors  # AuthenticationForm should carry errors
    # optional: check the common error text
    # assert "Please enter a correct" in resp.content.decode()
