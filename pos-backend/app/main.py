from fastapi import FastAPI
from app.api.routes import auth, admin
from app.db.init_db import init_db

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/")
def root():
    return {"message": "POS Backend Running 🚀"}
