import os
import sys
from pathlib import Path

import django
from dotenv import load_dotenv
from django.conf import settings


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from companies.models import Company
from tinkoff.tinkoff import get_shares


load_dotenv()


def sync_companies():
    shares = get_shares()

    created_count = 0
    updated_count = 0

    for share in shares:
        assets_dir = (
            Path(settings.BASE_DIR)
            / "static"
            / "attached_assets"
        )

        logo_files = list(assets_dir.glob(f"{share.ticker}_*.png"))

        logo_path = (
            f"attached_assets/{logo_files[0].name}"
            if logo_files
            else None
        )

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

    print(f"Получено из T-Invest: {len(shares)}")
    print(f"Создано компаний: {created_count}")
    print(f"Обновлено компаний: {updated_count}")


if __name__ == "__main__":
    sync_companies()

