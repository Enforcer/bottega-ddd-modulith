from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from used_stuff_market.orders.address import Address


VALID_INPUT = {
    "line_1": "Privet Drive 4",
    "line_2": None,
    "postal_code": "12345",
    "city": "Little Whinging",
    "country_code": "PL",
}


def test_address_can_be_created_with_complete_data() -> None:
    try:
        Address(**VALID_INPUT)  # type: ignore
    except ValueError:
        pytest.fail("Address creation failed")


def test_addresses_created_from_equal_values_are_considered_equal() -> None:
    address_1 = Address(**VALID_INPUT)  # type: ignore
    address_2 = Address(**VALID_INPUT)  # type: ignore

    assert address_1 == address_2


@pytest.mark.parametrize("field", VALID_INPUT.keys())
def test_address_cannot_be_mutated_after_creation(field: str) -> None:
    address = Address(**VALID_INPUT)  # type: ignore

    with pytest.raises(FrozenInstanceError):
        setattr(address, field, VALID_INPUT[field])


@pytest.mark.parametrize(
    "data_change",
    [
        pytest.param({"line_1": ""}, id="empty line_1"),
        pytest.param({"line_2": ""}, id="empty line_2"),
        pytest.param({"postal_code": ""}, id="empty postal_code"),
        pytest.param({"postal_code": "123"}, id="postal_code too short"),
        pytest.param({"postal_code": "66666666"}, id="postal_code too long"),
        pytest.param({"postal_code": "12XD3"}, id="malformed postal_code"),
        pytest.param({"city": ""}, id="empty city"),
        pytest.param({"country_code": ""}, id="empty country_code"),
        pytest.param({"country_code": "GB"}, id="other country_code"),
    ],
)
def test_address_fail_validation_for_invalid_data(data_change: dict[str, Any]) -> None:
    data = {**VALID_INPUT, **data_change}

    with pytest.raises(ValueError):
        Address(**data)
