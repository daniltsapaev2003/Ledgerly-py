from companies.models import FinancialReport


def get_income_chart_data(company, mode="FY"):
    reports = FinancialReport.objects.filter(
        company=company,
    ).select_related(
        "income_statement",
    )

    if mode == "FY":
        reports = reports.filter(
        period="FY",
        ).order_by("-year")[:5]
        reports = reversed(reports)

    elif mode == "Q":
        reports = reports.filter(
            period__in=["Q1", "Q2", "Q3", "Q4"],
        ).order_by(
            "year",
            "period",
        )

        years = list(
            reports.values_list(
                "year",
                flat=True,
            ).distinct()
        )

        years = years[-3:]

        reports = reports.filter(
            year__in=years,
        )

    else:
        return []

    result = []

    for report in reports:

        income = getattr(
            report,
            "income_statement",
            None,
        )

        if not income:
            continue

        if mode == "FY":
            label = str(report.year)
        else:
            label = f"{report.year} {report.period}"

        result.append(
            {
                "label": label,
                "year": report.year,
                "period": report.period,

                "revenue": income.revenue,
                "cost_of_revenue": income.cost_of_revenue,
                "gross_profit": income.gross_profit,
                "operating_profit": income.operating_profit,
                "ebitda": income.ebitda,
                "net_income": income.net_income,
            }
        )

    return result

def get_balance_chart_data(company, mode="FY"):
    reports = FinancialReport.objects.filter(
        company=company,
    ).select_related(
        "balance_sheet",
    )

    if mode == "FY":
        reports = list(
            reports.filter(
                period="FY",
            ).order_by("-year")[:5]
        )

        reports.reverse()

    elif mode == "Q":
        reports = reports.filter(
            period__in=["Q1", "Q2", "Q3", "Q4"],
        ).order_by(
            "year",
            "period",
        )

        years = list(
            reports.values_list(
                "year",
                flat=True,
            ).distinct()
        )

        years = years[-3:]

        reports = reports.filter(
            year__in=years,
        )

    else:
        return []

    result = []

    for report in reports:
        balance = getattr(
            report,
            "balance_sheet",
            None,
        )

        if not balance:
            continue

        if mode == "FY":
            label = str(report.year)
        else:
            label = f"{report.year} {report.period}"

        result.append(
            {
                "label": label,
                "year": report.year,
                "period": report.period,
                "cash_and_equivalents": balance.cash_and_equivalents,
                "total_assets": balance.total_assets,
                "current_liabilities": balance.current_liabilities,
                "total_liabilities": balance.total_liabilities,
                "total_debt": balance.total_debt,
                "equity": balance.equity,
            }
        )

    return result

def get_cash_flow_chart_data(company, mode="FY"):
    reports = FinancialReport.objects.filter(
        company=company,
    ).select_related(
        "cash_flow_statement",
    )

    if mode == "FY":
        reports = list(
            reports.filter(
                period="FY",
            ).order_by("-year")[:5]
        )

        reports.reverse()

    elif mode == "Q":
        reports = reports.filter(
            period__in=["Q1", "Q2", "Q3", "Q4"],
        ).order_by(
            "year",
            "period",
        )

        years = list(
            reports.values_list(
                "year",
                flat=True,
            ).distinct()
        )

        years = years[-3:]

        reports = reports.filter(
            year__in=years,
        )

    else:
        return []

    result = []

    for report in reports:
        cash_flow = getattr(
            report,
            "cash_flow_statement",
            None,
        )

        if not cash_flow:
            continue

        if mode == "FY":
            label = str(report.year)
        else:
            label = f"{report.year} {report.period}"

        result.append(
        {
        "label": label,
        "year": report.year,
        "period": report.period,
        "operating_cash_flow": cash_flow.operating_cash_flow,
        "investing_cash_flow": cash_flow.investing_cash_flow,
        "financing_cash_flow": cash_flow.financing_cash_flow,
        "capital_expenditures": cash_flow.capital_expenditures,
        "free_cash_flow": cash_flow.free_cash_flow,
        }
)

    return result