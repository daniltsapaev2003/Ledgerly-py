from django.http import JsonResponse

from companies.models import Company
from company_graphs.income import build_income_chart
from company_graphs.balance import build_balance_chart
from company_graphs.cash_flow import build_cash_flow_chart
from companies.models import (
    FinancialReport,
    AnalystForecast,
)

def income_chart_data(request, company_id):
    company = Company.objects.filter(
        id=company_id,
        is_active=True,
    ).first()

    if not company:
        return JsonResponse(
            {"error": "Company not found"},
            status=404,
        )

    mode = request.GET.get(
        "mode",
        "FY",
    )

    chart = build_income_chart(
        company,
        mode,
    )

    return JsonResponse(chart)

def balance_chart_data(request, company_id):
    company = Company.objects.filter(
        id=company_id,
        is_active=True,
    ).first()

    if not company:
        return JsonResponse(
            {"error": "Company not found"},
            status=404,
        )

    mode = request.GET.get(
        "mode",
        "FY",
    )

    chart = build_balance_chart(
        company,
        mode,
    )

    return JsonResponse(chart)

def cash_flow_chart_data(request, company_id):
    company = Company.objects.filter(
        id=company_id,
        is_active=True,
    ).first()

    if not company:
        return JsonResponse(
            {"error": "Company not found"},
            status=404,
        )

    mode = request.GET.get(
        "mode",
        "FY",
    )

    chart = build_cash_flow_chart(
        company,
        mode,
    )

    return JsonResponse(chart)

def get_analyst_forecasts(company):
    forecasts = AnalystForecast.objects.filter(
        company=company,
    ).order_by(
        "analyst_group",
    )

    return forecasts