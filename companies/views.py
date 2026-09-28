from django.shortcuts import render

from companies.models import Company


def dashboard(request):
    companies = Company.objects.filter(
        is_active=True
    ).order_by("ticker")

    return render(
        request,
        "dashboard.html",
        {"companies": companies},
    )