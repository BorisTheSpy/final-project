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
def get_all_reviews(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.User)
def get_one_review(item_id, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.post("/", response_model=list[schema.User])
def create_review(request: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.create(request=request, db=db)

@router.put("/{item_id}", response_model=schema.User)
def update_review(item_id, request: schema.UserUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete_review(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)