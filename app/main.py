import imp
from typing import Union
from fastapi import FastAPI
from app.auth.router import auth_router
from resizer.router import pdf_resizer_router
from db_config import engine, Base

app = FastAPI()


app.include_router(auth_router)
app.include_router(pdf_resizer_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)