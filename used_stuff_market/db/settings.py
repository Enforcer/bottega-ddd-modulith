from pydantic import BaseSettings, Field, PostgresDsn


class DbSettings(BaseSettings):
    URL: str = Field(
        default=(
            "postgresql://used_stuff_market:used_stuff_market"
            "@localhost:5432/used_stuff_market"
        )
    )

    class Config:
        env_prefix = "CONFIG_DB_"
