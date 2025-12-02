from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import reviews as controller
from ..schemas import review_schema as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags = ['Reviews'],
    prefix = '/reviews'
)

@router.get("/", response_model=list[schema.Review])
def get_all_reviews(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Review)
def get_one_review(item_id, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.post("/", response_model=schema.Review)
def create_review(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(request=request, db=db)

@router.put("/{item_id}", response_model=schema.Review)
def update_review(item_id, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete_review(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

