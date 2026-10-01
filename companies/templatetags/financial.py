from decimal import Decimal

from django import template


register = template.Library()


@register.filter
def financial(value):
    if value is None:
        return "—"

    value = Decimal(value)

    absolute_value = abs(value)

    if absolute_value >= Decimal("1000000000"):
        result = value / Decimal("1000000000")
        return f"{result:.2f} млрд"

    if absolute_value >= Decimal("1000000"):
        result = value / Decimal("1000000")
        return f"{result:.2f} млн"

    if absolute_value >= Decimal("1000"):
        result = value / Decimal("1000")
        return f"{result:.2f} тыс."

    return f"{value:.2f}"