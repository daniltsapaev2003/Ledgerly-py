from django.contrib.auth.hashers import check_password, make_password
from django.test import TestCase
from django.urls import reverse

from ledgerly.models import User


class AuthViewsTests(TestCase):
    def setUp(self):
        self.password = "test-password-123"
        self.user = User.objects.create(
            first_name="Иван",
            last_name="Тестов",
            email="test@example.com",
            phone_number="+79990000000",
            password=make_password(self.password),
        )

    def test_register_get_returns_page(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Loginpage.html")

    def test_register_empty_post_does_not_create_user(self):
        response = self.client.post(reverse("register"), {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["missing_fields"])
        self.assertEqual(User.objects.count(), 1)
        self.assertNotIn("session", self.client.session)

    def test_register_valid_post_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Анна",
                "last_name": "Тестова",
                "email": "new@example.com",
                "phone_number": "+79990000001",
                "password": self.password,
            },
        )

        self.assertRedirects(
            response,
            reverse("Dashboard"),
            fetch_redirect_response=False,
        )
        user = User.objects.get(email="new@example.com")
        self.assertTrue(check_password(self.password, user.password))
        self.assertEqual(self.client.session["session"], user.pk)

    def test_register_duplicate_email_returns_error(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Иван",
                "last_name": "Тестов",
                "email": self.user.email,
                "phone_number": "+79990000000",
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user_exists"])
        self.assertEqual(User.objects.count(), 1)
        self.assertNotIn("session", self.client.session)

    def test_login_get_returns_page(self):
        response = self.client.get(reverse("CheckUser"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Loginpage.html")

    def test_login_missing_or_empty_fields_returns_error(self):
        payloads = [
            {},
            {"email": self.user.email},
            {"password": self.password},
            {"email": "", "password": ""},
        ]

        for payload in payloads:
            with self.subTest(payload=payload):
                response = self.client.post(reverse("CheckUser"), payload)

                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["wrong_email_password"])
                self.assertNotIn("session", self.client.session)

    def test_login_valid_credentials_sets_session(self):
        response = self.client.post(
            reverse("CheckUser"),
            {
                "email": self.user.email,
                "password": self.password,
            },
        )

        self.assertRedirects(
            response,
            reverse("Dashboard"),
            fetch_redirect_response=False,
        )
        self.assertEqual(self.client.session["session"], self.user.pk)

    def test_login_wrong_password_does_not_set_session(self):
        response = self.client.post(
            reverse("CheckUser"),
            {
                "email": self.user.email,
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["wrong_email_password"])
        self.assertNotIn("session", self.client.session)

    def test_dashboard_without_session_redirects_to_login(self):
        response = self.client.get(reverse("Dashboard"))

        self.assertRedirects(response, reverse("Loginpage"))

    def test_dashboard_deleted_user_flushes_session(self):
        session = self.client.session
        session["session"] = self.user.pk
        session["old_data"] = "must be cleared"
        session.save()

        self.user.delete()

        response = self.client.get(reverse("Dashboard"))

        self.assertRedirects(response, reverse("Loginpage"))
        self.assertNotIn("session", self.client.session)
        self.assertNotIn("old_data", self.client.session)

    def test_dashboard_invalid_user_id_flushes_session(self):
        session = self.client.session
        session["session"] = "not-a-user-id"
        session.save()

        response = self.client.get(reverse("Dashboard"))

        self.assertRedirects(response, reverse("Loginpage"))
        self.assertNotIn("session", self.client.session)

    def test_dashboard_existing_user_returns_page(self):
        session = self.client.session
        session["session"] = self.user.pk
        session.save()

        response = self.client.get(reverse("Dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Dashboard.html")
        self.assertEqual(response.context["user"].pk, self.user.pk)

    def test_login_unknown_email_returns_error(self):
        response = self.client.post(
            reverse("CheckUser"),
            {
                "email": "unknown@example.com",
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["wrong_email_password"])
        self.assertNotIn("session", self.client.session)