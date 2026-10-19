from pathlib import Path

from django.contrib.staticfiles import finders
from django.test import SimpleTestCase


class StaticFilesTests(SimpleTestCase):
    def test_dashboard_script_exists_and_is_not_empty(self):
        path = finders.find("JS/dashboard.js")

        self.assertIsNotNone(
            path,
            "Не найден static/JS/dashboard.js",
        )

        content = Path(path).read_text(encoding="utf-8")

        self.assertTrue(
            content.strip(),
            "dashboard.js пустой. Проверь, сохранён ли код.",
        )

    def test_charts_script_exists(self):
        self.assertIsNotNone(
            finders.find("JS/charts.js"),
            "Не найден static/JS/charts.js",
        )

    def test_company_panel_script_exists(self):
        self.assertIsNotNone(
            finders.find("JS/company-panel.js"),
            "Не найден static/JS/company-panel.js",
        )