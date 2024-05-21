from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkersSettings(BaseSettings):
    URL: RedisDsn = Field(default="redis://localhost:6379/0")
    model_config = SettingsConfigDict(env_prefix="CONFIG_DB_")
