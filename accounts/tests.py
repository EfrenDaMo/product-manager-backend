import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestMeEndpoint:
    def test_me_returns_current_user(self, auth_client, user):
        response = auth_client.get("/api/v1/auth/me")

        assert response.status_code == 200
        assert response.data["email"] == user.email

    def test_me_requires_authentication(self, api_client):
        response = api_client.get("/api/v1/auth/me")

        assert response.status_code == 401

    def test_patch_me_updates_user(self, auth_client):
        response = auth_client.patch("/api/v1/auth/me", {"email": "update@example.com"})

        assert response.status_code == 200
        assert response.data["email"] == "update@example.com"

@pytest.mark.django_db
class TestChangePassword:
    def test_change_password_success(self, auth_client, user):
        response = auth_client.post(
            "/api/v1/auth/change-password",
            {"old_password": "testpass123", "new_password": "newpass456"}
        )

        assert response.status_code == 200
        user.refresh_from_db()
        assert user.check_password("newpass456")

    def test_change_password_wrong_old(self, auth_client, user):
        response = auth_client.post(
            "/api/v1/auth/change-password",
            {"old_password": "wrongpass123", "new_password": "newpass456"}
        )

        assert response.status_code == 400

@pytest.mark.django_db
class TestUserListCreate:
    def test_list_users_as_admin(self, admin_client, user):
        response = admin_client.get("/api/v1/user/")

        assert response.status_code == 200

    def test_list_users_forbidden_for_staff(self, auth_client):
        response = auth_client.get("/api/v1/user/")

        assert response.status_code == 403

    def test_create_user_as_admin(self, admin_client):
        response = admin_client.post(
            "/api/v1/user/",
            {"username": "newuser", "email": "new@example.com", "password": "Test!Pass456", "role": "staff"}
        )

        assert response.status_code == 201
        assert User.objects.filter(email="new@example.com").exists()


@pytest.mark.django_db
class TestUserToggle:
    def test_toggle_user_active(self, admin_client, user):
        assert user.is_active is True

        response = admin_client.patch(f"/api/v1/user/{user.pk}/toggle")
        assert response.status_code == 200

        user.refresh_from_db()
        assert user.is_active is False
