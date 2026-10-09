from .services import get_analyst_forecasts


def build_analyst_forecasts(company):
    forecasts = get_analyst_forecasts(company)

    return [
        {
            "analyst_group": forecast.analyst_group,
            "recommendation": forecast.recommendation,
            "target_price": forecast.target_price,
        }
        for forecast in forecasts
    ]