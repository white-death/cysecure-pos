from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.customer import Customer

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse
)

from app.utils.id_generator import (
    generate_customer_id
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE CUSTOMER
@router.post(
    "/",
    response_model=CustomerResponse
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    # CHECK PHONE DUPLICATE
    if customer.phone_number:

        existing_phone = db.query(Customer).filter(
            Customer.phone_number == customer.phone_number
        ).first()

        if existing_phone:
            raise HTTPException(
                status_code=400,
                detail="Phone number already exists"
            )

    # CHECK EMAIL DUPLICATE
    if customer.email_address:

        existing_email = db.query(Customer).filter(
            Customer.email_address == customer.email_address
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    count = db.query(Customer).count()

    customer_id = generate_customer_id(
        count + 1
    )

    new_customer = Customer(

        id=customer_id,

        phone_number=customer.phone_number,

        email_address=customer.email_address,

        first_name=customer.first_name,

        last_name=customer.last_name,

        special_occasion_date=customer.special_occasion_date,

        special_occasion_description=customer.special_occasion_description,

        feedback_recommendations=customer.feedback_recommendations,

        frequent_order_type=customer.frequent_order_type,

        crypto_wallet_address=customer.crypto_wallet_address,

        loyalty_points=0,

        loyalty_progress="Bronze"
    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    return new_customer


# GET ALL CUSTOMERS
@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db)
):

    customers = db.query(Customer).all()

    return customers


# GET CUSTOMER BY ID
@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer
