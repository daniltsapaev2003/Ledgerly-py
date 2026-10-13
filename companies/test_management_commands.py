from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from companies.management.commands import import_financial_data
from companies.management.commands.seed_demo import (
    Command as SeedDemoCommand,
)


class DemoCommandsTests(TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.base_dir = Path(self.temp_dir.name)
        self.data_dir = (
            self.base_dir / "static" / "financial_data"
        )
        self.forecasts_dir = (
            self.base_dir / "static" / "forecasts"
        )

        self.data_dir.mkdir(parents=True)
        self.forecasts_dir.mkdir(parents=True)

        settings_override = self.settings(
            BASE_DIR=self.base_dir
        )
        settings_override.enable()
        self.addCleanup(settings_override.disable)

    def run_command(self, name):
        call_command(
            name,
            stdout=StringIO(),
            stderr=StringIO(),
        )

    def test_import_accepts_empty_directories(self):
        self.run_command("import_financial_data")

    def test_forecasts_run_without_financial_files(self):
        forecast = self.forecasts_dir / "SBER.txt"
        forecast.write_text(
            "Demo Analyst=BUY=350\n",
            encoding="utf-8",
        )

        with patch.object(
            import_financial_data,
            "sync_forecast_file",
        ) as sync_forecast:
            self.run_command("import_financial_data")

        sync_forecast.assert_called_once_with(forecast)

    def test_import_reports_errors_and_continues(self):
        for filename in (
            "SBER_2026_Q1.txt",
            "SBER_2026_Q2.txt",
        ):
            (self.data_dir / filename).write_text(
                "revenue=100\n",
                encoding="utf-8",
            )

        with patch.object(
            import_financial_data,
            "sync_file",
            side_effect=[ValueError("broken file"), None],
        ) as sync_file:
            with self.assertRaises(CommandError):
                self.run_command("import_financial_data")

        self.assertEqual(sync_file.call_count, 2)

    def test_forecast_error_fails_command(self):
        (self.forecasts_dir / "SBER.txt").write_text(
            "invalid\n",
            encoding="utf-8",
        )

        with patch.object(
            import_financial_data,
            "sync_forecast_file",
            side_effect=ValueError("broken forecast"),
        ):
            with self.assertRaises(CommandError):
                self.run_command("import_financial_data")

    def test_empty_seed_creates_user_without_api(self):
        with (
            patch.dict(
                "os.environ",
                {
                    "DEMO_USERNAME": "demo-test",
                    "DEMO_PASSWORD": "initial-demo-password",
                },
            ),
            patch.object(
                SeedDemoCommand,
                "sync_companies",
            ) as sync_companies,
        ):
            self.run_command("seed_demo")

            user = get_user_model().objects.get(
                username="demo-test"
            )
            self.assertTrue(
                user.check_password("initial-demo-password")
            )
            self.assertFalse(user.is_staff)
            self.assertFalse(user.is_superuser)

            user.set_password("changed-demo-password")
            user.save()

            self.run_command("seed_demo")

        sync_companies.assert_not_called()

        user.refresh_from_db()
        self.assertTrue(
            user.check_password("changed-demo-password")
        )
        self.assertEqual(
            get_user_model().objects.filter(
                username="demo-test"
            ).count(),
            1,
        )

    def test_seed_propagates_import_error(self):
        with (
            patch.dict(
                "os.environ",
                {
                    "DEMO_USERNAME": "failed-demo",
                    "DEMO_PASSWORD": "demo-password",
                },
            ),
            patch(
                "companies.management.commands.seed_demo.call_command",
                side_effect=CommandError("import failed"),
            ),
        ):
            with self.assertRaises(CommandError):
                self.run_command("seed_demo")

        self.assertFalse(
            get_user_model().objects.filter(
                username="failed-demo"
            ).exists()
        )