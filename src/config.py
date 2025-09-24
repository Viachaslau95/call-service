from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = '.env'


class Postgres(BaseSettings):
    name: str = 'call-service-db'
    username: str = 'postgres'
    password: str = 'postgres'
    host: str = 'localhost'
    port: int = 5445
    test_name: str = 'test'

    @property
    def base_uri(self) -> str:
        return f'{self.user_host}/{self.name}'

    @property
    def user_host(self) -> str:
        user_info = f'{self.username}:{self.password}'
        host_info = f'{self.host}:{self.port}'
        return f'{user_info}@{host_info}'

    @property
    def uri(self) -> str:
        return f'postgresql+asyncpg://{self.base_uri}'

    @property
    def test_uri(self) -> str:
        test_uri = f'{self.user_host}/{self.test_name}'
        return f'postgresql+asyncpg://{test_uri}'

    @property
    def test_sync_uri(self) -> str:
        test_uri = f'{self.user_host}/{self.test_name}'
        return f'postgresql://{test_uri}'

    @property
    def sync_uri(self) -> str:
        return f'postgresql://{self.base_uri}'


class Celery(BaseSettings):
    broker_url: str = 'redis://localhost:6379/0'
    result_backend: str = 'redis://localhost:6379/0'
    task_always_eager: bool = False
    model_config = SettingsConfigDict(env_prefix='celery_', env_file=ENV_FILE, extra='ignore')


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
    celery: Celery = Celery()
    recordings_dir: str = './recordings'

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')


config = Config()