from datetime import datetime
from typing import TypedDict

import snowflake.connector


class OverduePayment(TypedDict):
    uuid: str
    when_created: datetime
    user_id: int
    when_payment_started: datetime
    amount: int
    currency: str


class SnowflakeGateway:
    def __init__(
        self,
        username: str,
        password: str,
        account: str,
        region: str,
        database: str,
        warehouse: str,
    ) -> None:
        self.ctx = snowflake.connector.connect(
            user=username,
            password=password,
            account=f"{account}.{region}",
            warehouse=warehouse,
            database=database,
        )

    def fetch_overdue_payments(self) -> list[OverduePayment]:
        with self.ctx.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    event_uuid,
                    when_created,
                    user_id,
                    when_payment_started,
                    amount,
                    currency
                FROM payments
                WHERE
                    when_payment_started > CURRENT_TIMESTAMP - INTERVAL '2 days'
            """
            )
            rows = cursor.fetchall()
            return [
                OverduePayment(
                    uuid=row[0],
                    when_created=row[1],
                    user_id=row[2],
                    when_payment_started=row[3],
                    amount=row[4],
                    currency=row[5],
                )
                for row in rows
            ]
