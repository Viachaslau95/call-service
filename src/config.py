from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = '.env'

class Postgres(BaseSettings):
    name: str = 'call-service-db'
    username: str = 'postgres'
    password: str = 'postgres'
    host: str = 'localhost'
    port: int = 5445
    test_name: str = 'test'


class Config(BaseSettings):
    allowed_origins: list[str] = ['http://localhost:3000', 'http://127.0.0.1:3000']
    debug: bool = True
    api_port: int = 8880
    api_host: str = 'localhost'
    version: str = '0.1.0'
    service_name: str = 'call-service'
    base_url: str = 'http://127.0.0.1:8880'
    backend_url: str = 'http://127.0.0.1:8000'
    postgres: Postgres = Postgres()

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')


config = Config()