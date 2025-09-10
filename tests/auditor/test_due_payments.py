from datetime import datetime
from unittest import mock

from auditor import due_payments
from auditor.snowflake_gateway import SnowflakeGateway
from prometheus_client import Metric
from time_machine import travel


@travel("2015-01-01 01:00:00")
def test_due_payments() -> None:
    with mock.patch("snowflake.connector.connect") as mock_snowflake_conn:
        cursor_mock = mock.MagicMock()
        cursor_mock.return_value.__enter__.return_value.fetchall.return_value = [
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
        ]
        mock_snowflake_conn.return_value.cursor.side_effect = cursor_mock

        checker = due_payments.DuePaymentsChecker(
            SnowflakeGateway(
                username="testuser",
                password="password",
                account="testaccount",
                region="eu-central-1",
                database="testdatabase",
                warehouse="default",
            ),
            prometheus_host_port="prometheus:9090",
        )
    with mock.patch.object(due_payments, "push_to_gateway") as mock_push_to_gateway:
        checker.check()

    mock_push_to_gateway.assert_called_once()
    call = mock_push_to_gateway.mock_calls[0]
    assert call.kwargs["gateway"] == "prometheus:9090"
    assert call.kwargs["job"] == "Due Payments"
    registry = call.kwargs["registry"]
    metrics_by_name = {metric.name: metric for metric in registry.collect()}
    assert (
        _get_value_from_metrics(metrics_by_name["failed_payments_within_last_2_days"])
        == 45.0
    )
    assert (
        _get_value_from_metrics(metrics_by_name["failed_payments_by_top_user"]) == 30.0
    )
    assert (
        _get_value_from_metrics(metrics_by_name["due_payments_last_check_unixtime"])
        == 1420070400.0
    )


def _get_value_from_metrics(metric: Metric) -> float:
    samples = metric.samples
    assert len(samples) == 1
    return samples[0].value
