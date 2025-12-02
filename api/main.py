from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import hashlib

# Import your models
from api.models.user import User
from api.models.orders import Order
from api.models.order_details import OrderDetail
from api.models.sandwiches import Sandwich
from api.models.recipes import Recipe
from api.models.resources import Resource
from api.models.review import Review
from api.models.promo import Promo
from api.models.payment import Payment
from api.dependencies.database import get_db, engine
from api.models import model_loader

app = FastAPI(title="Sandwich Shop API")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    model_loader.index()

# Helper functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id: int) -> str:
    return f"token_{user_id}_{datetime.now().timestamp()}"

# --- PYDANTIC MODELS (for API requests/responses) ---

class UserCreate(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    password: str
    role: str = "Customer"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: Optional[str]
    address: Optional[str]
    role: str
    token: str

class OrderDetailCreate(BaseModel):
    sandwich_id: int
    amount: int

class OrderCreate(BaseModel):
    user_id: int
    customer_name: str
    description: Optional[str] = None
    order_details: List[OrderDetailCreate]

class ReviewCreate(BaseModel):
    user_id: int
    order_id: Optional[int] = None
    rating: int
    comment: str

class PromoCreate(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str
    value: float
    is_active: int = 1

# --- ENDPOINTS ---

@app.get("/")
def root():
    return {"message": "Sandwich Shop API is running!"}

# USER ENDPOINTS
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        address=user.address,
        password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        phone_number=db_user.phone_number,
        address=db_user.address,
        role=db_user.role,
        token=generate_token(db_user.id)
    )

@app.post("/users/login", response_model=UserResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or user.password != hash_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        address=user.address,
        role=user.role,
        token=generate_token(user.id)
    )

@app.put("/users/{user_id}")
def update_user(user_id: int, updates: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in updates.items():
        if hasattr(user, key) and key not in ['password', 'id', 'email']:
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

# SANDWICH ENDPOINTS
@app.get("/sandwiches")
def get_sandwiches(db: Session = Depends(get_db)):
    sandwiches = db.query(Sandwich).all()
    return sandwiches

@app.get("/sandwiches/{sandwich_id}")
def get_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

# ORDER ENDPOINTS
@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(
        user_id=order.user_id,
        customer_name=order.customer_name,
        description=order.description,
        order_date=datetime.now(),
        status="Placed"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for detail in order.order_details:
        db_detail = OrderDetail(
            order_id=db_order.id,
            sandwich_id=detail.sandwich_id,
            amount=detail.amount
        )
        db.add(db_detail)
    
    db.commit()
    return {"id": db_order.id, "message": "Order created successfully"}

@app.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

@app.get("/orders/user/{user_id}")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

@app.put("/orders/{order_id}")
def update_order(order_id: int, updates: dict, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for key, value in updates.items():
        if hasattr(order, key):
            setattr(order, key, value)
    
    db.commit()
    return {"message": "Order updated successfully"}

# REVIEW ENDPOINTS
@app.post("/reviews")
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(
        user_id=review.user_id,
        order_id=review.order_id,
        rating=review.rating,
        comment=review.comment,
        review_date=datetime.now()
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return {"id": db_review.id, "message": "Review submitted"}

@app.get("/reviews")
def get_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).order_by(Review.review_date.desc()).all()
    return reviews

@app.get("/reviews/user/{user_id}")
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.user_id == user_id).all()
    return reviews

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}

# PROMO ENDPOINTS
@app.post("/promos")
def create_promo(promo: PromoCreate, db: Session = Depends(get_db)):
    db_promo = Promo(
        code=promo.code,
        description=promo.description,
        discount_type=promo.discount_type,
        value=promo.value,
        is_active=promo.is_active
    )
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)
    return {"id": db_promo.id, "message": "Promo created"}

@app.get("/promos")
def get_all_promos(db: Session = Depends(get_db)):
    return db.query(Promo).all()

@app.get("/promos/active")
def get_active_promos(db: Session = Depends(get_db)):
    return db.query(Promo).filter(Promo.is_active == 1).all()

@app.put("/promos/{promo_id}")
def update_promo(promo_id: int, updates: dict, db: Session = Depends(get_db)):
    promo = db.query(Promo).filter(Promo.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    
    for key, value in updates.items():
        if hasattr(promo, key):
            setattr(promo, key, value)
    
    db.commit()
    return {"message": "Promo updated"}

@app.delete("/promos/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    promo = db.query(Promo).filter(Promo.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    db.delete(promo)
    db.commit()
    return {"message": "Promo deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)