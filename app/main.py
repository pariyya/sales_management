from fastapi import FastAPI
from app.database.database import Base, engine
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.customer import Customer
from app.routers import product
from app.routers import auth
from app.routers import admin
from app.routers import customer
from app.routers import inventory
from app.routers import order


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sales Management API",
    description="API for sales management system",
    version="1.0.0"
)


app.include_router(product.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(customer.router)
app.include_router(inventory.router)
app.include_router(order.router)

if __name__ == "__main":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000
    )