from . import orders, order_details, sandwiches, users, reviews


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(sandwiches.router)
    app.include_router(users.router)
    app.include_router(reviews.router)
