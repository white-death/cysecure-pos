from sqlalchemy.orm import declarative_base

# Base class for all models
Base = declarative_base()

# Import all models here for Alembic detection
from app.models.user import User
