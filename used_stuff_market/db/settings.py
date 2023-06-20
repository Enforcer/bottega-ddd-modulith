from pydantic import BaseSettings, Field, PostgresDsn


class DbSettings(BaseSettings):
    URL: PostgresDsn = Field(
        default=(
            "postgresql://used_stuff_market:used_stuff_market"
            "@127.0.0.1:5432/used_stuff_market"
        )
    )

    class Config:
        env_prefix = "CONFIG_DB_"
