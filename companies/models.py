from django.db import models

class Company(models.Model):
    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    logo_color = models.CharField(max_length=7)
    logo_path = models.CharField(max_length=255, blank=True, null=True)
    tinkoff_uid = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FinancialReport(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="financial_reports"
    )

    year = models.PositiveIntegerField()

    period = models.CharField(
        max_length=10,
        choices=[
            ("FY", "Full Year"),
            ("Q1", "Q1"),
            ("Q2", "Q2"),
            ("Q3", "Q3"),
            ("Q4", "Q4"),
        ],
        default="FY"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "year", "period"],
                name="unique_company_year_period"
            )
        ]

    def __str__(self):
        return f"{self.company.ticker} — {self.year} — {self.period}"


class IncomeStatement(models.Model):

    report = models.OneToOneField(
        FinancialReport,
        on_delete=models.CASCADE,
        related_name="income_statement"
    )

    revenue = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    cost_of_revenue = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    gross_profit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    operating_profit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    ebitda = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    net_income = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Income Statement — {self.report}"


class BalanceSheet(models.Model):

    report = models.OneToOneField(
        FinancialReport,
        on_delete=models.CASCADE,
        related_name="balance_sheet"
    )

    cash_and_equivalents = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_assets = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    current_liabilities = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_liabilities = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    equity = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Balance Sheet — {self.report}"

class CashFlowStatement(models.Model):

    report = models.OneToOneField(
        FinancialReport,
        on_delete=models.CASCADE,
        related_name="cash_flow_statement"
    )

    operating_cash_flow = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    investing_cash_flow = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    financing_cash_flow = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    capital_expenditures = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    free_cash_flow = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Cash Flow Statement — {self.report}"

class Dividend(models.Model):
    PERIOD_CHOICES = [
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
        ("FY", "Full Year"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="dividends",
    )

    year = models.PositiveIntegerField()

    period = models.CharField(
        max_length=2,
        choices=PERIOD_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    payment_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "year", "period"],
                name="unique_company_dividend_period",
            )
        ]

    def __str__(self):
        return f"{self.company.ticker} — {self.year} — {self.period}"