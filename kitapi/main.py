from fastapi import FastAPI

from kitapi import v1


app = FastAPI()
app.include_router(v1.fact.router)
