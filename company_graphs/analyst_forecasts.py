from .services import get_analyst_forecasts


def build_analyst_forecasts(company):
    forecasts = get_analyst_forecasts(company)

    result = []

    for forecast in forecasts:
        item = {
        "analyst_group": forecast.analyst_group,
        "recommendation": forecast.recommendation,
        "target_price": forecast.target_price,
        }
        result.append(item)

    return result