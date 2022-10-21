from pydantic import BaseSettings, Field, RedisDsn


class WorkersSettings(BaseSettings):
    URL: RedisDsn = Field(default="redis://localhost:6379/0")

    class Config:
        env_prefix = "CONFIG_DB_"
