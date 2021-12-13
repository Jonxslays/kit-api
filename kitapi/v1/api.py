from fastapi import FastAPI

from kitapi import __appdata__
from kitapi.v1.endpoints import FactRouter

app = FastAPI(**__appdata__)
app.include_router(FactRouter, prefix="/v1")
