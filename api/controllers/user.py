from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import user as model
from sqlalchemy.exc import SQLAlchemyError

def read_all(db: Session):
    try:
        result = db.query(model.User).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

def create(db: Session, user):
    db_user = model.User(
        rating=user.rating,
        comment=user.comment
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user