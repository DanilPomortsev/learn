from pydantic import BaseSettings

#класс базовых настроек
class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    data_base_host: str = '127.0.0.1'
    data_base_user_name: str = 'root'
    data_base_name: str = 'mongodb_new'
    jwt_secret: str = "mXyTW_HqbY4-S21rb0W8HgdTnwWvUe7HMpwtzkDJxZ8" 'HS256'
    jwt_algoritm: str = 'HS256'
    jwt_expiration: int = 3600



settings_ = Settings(
    _env_file='_env',
    _env_file_encoding='utf-8'
)