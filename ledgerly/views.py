from django.shortcuts import render, redirect
from .models import User
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.hashers import check_password
from companies.models import Company, FinancialReport
from ledgerly.models import User
from django.http import JsonResponse
from dividendforecast.dividend import build_dividend_table
from company_graphs.income import build_income_chart
from company_graphs.balance import build_balance_chart
from company_graphs.cash_flow import build_cash_flow_chart

def registration(request):
    if request.method == "POST":
        try:
                User.objects.create(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                phone_number=request.POST["phone_number"],
                password=make_password(request.POST["password"])
                )
                request.session["session"] =  User.objects.filter(email = request.POST["email"]).first().id
                return redirect("Dashboard")

        except IntegrityError:
            return render(
                request,
                "Loginpage.html",
                {"user_exists": True}
            )

    return 0

def CheckUser(request):
    user_data = User.objects.filter(email = request.POST["email"])
    password = request.POST["password"]
    if user_data.exists():
         if check_password(password,user_data.first().password):
              request.session["session"] = user_data.first().id
              return redirect("Dashboard")
    return render(
                    request,
                    "Loginpage.html",
                    {"wrong_email_password": True}
                )   


def dashboard_protect(request):
    if "session" in request.session:
        companies = Company.objects.filter(
        is_active=True
        ).order_by("ticker")

        user = User.objects.get(
        id=request.session["session"]
        )

        return render(
        request,
        "Dashboard.html",
        {
            "companies": companies,
            "user": user,
        },
    )

    return redirect("Loginpage")

def logout(request):
    request.session.flush()

    return redirect("Loginpage")


def company_price(request, company_id):
    if "session" not in request.session:
        return JsonResponse(
            {"error": "Unauthorized"},
            status=401,
        )

    company = Company.objects.filter(
        id=company_id,
        is_active=True,
    ).first()

    if not company:
        return JsonResponse(
            {"error": "Company not found"},
            status=404,
        )

    from tinkoff.tinkoff import get_last_price

    price = get_last_price(company.tinkoff_uid)

    return render(
    request,
    "Company_price.html",
    {
        "price": price,
        "company_id": company_id,
    },
)

from decimal import Decimal


def calculate_change(current, previous):
    if current is None or previous is None:
        return None

    current = Decimal(current)
    previous = Decimal(previous)

    if previous == 0:
        return None

    return (current - previous) / abs(previous) * Decimal("100")


def get_statement(report, related_name):
    if not report:
        return None

    try:
        return getattr(report, related_name)
    except Exception:
        return None


def build_changes(report, previous_report):
    if not report or not previous_report:
        return {}

    sections = {
        "income": "income_statement",
        "balance": "balance_sheet",
        "cash_flow": "cash_flow_statement",
    }

    fields = {
        "income": [
            "revenue",
            "cost_of_revenue",
            "gross_profit",
            "operating_profit",
            "ebitda",
            "net_income",
        ],
        "balance": [
            "cash_and_equivalents",
            "total_assets",
            "current_liabilities",
            "total_liabilities",
            "total_debt",
            "equity",
        ],
        "cash_flow": [
            "operating_cash_flow",
            "investing_cash_flow",
            "financing_cash_flow",
            "capital_expenditures",
            "free_cash_flow",
        ],
    }

    changes = {}

    for section, related_name in sections.items():
        current_data = get_statement(report, related_name)
        previous_data = get_statement(previous_report, related_name)

        changes[section] = {}

        for field in fields[section]:
            current_value = getattr(current_data, field, None)
            previous_value = getattr(previous_data, field, None)

            changes[section][field] = calculate_change(
                current_value,
                previous_value,
            )
    return changes


def company_panel(request, company_id):
    if "session" not in request.session:
        return JsonResponse(
            {"error": "Unauthorized"},
            status=401,
        )

    company = Company.objects.filter(
        id=company_id,
        is_active=True,
    ).first()

    if not company:
        return JsonResponse(
            {"error": "Company not found"},
            status=404,
        )
    
    dividends = build_dividend_table(company)
    year = request.GET.get("year")
    period = request.GET.get("period", "FY")

    periods = ["Q1", "Q2", "Q3", "Q4", "FY"]

    report = None
    previous_report = None
    changes = {}

    if year:
        year = int(year)

        report = FinancialReport.objects.filter(
            company=company,
            year=year,
            period=period,
        ).first()

        previous_report = FinancialReport.objects.filter(
            company=company,
            year=year - 1,
            period=period,
        ).first()

        changes = build_changes(
            report,
            previous_report,
        )

    chart_mode = request.GET.get("chart_mode", "FY")
    balance_chart = build_balance_chart(
        company,
        "FY",
    )
    income_chart = build_income_chart(
        company,
        chart_mode,
    )

    cash_flow_chart = build_cash_flow_chart(
        company,
        "FY",
    )

    return render(
        request,
        "Company_panel.html",
        {
            "company": company,
            "report": report,
            "previous_report": previous_report,
            "changes": changes,
            "year": year,
            "period": period,
            "years": range(2020, 2027),
            "periods": periods,
            "dividends": dividends,
            "income_chart": income_chart,
            "balance_chart": balance_chart,
            "cash_flow_chart": cash_flow_chart,
        },
    )