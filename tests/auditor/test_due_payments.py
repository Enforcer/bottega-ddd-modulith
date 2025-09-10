from datetime import datetime
from unittest.mock import Mock, seal

from auditor.due_payments import DuePaymentsChecker
from auditor.prometheus_gateway import PrometheusGateway
from auditor.snowflake_gateway import OverduePayment, SnowflakeGateway
from time_machine import travel


class SnowflakeGatewayStub(SnowflakeGateway):
    """Stubs can be implemented manually, e.g. by subclassing. or using Mocks."""

    def __init__(self, payments: list[OverduePayment]) -> None:
        self._payments = payments

    def fetch_overdue_payments(self) -> list[OverduePayment]:
        return self._payments


@travel("2015-01-01 01:00:00")
def test_due_payments() -> None:
    snowflake_gateway_stub = Mock(
        spec_set=SnowflakeGateway,
        fetch_overdue_payments=Mock(
            return_value=[
                OverduePayment(
                    uuid="90d9a448-9555-41bf-a983-76bf5ffb74e3",
                    when_created=datetime(2020, 1, 1, 12, 10, 30),
                    user_id=1,
                    when_payment_started=datetime(2020, 1, 1, 12, 11, 30),
                    amount=20,
                    currency="USD",
                ),
                OverduePayment(
                    uuid="90d9a448-9555-41bf-a983-76bf5ffb74e3",
                    when_created=datetime(2020, 1, 1, 12, 10, 30),
                    user_id=1,
                    when_payment_started=datetime(2020, 1, 1, 12, 11, 30),
                    amount=10,
                    currency="USD",
                ),
                OverduePayment(
                    uuid="90d9a448-9555-41bf-a983-76bf5ffb74e3",
                    when_created=datetime(2020, 1, 1, 12, 10, 30),
                    user_id=2,
                    when_payment_started=datetime(2020, 1, 1, 12, 11, 30),
                    amount=15,
                    currency="USD",
                ),
            ]
        ),
    )
    seal(snowflake_gateway_stub)
    prometheus_gateway_mock = Mock(spec_set=PrometheusGateway)

    checker = DuePaymentsChecker(
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
