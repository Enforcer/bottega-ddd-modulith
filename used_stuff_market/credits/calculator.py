from decimal import Decimal

from used_stuff_market.credits import scorings
from used_stuff_market.credits.employment_type import EmploymentType
from used_stuff_market.shared_kernel.money import Money


def calculate_lending_capacity(
    net_income: Money,
    total_credits_card_limit: Money,
    cost_of_living: Money,
    number_of_people_in_household: int,
    employment_type: EmploymentType,
) -> Money:
    score = (
        0
        + scorings.for_net_income(net_income)
        + scorings.for_credits_card_limit(total_credits_card_limit)
        + scorings.for_cost_of_living(cost_of_living)
        + scorings.for_number_of_people(number_of_people_in_household)
        + scorings.for_employment_type(employment_type)
    )
    if score <= 0:
        return Money(net_income.currency, 0)

    amount = round(net_income.amount * Decimal(score / 10.0), 2)
    return Money(net_income.currency, amount)
