from .services import get_income_chart_data


INCOME_SERIES = [
    {
        "key": "revenue",
        "label": "Выручка",
    },
    {
        "key": "cost_of_revenue",
        "label": "Себестоимость",
    },
    {
        "key": "gross_profit",
        "label": "Валовая прибыль",
    },
    {
        "key": "operating_profit",
        "label": "Операционная прибыль",
    },
    {
        "key": "ebitda",
        "label": "EBITDA",
    },
    {
        "key": "net_income",
        "label": "Чистая прибыль",
    },
]


def build_income_chart(company, mode="FY"):
    data = get_income_chart_data(
        company,
        mode,
    )

    return {
        "series": INCOME_SERIES,
        "data": data,
    }