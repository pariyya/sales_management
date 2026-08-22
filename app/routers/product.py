#this module handles product display and search
#get product information
#search products
#filter products by category and price
#sort products

from fastapi import APIRouter
from app.database.database import SessionLocal
from app.models.product import Product

router = APIRouter()

@router.get("/_display_product_")
def get_products(
    search: str |None=None,
    category: str |None=None,
    min_price: float |None=None,
    max_price: float |None=None,
    sort: str |None=None,
    order: str = "asc"
):
    db = SessionLocal()

    query = db.query(Product).filter(
        Product.is_active == True
    )

    if search:
        query = query.filter(
            Product.name.contains(search)
        )

    if category:
        query = query.filter(
            Product.category == category
        )

    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    if sort == "price":
        if order == "desc":
            query = query.order_by(Product.price.desc())
        else:
            query = query.order_by(Product.price.asc())

    elif sort == "name":
        if order == "desc":
            query = query.order_by(Product.name.desc())
        else:
            query = query.order_by(Product.name.asc())

    products = query.all()

    db.close()

    return products
