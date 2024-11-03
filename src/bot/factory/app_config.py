from ..app_config import AppConfig, CommonConfig, PostgresConfig, RedisConfig


def create_app_config() -> AppConfig:
    return AppConfig(
        common=CommonConfig(),
        postgres=PostgresConfig(),
        redis=RedisConfig(),
    )
