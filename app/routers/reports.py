# this module handles sales and inventory reports
# show total orders
# calculate total sales price
#only admin can access to this session

from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.order import Order
from app.models.user import User

router = APIRouter()


@router.get("/reports/sales/{admin_id}")
def sales_report(admin_id: int):

    db = SessionLocal()

    admin = db.query(User).filter(
        User.id == admin_id
    ).first()

    if not admin:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Admin user not found"
        )

    if admin.role != "ADMIN":
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    total_orders = db.query(Order).count()

    total_sales = sum(
        order.total_price
        for order in db.query(Order).all()
    )

    db.close()

    return {
        "total_orders": total_orders,
        "total_sales": total_sales
    }