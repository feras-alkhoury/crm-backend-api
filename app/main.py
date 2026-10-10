from fastapi import Depends, FastAPI, Form, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    get_current_user,
    get_db,
    hash_password,
    verify_password,
)
from app.models import Customer, User
from app.database import Base, engine
from app.schemas.auth import Token, UserCreate
from app.schemas.customer import CustomerCreate, CustomerResponse


app = FastAPI(
    title="CRM Backend API",
    description="Backend API for a SaaS CRM system",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────
# Health
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "CRM Backend API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# ─────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────

@app.post("/auth/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "username": new_user.username,
    }


@app.post("/auth/login", response_model=Token)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(
        password,
        existing_user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        existing_user.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ─────────────────────────────────────────────
# Customers
# ─────────────────────────────────────────────

@app.post("/customers", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_customer = (
        db.query(Customer)
        .filter(Customer.email == customer.email)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Customer with this email already exists",
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        company=customer.company,
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@app.get("/customers", response_model=list[CustomerResponse])
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Customer)

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            (Customer.name.ilike(search_pattern))
            | (Customer.email.ilike(search_pattern))
            | (Customer.company.ilike(search_pattern))
        )

    return (
        query
        .order_by(Customer.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    duplicate_email = (
        db.query(Customer)
        .filter(
            Customer.email == customer.email,
            Customer.id != customer_id,
        )
        .first()
    )

    if duplicate_email:
        raise HTTPException(
            status_code=400,
            detail="Customer with this email already exists",
        )

    existing.name = customer.name
    existing.email = customer.email
    existing.phone = customer.phone
    existing.company = customer.company

    db.commit()
    db.refresh(existing)

    return existing


@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }
