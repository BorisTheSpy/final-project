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

def create(db: Session, request):
    db_user = model.User(
        name=request.name,
        phone_number=request.phone_number,
        address=request.address,
        email=request.email,
        role=request.user_role,
        password=request.password

    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return db_user