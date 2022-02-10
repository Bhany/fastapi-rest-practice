from sqlalchemy.orm import Session

def commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)