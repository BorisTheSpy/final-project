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

@router.post("/", response_model=schema.Review)
def create_review(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(request=request, db=db)