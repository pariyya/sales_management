#module for create new product with some itributes by admin,
#if the product already exists server response http error
#update an existing product without creating a new object
#update the stock of an existing product
#delete a product by its id
#display all orders

from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.product import Product
from app.models.order import Order
from app.models.user import User
from app.models.customer import Customer
from app.schemas.product import ProductCreateSchema


router = APIRouter()

@router.post("/_new_product")
def create_product(
    data: ProductCreateSchema,
    admin_id: int
):

    db = SessionLocal()
    admin = db.query(User).filter(
            User.id == admin_id
        ).first()

    if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin user not found"
            )

    if admin.role != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

    product = db.query(Product).filter(
            Product.name == data.name
        ).first()

    if product:
            raise HTTPException(
                status_code=409,
                detail="محصولی با این نام از قبل وجود دارد"
            )
            
    product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            category=data.category,
            stock=data.stock,
            is_active=data.is_active
        )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product
    db.close()

@router.put("/_update_product/{product_id}")
def update_product(
    product_id: int,
    data: ProductCreateSchema,
    admin_id: int
):

    db = SessionLocal()
    admin = db.query(User).filter(
            User.id == admin_id
        ).first()

    if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin user not found"
            )

    if admin.role != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )
    product = db.query(Product).filter(
            Product.id == product_id
        ).first()

    if not product:
            raise HTTPException(
                status_code=404,
                detail="محصول موردنظر یافت نشد"
            )

    product.name = data.name
    product.description = data.description
    product.price = data.price
    product.category = data.category
    product.stock = data.stock
    product.is_active = data.is_active

    db.commit()
    db.refresh(product)

    return {
            "message": f"محصول {product.name} به‌روزرسانی شد"
        }
    db.close()

@router.delete("/_delete_product/{product_id}")
def delete_product(
    product_id: int,
    admin_id: int
):

    db = SessionLocal()

    admin = db.query(User).filter(
            User.id == admin_id
        ).first()

    if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin user not found"
            )

    if admin.role != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )
    product = db.query(Product).filter(
            Product.id == product_id
        ).first()

    if not product:
            raise HTTPException(
                status_code=404,
                detail="محصول موردنظر یافت نشد"
            )

    db.delete(product)
    db.commit()

    return {
            "message": f"محصول {product_id} حذف شد"
        }
    db.close()

@router.put("/_update_product_stock/{product_id}")
def update_stock(
    product_id: int,
    new_stock: int,
    admin_id: int
):

    db = SessionLocal()
    admin = db.query(User).filter(
            User.id == admin_id
        ).first()

    if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin user not found"
            )

    if admin.role != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

    if new_stock < 0:
            raise HTTPException(
                status_code=400,
                detail="مقدار موجودی نمی‌تواند منفی باشد"
            )
    product = db.query(Product).filter(
            Product.id == product_id
        ).first()

    if not product:
            raise HTTPException(
                status_code=404,
                detail="محصول موردنظر یافت نشد"
            )

    product.stock = new_stock
    db.commit()
    db.refresh(product)

    return {
            "message": f"موجودی محصول {product_id} تغییر کرد"
        }
    db.close()

@router.get("/_display_orders")
def display_orders(admin_id: int):

    db = SessionLocal()
    admin = db.query(User).filter(
            User.id == admin_id
        ).first()

    if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin user not found"
            )

    if admin.role != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

    orders = db.query(Order).all()

    return orders
    db.close() 

@router.get("/display_user")
def get_users(admin_id: int):

    db = SessionLocal()

    admin = db.query(User).filter(
            User.id == admin_id
        ).first()

    if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin user not found"
            )

    if admin.role != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

    users = db.query(User).all()

    return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
            for user in users
        ]

    db.close()

@router.delete("/_delete_customer_/{customer_id}")
def delete_customer(
    customer_id: int,
    admin_id: int
):

    db = SessionLocal()
    admin = db.query(User).filter(
            User.id == admin_id
        ).first()

    if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin user not found"
            )

    if admin.role != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

    customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

    if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

    db.delete(customer)
    db.commit()

    return {
            "message": "Customer deleted successfully"
        }
    db.close()
@router.delete("/_delete_user_/{user_id}/{admin_id}")
def delete_user(user_id: int, admin_id: int):

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

    if user_id == admin_id:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete himself"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # اگر این User مشتری هم باشد، مشتری‌اش را حذف کن
    customer = db.query(Customer).filter(
        Customer.email == user.email
    ).first()

    if customer:
        db.delete(customer)

    # حذف User
    db.delete(user)

    db.commit()
    db.close()

    return {
        "message": "User and related customer deleted successfully"
    }