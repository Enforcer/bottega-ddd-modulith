from decimal import Decimal

import pytest

from used_stuff_market.negotiations.price_diff_policies import (
    NoLimits,
    NoMoreThan10USD,
    NoMoreThan30Percent,
)


def test_no_limits() -> None:
    policy = NoLimits()

    try:
        policy.validate(old_price=Decimal("10"), new_price=Decimal("20"))
    except ValueError:
        pytest.fail("Should pass")


def test_no_more_than_10_usd_passes_with_10() -> None:
    policy = NoMoreThan10USD()

    try:
        policy.validate(old_price=Decimal("10"), new_price=Decimal("20"))
    except ValueError:
        pytest.fail("Should pass")


def test_no_more_than_10_usd_fails_with_11() -> None:
    policy = NoMoreThan10USD()

    with pytest.raises(ValueError):
        policy.validate(old_price=Decimal("10"), new_price=Decimal("21"))


def test_no_more_than_30_percent_passes_with_30_percent() -> None:
    policy = NoMoreThan30Percent()

    try:
        policy.validate(old_price=Decimal("10"), new_price=Decimal("13"))
    except ValueError:
        pytest.fail("Should pass")


def test_no_more_than_30_percent_fails_with_31_percent() -> None:
    policy = NoMoreThan30Percent()

    with pytest.raises(ValueError):
        policy.validate(old_price=Decimal("10"), new_price=Decimal("13.1"))
