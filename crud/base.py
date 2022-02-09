from fastapi import HTTPException
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import uuid

def _commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
