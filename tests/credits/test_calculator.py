from used_stuff_market.credits.calculator import calculate_lending_capacity
from used_stuff_market.credits.employment_type import EmploymentType
from used_stuff_market.shared_kernel.money import USD, Money


def test_calculations() -> None:
    lending_capacity = calculate_lending_capacity(
        net_income=Money(USD, 1000),
        total_credits_card_limit=Money(USD, 500),
        cost_of_living=Money(USD, 800),
        number_of_people_in_household=3,
        employment_type=EmploymentType.CONTRACT_OF_EMPLOYMENT,
    )

    assert lending_capacity == Money(USD, 22500)
