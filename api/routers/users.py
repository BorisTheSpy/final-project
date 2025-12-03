from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import user as controller
from ..schemas import user_schema as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags = ['Users'],
    prefix = '/users'
)

@router.get("/", response_model=list[schema.User])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.post("/login", response_model=schema.LoginResponse)
def login(request: schema.LoginRequest, db: Session = Depends(get_db)):
    user = controller.login(db=db, email=request.email, password=request.password)
    # Create LoginResponse by manually converting SQLAlchemy model to dict
    # This avoids the model_validate issue with SQLAlchemy instances
    user_dict = {
        "id": user.id,
        "name": user.name,
        "phone_number": user.phone_number,
        "address": user.address,
        "email": user.email,
        "role": user.role,
        "token": str(user.id)
    }
    return schema.LoginResponse(**user_dict)

@router.get("/{item_id}", response_model=schema.User)
def read_one(item_id, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.post("/", response_model=list[schema.User])
def create(request: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.create(request=request, db=db)

@router.put("/{item_id}", response_model=schema.User)
def update(item_id, request: schema.UserUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)