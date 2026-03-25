from app.db.base import Base
from app.db.session import engine

# VERY IMPORTANT: import models
from app.models import User
from app.models.refresh_token import RefreshToken

def init_db():
    Base.metadata.create_all(bind=engine)
