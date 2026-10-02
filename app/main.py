# app/main.py
from fastapi import FastAPI
from app.api.router import router
from app.database import engine, Base

# Create the database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meeting Minutes Engine")

app.include_router(router, prefix="/api")