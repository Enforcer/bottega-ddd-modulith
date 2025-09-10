from collections import defaultdict
from decimal import Decimal

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from auditor.check import Checker
from auditor.snowflake_gateway import SnowflakeGateway


class DuePaymentsChecker(Checker):
    def __init__(
        self, snowflake_gateway: SnowflakeGateway, prometheus_host_port: str
    ) -> None:
        super().__init__(prometheus_host_port=prometheus_host_port)
        self._snowflake_gateway = snowflake_gateway

    def check(self) -> None:
        registry = CollectorRegistry()
        last_success = Gauge(
            "due_payments_last_check_unixtime",
            "Last time a check successfully finished",
            registry=registry,
        )
        last_success.set_to_current_time()
        failed_payments_sum_gauge = Gauge(
            "failed_payments_within_last_2_days",
            "Amount of money that were not paid despite reservation within last 2 days",
            registry=registry,
        )
        top_user = Gauge(
            "failed_payments_by_top_user",
            "Amount of money that were not paid by the largest offending user within last 2 days",
            registry=registry,
        )

        overdue_payments = self._snowflake_gateway.fetch_overdue_payments()

        failed_payments_by_user: dict[int, Decimal] = defaultdict(
            lambda: Decimal("0.0")
        )
        total_failed_payment = Decimal("0.0")
        for payment in overdue_payments:
            total_failed_payment += payment["amount"]
            failed_payments_by_user[payment["user_id"]] += payment["amount"]

        failed_payments_sum_gauge.set(float(total_failed_payment))
        sorted_payments_by_user = sorted(
            failed_payments_by_user.items(),
            key=lambda key_value: key_value[1],
            reverse=True,
        )
        try:
            user_with_biggest_due_payments_sum = sorted_payments_by_user[0]
        except IndexError:
            top_user.set(0.0)
        else:
            top_user.set(float(user_with_biggest_due_payments_sum[1]))

        push_to_gateway(
            gateway=self.prometheus_host_port, job="Due Payments", registry=registry
        )
