import abc

import snowflake.connector


class Checker(abc.ABC):
    def __init__(
        self,
        snowflake_username: str,
        snowflake_password: str,
        snowflake_account: str,
        snowflake_region: str,
        snowflake_database: str,
        snowflake_warehouse: str,
        prometheus_host_port: str,
    ) -> None:
        self.ctx = snowflake.connector.connect(
            user=snowflake_username,
            password=snowflake_password,
            account=f"{snowflake_account}.{snowflake_region}",
            warehouse=snowflake_warehouse,
            database=snowflake_database,
        )
        self.prometheus_host_port = prometheus_host_port

    @abc.abstractmethod
    def check(self) -> None:
        pass
