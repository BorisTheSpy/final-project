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

def read_one(db: Session, item_id):
    try:
        item = db.query(model.User).filter(model.User.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def login(db: Session, email: str, password: str):
    try:
        user = db.query(model.User).filter(model.User.email == email).first()
        if not user or user.password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        return user
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

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

def update(db: Session, request, item_id):
    try:
        item = db.query(model.User).filter(model.User.id == item_id)

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
        item = db.query(model.User).filter(model.User.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)