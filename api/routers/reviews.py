from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import reviews as controller
from ..schemas import review_schema as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags = ['Reviews'],
    prefix = '/reviews'
)

@router.get("/", response_model=list[schema.Review], tags=["Review"])
def get_all_reviews(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.post("/", response_model=list[schema.Review], tags=["Review"])
def create_review(review: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(review=review, db=db)