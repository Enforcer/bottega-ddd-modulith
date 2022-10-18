from pydantic import BaseSettings, PostgresDsn


class DbSettings(BaseSettings):
    URL: PostgresDsn = (
        "postgresql://used_stuff_market:used_stuff_market"
        "@localhost:5432/used_stuff_market"
    )

    class Config:
        env_prefix = "CONFIG_DB_"
