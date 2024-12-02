from fastapi import FastAPI
from src.router import router as scheduler_router
from models import Base
from database import engine

app = FastAPI()


Base.metadata.create_all(bind=engine)


@app.get("/hello")
def read_root():
    return {"status": "server ok"}


app.include_router(scheduler_router)
