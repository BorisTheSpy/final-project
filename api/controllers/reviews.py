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

def create(db: Session, request):
    db_review = model.Review(
        rating=request.rating,
        comment=request.comment,
        user_id=request.user_id,
        order_id=request.order_id
    )

    try:
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return db_review