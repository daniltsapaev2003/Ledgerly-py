import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from companies.models import Company


companies = Company.objects.all().order_by("ticker")

for company in companies:
    print(f"{company.ticker} | {company.name}")