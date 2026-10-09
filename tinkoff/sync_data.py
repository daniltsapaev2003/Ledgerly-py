import os
import sys
from pathlib import Path
from datetime import datetime
import django


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "static" / "financial_data"
FORECASTS_DIR = BASE_DIR / "static" / "forecasts"

sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from companies.models import (
    Company,
    FinancialReport,
    IncomeStatement,
    BalanceSheet,
    CashFlowStatement,
    Dividend,
    AnalystForecast,
)
DIVIDEND_FIELDS = {
    "dividend",
    "payment_date",
}

INCOME_FIELDS = {
    "revenue",
    "cost_of_revenue",
    "gross_profit",
    "operating_profit",
    "ebitda",
    "net_income",
}

BALANCE_FIELDS = {
    "cash_and_equivalents",
    "total_assets",
    "current_liabilities",
    "total_liabilities",
    "total_debt",
    "equity",
}

CASH_FLOW_FIELDS = {
    "operating_cash_flow",
    "investing_cash_flow",
    "financing_cash_flow",
    "capital_expenditures",
    "free_cash_flow",
}


def parse_filename(file_path):
    parts = file_path.stem.split("_")

    if len(parts) != 3:
        raise ValueError(
            f"Неверное имя файла: {file_path.name}. "
            "Ожидается TICKER_YEAR_PERIOD.txt"
        )

    ticker, year, period = parts

    if period not in {"FY", "Q1", "Q2", "Q3", "Q4"}:
        raise ValueError(
            f"{file_path.name}: неизвестный период {period}"
        )

    return ticker.upper(), int(year), period


def parse_file(file_path):
    data = {}

    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            if "=" not in line:
                raise ValueError(
                    f"{file_path.name}, строка {line_number}: "
                    "ожидается формат key=value"
                )

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            if key not in (
                 INCOME_FIELDS
                 | BALANCE_FIELDS
                 | CASH_FLOW_FIELDS
                 | DIVIDEND_FIELDS
                ):
                raise ValueError(
                    f"{file_path.name}, строка {line_number}: "
                    f"неизвестное поле {key}"
                )

            data[key] = value

    return data

def sync_file(file_path):
    ticker, year, period = parse_filename(file_path)
    data = parse_file(file_path)

    company = Company.objects.filter(
        ticker=ticker,
        is_active=True,
    ).first()

    if not company:
        print(
            f"SKIP: компания {ticker} не найдена в базе"
        )
        return

    report, created = FinancialReport.objects.update_or_create(
        company=company,
        year=year,
        period=period,
        defaults={},
    )

    IncomeStatement.objects.update_or_create(
        report=report,
        defaults={
            field: data[field]
            for field in INCOME_FIELDS
            if field in data
        },
    )

    BalanceSheet.objects.update_or_create(
        report=report,
        defaults={
            field: data[field]
            for field in BALANCE_FIELDS
            if field in data
        },
    )

    CashFlowStatement.objects.update_or_create(
        report=report,
        defaults={
            field: data[field]
            for field in CASH_FLOW_FIELDS
            if field in data
        },
    )


    if "dividend" in data:
      Dividend.objects.update_or_create(
        company=company,
        year=year,
        period=period,
        defaults={
            "amount": data["dividend"],
            "payment_date": (
                datetime.strptime(
                    data["payment_date"],
                    "%d.%m.%Y",
                ).date()
                if "payment_date" in data
                else None
            ),
        },
      )

    if created:
        action = "создан"
    else:
        action = "обновлён"

    print(
        f"OK: {ticker} — {year} — {period} ({action})"
    )

def sync_forecast_file(file_path):
    ticker = file_path.stem.upper()

    company = Company.objects.filter(
        ticker=ticker,
        is_active=True,
    ).first()

    if not company:
        print(
            f"SKIP: компания {ticker} не найдена в базе"
        )
        return

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1,
        ):
            line = line.strip()

            if not line:
                continue

            parts = [
                part.strip()
                for part in line.split("=")
            ]

            if len(parts) != 3:
                raise ValueError(
                    f"{file_path.name}, строка {line_number}: "
                    "ожидается формат GROUP=RECOMMENDATION=PRICE"
                )

            analyst_group, recommendation, target_price = parts

            if recommendation not in {
                "BUY",
                "HOLD",
                "SELL",
            }:
                raise ValueError(
                    f"{file_path.name}, строка {line_number}: "
                    f"неизвестная рекомендация {recommendation}"
                )

            AnalystForecast.objects.update_or_create(
                company=company,
                analyst_group=analyst_group,
                defaults={
                    "recommendation": recommendation,
                    "target_price": target_price,
                },
            )

            print(
                f"FORECAST: {ticker} — "
                f"{analyst_group} — "
                f"{recommendation} — "
                f"{target_price}"
            )

def main():
    files = sorted(DATA_DIR.glob("*.txt"))

    print(f"Папка: {DATA_DIR}")
    print(f"Найдено файлов: {len(files)}")
    print()

    for file_path in files:
        try:
            sync_file(file_path)

        except Exception as error:
            print(
                f"ERROR: {file_path.name}: {error}"
            )
        forecast_files = sorted(
        FORECASTS_DIR.glob("*.txt")
    )

    print()
    print(f"Папка: {FORECASTS_DIR}")
    print(
        f"Найдено файлов прогнозов: "
        f"{len(forecast_files)}"
    )
    print()

    for file_path in forecast_files:
        try:
            sync_forecast_file(file_path)

        except Exception as error:
            print(
                f"ERROR: {file_path.name}: {error}"
            )


if __name__ == "__main__":
    main()