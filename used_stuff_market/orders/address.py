from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    line_1: str
    line_2: str | None
    postal_code: str
    city: str
    country_code: str

    def __post_init__(self) -> None:
        if not self.line_1:
            raise ValueError("line_1 must not be empty")

        if self.line_2 is not None and not self.line_2:
            raise ValueError("line_2 must be None or non-empty string")

        if len(self.postal_code) != 5:
            raise ValueError("postal_code must have 5 digits")

        if not self.postal_code.isdigit():
            raise ValueError("postal_code must have 4 digits")

        if not self.city:
            raise ValueError("city must not be empty")

        if not self.country_code:
            raise ValueError("country_code must not be empty")

        if self.country_code != "PL":
            raise ValueError("country_code must be PL")
