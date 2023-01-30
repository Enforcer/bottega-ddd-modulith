from used_stuff_market.credits.employment_type import EmploymentType
from used_stuff_market.shared_kernel.money import Money


def for_net_income(net_income: Money) -> int:
    if net_income.amount < 2_000:
        return -100
    elif net_income.amount < 3_500:
        return 100
    elif net_income.amount < 5_000:
        return 200
    elif net_income.amount < 10_000:
        return 500
    else:
        return 1000


def for_credits_card_limit(limit: Money) -> int:
    if limit.amount == 0:
        return 100
    elif limit.amount < 5_000:
        return 50
    elif limit.amount < 10_000:
        return 0
    else:
        return -100


def for_cost_of_living(cost: Money) -> int:
    if cost.amount < 500:
        return -100
    elif cost.amount < 1000:
        return 100
    elif cost.amount < 2000:
        return 75
    elif cost.amount < 4000:
        return 25
    elif cost.amount < 5000:
        return 0
    else:
        return -100


def for_number_of_people(number: Money) -> int:
    if number == 1:
        return 50
    elif number == 2:
        return 100
    elif number < 4:
        return 75
    elif number < 5:
        return 50
    elif number < 6:
        return 0
    elif number < 10:
        return -100
    else:
        return -1000


def for_employment_type(employment_type: EmploymentType) -> None:
    if employment_type == EmploymentType.CONTRACT_OF_EMPLOYMENT:
        return 100
    elif employment_type == EmploymentType.SELF_EMPLOYMENT:
        return 50
    elif employment_type == EmploymentType.UNEMPLOYED:
        return -1000
