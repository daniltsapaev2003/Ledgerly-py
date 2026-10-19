from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from ledgerly.models import User


class LogoutViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Иван",
            last_name="Тестов",
            email="logout@example.com",
            phone_number="+79990000002",
            password=make_password("test-password-123"),
        )

        session = self.client.session
        session["session"] = self.user.pk
        session.save()

    def test_logout_post_removes_authentication(self):
        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 302)
        self.assertNotIn("session", self.client.session)

    def test_dashboard_after_logout_redirects_to_login(self):
        self.client.post(reverse("logout"))

        response = self.client.get(reverse("Dashboard"))

        self.assertRedirects(response, reverse("Loginpage"))

    def test_logout_get_is_not_allowed(self):
        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)

        # Запрос GET не должен разлогинивать пользователя.
        self.assertEqual(
            self.client.session["session"],
            self.user.pk,
        )