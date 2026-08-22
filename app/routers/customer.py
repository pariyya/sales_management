#Customer module for add, update, delete, and display customers
#import required libraries, model and schema
#create a new customer with user information
#display all customers
#find a customer by id
#update an existing customer without creating a new object
#delete a customer by id
#show HTTP error if the customer is not found

from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.customer import Customer
from app.schemas.customers import CustomerSchema
from app.models.user import User

router = APIRouter()
@router.post("/_create_customer_/{registration_id}/{registration_email}")
def create_customer(
    registration_id: int,
    registration_email: str,
    data: CustomerSchema
):

    db = SessionLocal()

    
    user = db.query(User).filter(
            (User.id == registration_id) and
            (User.email == registration_email)
    ).first()

    if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found. Please register first."
            )

    existing_customer = db.query(Customer).filter(
            Customer.email == registration_email
        ).first()

    if existing_customer:
            raise HTTPException(
                status_code=409,
                detail="This user is already a customer."
            )


    customer = Customer(
            name=data.name,
            phone=data.phone,
            email=registration_email,
            address=data.address
        )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return {
            "message": "Customer created successfully",
            "customer_id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "address": customer.address
        }

    
    db.close()

@router.get("/customers/{customer_id}")
def get_customer(customer_id: int):

    db = SessionLocal()

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.close()

    return customer

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):

    db = SessionLocal()

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()
    db.close()

    return {
        "message": "Customer deleted successfully"
    }