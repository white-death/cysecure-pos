from fastapi import FastAPI

# Database
from app.db.init_db import init_db

# Routes
from app.api.routes import admin
from app.api.routes.resources import router as resource_router

app = FastAPI(
    title="CySecure POS Backend",
    version="1.0.0"
)


# Create tables on startup
@app.on_event("startup")
def on_startup():
    init_db()


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "POS Backend Running 🚀"
    }


# Admin routes
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"]
)


# Resource routes
app.include_router(
    resource_router
)
