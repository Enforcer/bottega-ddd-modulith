from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from used_stuff_market.auditor.check import Checker
from used_stuff_market.auditor.prometheus_gateway import PrometheusGateway
from used_stuff_market.auditor.snowflake_gateway import SnowflakeGateway


class DuePaymentsChecker(Checker):
    def __init__(
        self,
        snowflake_gateway: SnowflakeGateway,
        prometheus_gateway: PrometheusGateway,
    ) -> None:
        self._snowflake_gateway = snowflake_gateway
        self._prometheus_gateway = prometheus_gateway

    def check(self) -> None:
        rows = self._snowflake_gateway.fetch_overdue_payments()

        failed_payments_by_user = defaultdict(lambda: Decimal("0.0"))
        total_failed_payment = Decimal("0.0")
        for row in rows:
            total_failed_payment += row[4]
            failed_payments_by_user[row[2]] += row[4]

        sorted_payments_by_user = sorted(
            failed_payments_by_user.items(),
            key=lambda key_value: key_value[1],
            reverse=True,
        )
        try:
            user_with_biggest_due_payments_sum = sorted_payments_by_user[0]
        except IndexError:
            top_user = 0.0
        else:
            top_user = user_with_biggest_due_payments_sum[1]

        self._prometheus_gateway.push_metrics(
            job="Due Payments",
            metrics=[
                PrometheusGateway.Metric(
                    name="due_payments_last_check_unixtime",
                    description="Last time a check successfully finished",
                    value=datetime.now().timestamp(),
                ),
                PrometheusGateway.Metric(
                    name="failed_payments_within_last_2_days",
                    description="Amount of money that were not paid despite reservation within last 2 days",
                    value=float(total_failed_payment),
                ),
                PrometheusGateway.Metric(
                    name="failed_payments_by_top_user",
                    description="Amount of money that were not paid by the largest offending user within last 2 days",
                    value=float(top_user),
                ),
            ],
        )
