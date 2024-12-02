from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    db_username: str = ""
    db_password: str = ""
    db_host: str = ""
    db_port: int = 5432
    db_name: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


db_settings = DBSettings()
