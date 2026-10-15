from decimal import Decimal


CENT = Decimal("0.01")


class DistributionError(ValueError):
    pass


def _validate_unique_participants(participant_ids: list[int]) -> None:
    if not participant_ids:
        raise DistributionError("La distribución requiere al menos una persona")
    if len(participant_ids) != len(set(participant_ids)):
        raise DistributionError("La distribución no admite personas repetidas")


def distribute_expense(
    *,
    amount: Decimal,
    expense_type: str,
    person_id: int | None = None,
    participant_ids: list[int] | None = None,
    custom_allocations: list[tuple[int, Decimal]] | None = None,
) -> list[tuple[int, Decimal]]:
    if amount <= 0:
        raise DistributionError("El monto total debe ser mayor que cero")
    if amount.quantize(CENT) != amount:
        raise DistributionError("El monto total admite como máximo dos decimales")

    if expense_type == "personal":
        if person_id is None:
            raise DistributionError("El gasto personal requiere una persona asignada")
        if participant_ids is not None or custom_allocations is not None:
            raise DistributionError("La distribución no corresponde al tipo personal")
        return [(person_id, amount)]

    if expense_type == "equal":
        if participant_ids is None:
            raise DistributionError("La división equitativa requiere participantes")
        if person_id is not None or custom_allocations is not None:
            raise DistributionError("La distribución no corresponde al tipo equitativo")
        _validate_unique_participants(participant_ids)

        total_cents = int(amount / CENT)
        base_cents, remaining_cents = divmod(total_cents, len(participant_ids))
        return [
            (
                participant_id,
                Decimal(base_cents + (index < remaining_cents)) * CENT,
            )
            for index, participant_id in enumerate(participant_ids)
        ]

    if expense_type == "custom":
        if custom_allocations is None:
            raise DistributionError("La división personalizada requiere partes")
        if person_id is not None or participant_ids is not None:
            raise DistributionError("La distribución no corresponde al tipo personalizado")
        _validate_unique_participants(
            [participant_id for participant_id, _ in custom_allocations]
        )
        if any(allocated_amount < 0 for _, allocated_amount in custom_allocations):
            raise DistributionError("Las partes personalizadas no admiten importes negativos")
        if any(
            allocated_amount.quantize(CENT) != allocated_amount
            for _, allocated_amount in custom_allocations
        ):
            raise DistributionError("Las partes admiten como máximo dos decimales")
        if sum(
            (allocated_amount for _, allocated_amount in custom_allocations),
            start=Decimal("0.00"),
        ) != amount:
            raise DistributionError(
                "Las partes personalizadas deben sumar exactamente el monto total"
            )
        return custom_allocations

    raise DistributionError("Tipo de gasto inválido")


def calculate_debts(
    *,
    payer_id: int,
    allocations: list[tuple[int, Decimal]],
) -> list[tuple[int, Decimal]]:
    return [
        (participant_id, amount)
        for participant_id, amount in allocations
        if participant_id != payer_id and amount > 0
    ]
