import snowflake.connector


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

    def fetch_overdue_payments(self) -> list[tuple]:
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
            return cursor.fetchall()
