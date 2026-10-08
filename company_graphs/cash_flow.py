from .services import get_cash_flow_chart_data


CASH_FLOW_SERIES = [
    {
        "key": "operating_cash_flow",
        "label": "Операционный денежный поток",
    },
    {
        "key": "investing_cash_flow",
        "label": "Инвестиционный денежный поток",
    },
    {
        "key": "financing_cash_flow",
        "label": "Финансовый денежный поток",
    },
    {
        "key": "capital_expenditures",
        "label": "Капитальные затраты",
    },
    {
        "key": "free_cash_flow",
        "label": "Свободный денежный поток",
    },
]


def build_cash_flow_chart(company, mode="FY"):
    data = get_cash_flow_chart_data(
        company,
        mode,
    )

    return {
        "series": CASH_FLOW_SERIES,
        "data": data,
    }