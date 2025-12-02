from . import orders, order_details, recipes, sandwiches, resources
from . import user, payment, review, promo
from ..dependencies.database import engine, Base


def index():
    # Import all models to register them with Base.metadata
    # All models use the same Base instance from database.py
    Base.metadata.create_all(engine)
