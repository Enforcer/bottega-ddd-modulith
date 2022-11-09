from datetime import datetime
from unittest import mock

from freezegun import freeze_time

from used_stuff_market.auditor import due_payments
from used_stuff_market.auditor.prometheus_gateway import PrometheusGateway
from used_stuff_market.auditor.snowflake_gateway import SnowflakeGateway


class SnowflakeGatewayStub(SnowflakeGateway):
    """Stubs can be implemented manually, e.g. by subclassing."""

    def __init__(self, rows_to_return: list[tuple]) -> None:
        self._rows_to_return = rows_to_return

    def fetch_overdue_payments(self) -> list[tuple]:
        return self._rows_to_return


@freeze_time("2015-01-01")
def test_due_payments() -> None:
    snowflake_gateway_stub = mock.Mock(
        spec_set=SnowflakeGateway,
        fetch_overdue_payments=mock.Mock(
            return_value=[
                (
                    "90d9a448-9555-41bf-a983-76bf5ffb74e3",
                    datetime(2020, 1, 1, 12, 10, 30),
                    1,
                    datetime(2020, 1, 1, 12, 11, 30),
                    20,
                    "USD",
                ),
                (
                    "90d9a448-9555-41bf-a983-76bf5ffb74e3",
                    datetime(2020, 1, 1, 12, 10, 30),
                    1,
                    datetime(2020, 1, 1, 12, 11, 30),
                    10,
                    "USD",
                ),
                (
                    "90d9a448-9555-41bf-a983-76bf5ffb74e3",
                    datetime(2020, 1, 1, 12, 10, 30),
                    2,
                    datetime(2020, 1, 1, 12, 11, 30),
                    15,
                    "USD",
                ),
            ],
        ),
    )

    prometheus_gateway_mock = mock.Mock(spec_set=PrometheusGateway)
    checker = due_payments.DuePaymentsChecker(
        snowflake_gateway=snowflake_gateway_stub,
        prometheus_gateway=prometheus_gateway_mock,
    )

    checker.check()

    prometheus_gateway_mock.push_metrics.assert_called_once_with(
        job="Due Payments",
        metrics=[
            PrometheusGateway.Metric(
                name="due_payments_last_check_unixtime",
                description="Last time a check successfully finished",
                value=1420070400.0,
            ),
            PrometheusGateway.Metric(
                name="failed_payments_within_last_2_days",
                description="Amount of money that were not paid despite reservation within last 2 days",
                value=45.0,
            ),
            PrometheusGateway.Metric(
                name="failed_payments_by_top_user",
                description="Amount of money that were not paid by the largest offending user within last 2 days",
                value=30.0,
            ),
        ],
    )
