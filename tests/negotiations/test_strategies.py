import pytest

from used_stuff_market.negotiations.strategies import (
    FiveDollarsLimit,
    FivePercentLimit,
    NegotiationStrategy,
)
from used_stuff_market.shared_kernel.money import Currency, Money


@pytest.mark.parametrize(
    "new_offer",
    [Money(Currency.from_code("USD"), "10.5"), Money(Currency.from_code("USD"), "9.5")],
)
def test_five_percent_in_range_not_raising_exception(new_offer: Money) -> None:
    strategy = FivePercentLimit()
    try:
        strategy.validate_offer(
            current_offer=Money(Currency.from_code("USD"), "10"),
            new_offer=new_offer,
        )
    except Exception:
        pytest.fail("Should not raise exception!")


@pytest.mark.parametrize(
    "new_offer",
    [
        Money(Currency.from_code("USD"), "10.51"),
        Money(Currency.from_code("USD"), "9.49"),
    ],
)
def test_five_percent_out_of_range_raising_exception(new_offer: Money) -> None:
    strategy = FivePercentLimit()
    with pytest.raises(NegotiationStrategy.PriceNotAllowed):
        strategy.validate_offer(
            current_offer=Money(Currency.from_code("USD"), "10"),
            new_offer=new_offer,
        )


@pytest.mark.parametrize(
    "new_offer",
    [Money(Currency.from_code("USD"), "15"), Money(Currency.from_code("USD"), "5")],
)
def test_five_dollars_in_range_not_raising_exception(new_offer: Money) -> None:
    strategy = FiveDollarsLimit()
    try:
        strategy.validate_offer(
            current_offer=Money(Currency.from_code("USD"), "10"),
            new_offer=new_offer,
        )
    except Exception:
        pytest.fail("Should not raise exception!")


@pytest.mark.parametrize(
    "new_offer",
    [
        Money(Currency.from_code("USD"), "15.01"),
        Money(Currency.from_code("USD"), "4.99"),
    ],
)
def test_five_dollars_out_of_range_raising_exception(new_offer: Money) -> None:
    strategy = FiveDollarsLimit()
    with pytest.raises(NegotiationStrategy.PriceNotAllowed):
        strategy.validate_offer(
            current_offer=Money(Currency.from_code("USD"), "10"),
            new_offer=new_offer,
        )
