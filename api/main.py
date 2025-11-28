import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from .schemas import review_schema
from .controllers import orders, order_details, reviews
from .dependencies.database import get_db
from sqlalchemy.orm import Session


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)

@app.get("/reviews", response_model=list[review_schema.Review], tags=["Review"])
def get_all_reviews(db: Session = Depends(get_db)):
    return reviews.read_all(db)

@app.post("/review", response_model=list[review_schema.Review], tags=["Review"])
def create_review(review: review_schema.ReviewCreate, db: Session = Depends(get_db)):
    return reviews.create(review=review, db=db)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)