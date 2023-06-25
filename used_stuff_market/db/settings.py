from pydantic import BaseSettings, Field, MongoDsn, PostgresDsn


class DbSettings(BaseSettings):
    URL: PostgresDsn = Field(
        default=(
            "postgresql://used_stuff_market:used_stuff_market"
            "@127.0.0.1:5432/used_stuff_market"
        )
    )
    MONGO_URL: MongoDsn = Field(
        default="mongodb://used_stuff_market:used_stuff_market@localhost:27017"
    )
    MONGO_DB: str = Field(default="used_stuff_market")

    class Config:
        env_prefix = "CONFIG_DB_"
