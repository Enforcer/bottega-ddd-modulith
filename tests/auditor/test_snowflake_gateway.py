from datetime import datetime
from unittest import mock

import pytest

from used_stuff_market.auditor.snowflake_gateway import SnowflakeGateway


@pytest.mark.parametrize(
    "rows",
    [
        [
            (
                "90d9a448-9555-41bf-a983-76bf5ffb74e3",
                datetime(2020, 1, 1, 12, 10, 30),
                1,
                datetime(2020, 1, 1, 12, 11, 30),
                20,
                "USD",
            ),
        ],
        [
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
    ],
)
def test_returns_raw_rows_from_snowflake(rows: list[tuple]) -> None:
    with mock.patch("snowflake.connector.connect") as mock_snowflake_conn:
        cursor_mock = mock.MagicMock()
        cursor_mock.return_value.__enter__.return_value.fetchall.return_value = rows
        mock_snowflake_conn.return_value.cursor.side_effect = cursor_mock

        gateway = SnowflakeGateway(
            username="testuser",
            password="password",
            account="testaccount",
            region="eu-central-1",
            database="testdatabase",
            warehouse="default",
        )

        overdue_payments = gateway.fetch_overdue_payments()

        assert overdue_payments == rows
