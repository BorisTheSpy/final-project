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

@router.post("/", response_model=list[schema.User], tags=["Review"])
def create_review(user: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.create(user=user, db=db)