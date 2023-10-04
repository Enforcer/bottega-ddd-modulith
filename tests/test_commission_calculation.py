from dataclasses import dataclass
from decimal import Decimal

from hypothesis import given, strategies

from used_stuff_market.shared_kernel.money import USD, Money

# See decimal strategy to generate numbers
# https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.decimals


def test_calculate_commission_loses_no_money() -> None:
    price = Money(USD, "100")
    amount = 1

    result = calculate_commission(
        price=price,
        amount=amount,
        sell_commission=Decimal("0.2"),
    )

    value_without_commission = Money(USD, round(price.amount * amount, 2))
    commission = Money(USD, 0)
    total_money_before = value_without_commission + commission
    total_money_after = result.payout + result.commission_for_platform
    assert total_money_before == total_money_after


@dataclass(frozen=True)
class Result:
    payout: Money
    commission_for_platform: Money


def calculate_commission(
    price: Money,
    amount: int,
    sell_commission: Decimal,
) -> Result:
    payout = round(price.amount * amount, 2)
    actual_payout = Money(USD, (Decimal(1) - sell_commission) * payout)
    commission = Money(USD, payout * sell_commission)
    return Result(payout=actual_payout, commission_for_platform=commission)
