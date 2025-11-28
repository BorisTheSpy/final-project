from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import review as model
from sqlalchemy.exc import SQLAlchemyError

def read_all(db: Session):
    try:
        result = db.query(model.Review).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

def create(db: Session, review):
    db_review = model.Review(
        rating=review.rating,
        comment=review.comment
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review