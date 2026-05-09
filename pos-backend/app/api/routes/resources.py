from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.resource import Resource
from app.schemas.resource import (
    ResourceCreate,
    ResourceResponse
)
from app.utils.id_generator import generate_resource_id

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Resource
@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):

    valid_types = [
        "food",
        "beverage",
        "dessert",
        "sellable",
        "merchandise"
    ]

    if resource.resource_type.lower() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid resource type"
        )

    # Count existing resources of same type
    count = db.query(Resource).filter(
        Resource.resource_type == resource.resource_type.lower()
    ).count()

    # Generate ID
    resource_id = generate_resource_id(
        resource.resource_type,
        count + 1
    )

    # Create object
    new_resource = Resource(
        id=resource_id,
        name=resource.name,
        resource_type=resource.resource_type.lower(),
        description=resource.description,
        price=resource.price,
        instock_quantity=resource.instock_quantity,
        resource_location=resource.resource_location,
        image_url=resource.image_url
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


# Get All Resources
@router.get("/", response_model=list[ResourceResponse])
def get_resources(
    db: Session = Depends(get_db)
):

    resources = db.query(Resource).all()

    return resources


# Get Resource By ID
@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: str,
    db: Session = Depends(get_db)
):

    resource = db.query(Resource).filter(
        Resource.id == resource_id
    ).first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource
