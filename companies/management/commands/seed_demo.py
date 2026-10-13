import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from companies.models import Company


class Command(BaseCommand):
    help = "Загрузка компаний и финансовых данных, создание демопользователя."

    def handle(self, *args, **options):
        username = os.environ.get("DEMO_USERNAME", "demo")
        password = os.environ.get("DEMO_PASSWORD")
        email = os.environ.get("DEMO_EMAIL", "demo@example.com")

        if not username:
            raise CommandError("DEMO_USERNAME не должен быть пустым.")

        User = get_user_model()

        user_exists = User.objects.filter(username=username).exists()

        if not user_exists and not password:
            raise CommandError(
                "Для создания демопользователя задайте DEMO_PASSWORD."
            )

        base_dir = Path(settings.BASE_DIR)
        data_dir = base_dir / "static" / "financial_data"
        forecasts_dir = base_dir / "static" / "forecasts"

        has_files = (
            any(data_dir.glob("*.txt"))
            or any(forecasts_dir.glob("*.txt"))
        )

        if has_files:
            try:
                self.sync_companies()
            except Exception as error:
                raise CommandError(
                    f"Не удалось загрузить компании из T-Invest: {error}"
                ) from error
        else:
            self.stdout.write(
                "TXT-файлы отсутствуют: загрузка компаний не требуется."
            )

        # CommandError из импорта намеренно не перехватываем:
        # при ошибке seed_demo тоже завершится неуспешно.
        call_command(
            "import_financial_data",
            stdout=self.stdout,
            stderr=self.stderr,
        )

        if user_exists:
            self.stdout.write(
                f"Пользователь {username} уже существует; "
                "пароль и права не изменены."
            )
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Создан демопользователь: {username}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS("Подготовка демоданных завершена.")
        )

    def sync_companies(self):
        # Импортируем только при необходимости обращения к API.
        from tinkoff.tinkoff import get_shares

        shares = get_shares()

        created_count = 0
        updated_count = 0

        assets_dir = (
            Path(settings.BASE_DIR)
            / "static"
            / "attached_assets"
        )

        for share in shares:
            logo_files = list(
                assets_dir.glob(f"{share.ticker}_*.png")
            )

            if logo_files:
                logo_path = f"attached_assets/{logo_files[0].name}"
            else:
                logo_path = None

            company, created = Company.objects.update_or_create(
                tinkoff_uid=share.uid,
                defaults={
                    "ticker": share.ticker,
                    "name": share.name,
                    "sector": share.sector or None,
                    "logo_color": share.brand.logo_base_color,
                    "logo_path": logo_path,
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(f"Получено из T-Invest: {len(shares)}")
        self.stdout.write(f"Создано компаний: {created_count}")
        self.stdout.write(f"Обновлено компаний: {updated_count}")