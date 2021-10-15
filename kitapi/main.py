import uvloop
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from tortoise.contrib.fastapi import register_tortoise

from kitapi.core import settings
from kitapi.v1 import api

uvloop.install()


app = api.app
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse("static/index.html")


register_tortoise(
    app, generate_schemas=True, add_exception_handlers=True, config=settings.tortoise_config()
)
