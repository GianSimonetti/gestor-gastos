from collections.abc import Iterable
from decimal import Decimal


def calculate_monthly_summary(
    *,
    available_base: Decimal,
    expense_totals: Iterable[Decimal],
) -> tuple[Decimal, Decimal]:
    consumed = sum(expense_totals, start=Decimal("0.00"))
    return consumed, available_base - consumed
