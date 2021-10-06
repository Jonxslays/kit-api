from fastapi import FastAPI

from kitapi import __appdata__

from .endpoints import FactRouter

app = FastAPI(**__appdata__)
app.include_router(FactRouter)
