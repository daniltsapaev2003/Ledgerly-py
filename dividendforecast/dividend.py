from datetime import date

from companies.models import Dividend


def get_dividends(company):

    dividends = (
    Dividend.objects
    .filter(company=company)
    .order_by("-year", "-period")[:5]
    )

    result = []

    for dividend in dividends:
        if dividend.payment_date:
            is_paid = dividend.payment_date <= date.today()
        else:
            is_paid = False

        result.append(
            {
                "year": dividend.year,
                "period": dividend.period,
                "amount": dividend.amount,
                "payment_date": dividend.payment_date,
                "is_paid": is_paid,
            }
        )

    return result


def build_dividend_table(company):

    dividends = get_dividends(company)

    rows = []

    for dividend in dividends:
        period = dividend["period"]

        if period == "FY":
         label = f"Дивиденд за {dividend['year']}"
        else:
         label = f"Дивиденд за {dividend['year']} {period}"

        rows.append(
            {
                "year": dividend["year"],
                "period": period,
                "label": label,
                "amount": dividend["amount"],
                "payment_date": dividend["payment_date"],
                "is_paid": dividend["is_paid"],
            }
        )

    return rows