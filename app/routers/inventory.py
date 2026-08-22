from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.product import Product


router = APIRouter()


@router.put("/inventory/{product_id}/stock-in")
def stock_in(product_id: int, count: int):
    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="محصول موردنظر یافت نشد"
        )

    if count <= 0:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="مقدار افزایش باید بیشتر از صفر باشد"
        )

    product.stock += count

    db.commit()
    db.refresh(product)
    db.close()

    return {
        "message": "موجودی با موفقیت افزایش یافت",
        "product_id": product_id,
        "stock": product.stock
    }
@router.put("/inventory/{product_id}/stock-out")
def stock_out(product_id: int, count: int):
    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="محصول موردنظر یافت نشد"
        )

    if count <= 0:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="مقدار کاهش باید بیشتر از صفر باشد"
        )

    if count > product.stock:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="موجودی کافی نیست"
        )

    product.stock -= count

    db.commit()
    db.refresh(product)
    db.close()

    return {
        "message": "موجودی با موفقیت کاهش یافت",
        "product_id": product_id,
        "stock": product.stock
    }


@router.get("/inventory/{product_id}/stock")
def check_stock(product_id: int):
    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="محصول موردنظر یافت نشد"
        )

    stock = product.stock

    db.close()

    return {
        "product_id": product_id,
        "stock": stock
    }