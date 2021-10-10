import typing
from os import environ

from dotenv import load_dotenv

__all__: list[str] = [
    "tortoise_config",
]

load_dotenv()


def tortoise_config() -> dict[str, dict[str, typing.Any]]:
    return {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "database": environ.get("DB_NAME"),
                    "host": environ.get("DB_HOST"),
                    "password": environ.get("DB_PASS"),
                    "port": environ.get("DB_PORT"),
                    "user": environ.get("DB_USER"),
                },
            }
        },
        "apps": {
            "models": {
                "models": ["kitapi.core.models"],
                "default_connection": "default",
            }
        },
    }
