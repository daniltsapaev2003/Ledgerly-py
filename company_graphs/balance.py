from .services import get_balance_chart_data


BALANCE_SERIES = [
    {
        "key": "cash_and_equivalents",
        "label": "Денежные средства",
    },
    {
        "key": "total_assets",
        "label": "Активы",
    },
    {
        "key": "current_liabilities",
        "label": "Текущие обязательства",
    },
    {
        "key": "total_liabilities",
        "label": "Обязательства",
    },
    {
        "key": "total_debt",
        "label": "Долг",
    },
    {
        "key": "equity",
        "label": "Капитал",
    },
]


def build_balance_chart(company, mode="FY"):
    data = get_balance_chart_data(
        company,
        mode,
    )

    return {
        "series": BALANCE_SERIES,
        "data": data,
    }