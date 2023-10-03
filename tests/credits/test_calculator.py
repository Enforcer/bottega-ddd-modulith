import pytest

from used_stuff_market.credits.calculator import calculate_lending_capacity
from used_stuff_market.credits.employment_type import EmploymentType
from used_stuff_market.shared_kernel.money import USD, Money


@pytest.mark.parametrize(
    "net_income, total_credits_card_limit, cost_of_living, "
    "number_of_people_in_household, employment_type, result",
    [
        (
            Money(USD, 1000),
            Money(USD, 500),
            Money(USD, 800),
            3,
            EmploymentType.CONTRACT_OF_EMPLOYMENT,
            Money(USD, 225_00),
        ),
        (
            Money(USD, 8000),
            Money(USD, 0),
            Money(USD, 3000),
            3,
            EmploymentType.SELF_EMPLOYMENT,
            Money(USD, 600_000),
        ),
        (
            Money(USD, 3000),
            Money(USD, 1000),
            Money(USD, 500),
            1,
            EmploymentType.SELF_EMPLOYMENT,
            Money(USD, 105_000),
        )
    ],
)
def test_calculations_lending_capacity_for_eligible_people(
    net_income,
    total_credits_card_limit,
    cost_of_living,
    number_of_people_in_household,
    employment_type,
    result,
) -> None:
    lending_capacity = calculate_lending_capacity(
        net_income=net_income,
        total_credits_card_limit=total_credits_card_limit,
        cost_of_living=cost_of_living,
        number_of_people_in_household=number_of_people_in_household,
        employment_type=employment_type,
    )

    assert lending_capacity == result


@pytest.mark.parametrize(
    "net_income, total_credits_card_limit, cost_of_living, "
    "number_of_people_in_household, employment_type, result",
    [
        (
            Money(USD, 0),
            Money(USD, 0),
            Money(USD, 500),
            1,
            EmploymentType.UNEMPLOYED,
            Money(USD, 0),
        ),
        (
            Money(USD, 1000),
            Money(USD, 1000),
            Money(USD, 3000),
            7,
            EmploymentType.UNEMPLOYED,
            Money(USD, 0),
        ),
    ],
)
def test_calculations_lending_capacity_for_ineligible_people(
    net_income,
    total_credits_card_limit,
    cost_of_living,
    number_of_people_in_household,
    employment_type,
    result,
) -> None:
    lending_capacity = calculate_lending_capacity(
        net_income=net_income,
        total_credits_card_limit=total_credits_card_limit,
        cost_of_living=cost_of_living,
        number_of_people_in_household=number_of_people_in_household,
        employment_type=employment_type,
    )

    assert lending_capacity == result
