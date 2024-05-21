from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    URL: PostgresDsn = Field(
        default=(
            "postgresql://used_stuff_market:used_stuff_market"
            "@127.0.0.1:5432/used_stuff_market"
        )
    )
    model_config = SettingsConfigDict(env_prefix="CONFIG_DB_")
