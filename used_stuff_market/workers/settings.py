from pydantic import BaseSettings, RedisDsn


class WorkersSettings(BaseSettings):
    URL: RedisDsn = "redis://localhost:6379/0"

    class Config:
        env_prefix = "CONFIG_DB_"
