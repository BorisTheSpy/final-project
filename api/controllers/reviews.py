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

def read_one(db: Session, item_id):
    try:
        item = db.query(model.Review).filter(model.Review.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

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

def update(db: Session, request, item_id):
    try:
        item = db.query(model.Review).filter(model.Review.id == item_id)

        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, item_id):
    try:
        item = db.query(model.Review).filter(model.Review.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)