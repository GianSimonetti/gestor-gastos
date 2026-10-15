from decimal import Decimal

import pytest

from app.expense_distribution import (
    DistributionError,
    calculate_debts,
    distribute_expense,
)


def test_equal_distribution_splits_amount_exactly():
    allocations = distribute_expense(
        amount=Decimal("30000.00"),
        expense_type="equal",
        participant_ids=[3, 7],
    )

    assert allocations == [
        (3, Decimal("15000.00")),
        (7, Decimal("15000.00")),
    ]


def test_equal_distribution_assigns_remaining_cents_in_input_order():
    first = distribute_expense(
        amount=Decimal("100.00"),
        expense_type="equal",
        participant_ids=[8, 2, 5],
    )
    second = distribute_expense(
        amount=Decimal("100.00"),
        expense_type="equal",
        participant_ids=[8, 2, 5],
    )

    expected = [
        (8, Decimal("33.34")),
        (2, Decimal("33.33")),
        (5, Decimal("33.33")),
    ]
    assert first == expected
    assert second == expected
    assert sum(amount for _, amount in first) == Decimal("100.00")


def test_custom_distribution_preserves_decimal_amounts():
    allocations = distribute_expense(
        amount=Decimal("150000.00"),
        expense_type="custom",
        custom_allocations=[
            (4, Decimal("40000.00")),
            (9, Decimal("110000.00")),
        ],
    )

    assert allocations == [
        (4, Decimal("40000.00")),
        (9, Decimal("110000.00")),
    ]


@pytest.mark.parametrize(
    ("allocations", "message"),
    [
        ([(1, Decimal("150000.01"))], "sumar exactamente"),
        (
            [(1, Decimal("150000.00")), (2, Decimal("-0.01"))],
            "negativos",
        ),
    ],
)
def test_custom_distribution_rejects_invalid_amounts(allocations, message):
    with pytest.raises(DistributionError, match=message):
        distribute_expense(
            amount=Decimal("150000.00"),
            expense_type="custom",
            custom_allocations=allocations,
        )


def test_distribution_rejects_duplicate_or_missing_participants():
    with pytest.raises(DistributionError, match="repetidas"):
        distribute_expense(
            amount=Decimal("10.00"),
            expense_type="equal",
            participant_ids=[1, 1],
        )

    with pytest.raises(DistributionError, match="al menos una"):
        distribute_expense(
            amount=Decimal("10.00"),
            expense_type="equal",
            participant_ids=[],
        )


def test_debts_include_only_non_payers_with_a_positive_share():
    debts = calculate_debts(
        payer_id=4,
        allocations=[
            (4, Decimal("40.00")),
            (9, Decimal("60.00")),
            (12, Decimal("0.00")),
        ],
    )

    assert debts == [(9, Decimal("60.00"))]
