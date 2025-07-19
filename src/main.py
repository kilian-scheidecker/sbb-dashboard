from fastapi import FastAPI

from router import next_departure_router


app = FastAPI()

app.include_router(next_departure_router)

