import uvloop
from tortoise.contrib.fastapi import register_tortoise

from kitapi.v1 import api
from kitapi.core import settings


uvloop.install()


app = api.app

register_tortoise(
    app, generate_schemas=True, add_exception_handlers=True, config=settings.tortoise_config()
)
