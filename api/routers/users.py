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

@router.get("/{item_id}", response_model=schema.User)
def read_one(item_id, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.post("/", response_model=schema.User)
def create(request: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.create(request=request, db=db)

@router.put("/{item_id}", response_model=schema.User)
def update(item_id, request: schema.UserUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)