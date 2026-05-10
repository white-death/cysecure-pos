from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


# DATABASE
from app.db.init_db import init_db


# ROUTES
from app.api.routes import admin

from app.api.routes.auth import router as auth_router

from app.api.routes.resources import (
    router as resource_router
)

from app.api.routes.customers import (
    router as customer_router
)

from app.api.routes.invoices import (
    router as invoice_router
)


app = FastAPI(
    title="CySecure POS Backend",
    version="1.0.0"
)


# CORS

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://192.168.0.119:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# STARTUP

@app.on_event("startup")
def on_startup():

    init_db()


# ROOT

@app.get("/")
def root():

    return {
        "message": "POS Backend Running 🚀"
    }


# ADMIN ROUTES

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"]
)


# RESOURCE ROUTES

app.include_router(
    resource_router
)


# CUSTOMER ROUTES

app.include_router(
    customer_router
)


# INVOICE ROUTES

app.include_router(
    invoice_router
)


# AUTH ROUTES

app.include_router(
    auth_router
)
