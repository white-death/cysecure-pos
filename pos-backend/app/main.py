from fastapi import FastAPI

# REQUIRED IMPORTS
from app.db.init_db import init_db
from app.api.routes import admin

app = FastAPI()


# Create tables on startup
@app.on_event("startup")
def on_startup():
    init_db()


# Register routes
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/")
def root():
    return {"message": "POS Backend Running 🚀"}
