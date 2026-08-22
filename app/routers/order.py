#this module handles orders,
#includ creating orders and changing order status
#define order status
#create order object
#check products availabilities and stock
#calculate total price as final  order price
#update the order status

from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.product import Product
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.schemas.order import OrderSchema
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


router = APIRouter()

@router.post("/orders")
def create_order(data: OrderSchema):

    db = SessionLocal()

    total_price = 0

    # بررسی محصولات
    for item in data.items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            db.close()
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if not product.is_active:
            db.close()
            raise HTTPException(
                status_code=400,
                detail="Product is not active"
            )

        if item.quantity > product.stock:
            db.close()
            raise HTTPException(
                status_code=400,
                detail="موجودی کافی نیست!"
            )

        item_total = product.price * item.quantity
        total_price += item_total

    # ساخت سفارش
    order = Order(
        customer_id=data.customer_id,
        total_price=total_price,
        status="PENDING",
        created_at=datetime.utcnow()
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # ساخت آیتم‌های سفارش
    for item in data.items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        item_total = product.price * item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            total_price=item_total
        )

        # کم کردن موجودی
        product.stock -= item.quantity

        db.add(order_item)

    # ذخیره تغییرات
    db.commit()

    # قبل از بستن دیتابیس ذخیره کن
    order_id = order.id
    final_total_price = order.total_price

    db.close()

    return {
        "message": "Order created successfully",
        "order_id": order_id,
        "total_price": final_total_price,
        "status": "PENDING"
    }