import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import CreateUserRequest
from app.api.deps import require_admin, get_db
from app.models.user import User
from app.utils.id_generator import generate_enxu_id
from app.core.config import settings

router = APIRouter()


# -------------------------------
# Get Keycloak Admin Token
# -------------------------------
def get_admin_token():
    try:
        res = requests.post(
            f"{settings.KEYCLOAK_URL}/realms/master/protocol/openid-connect/token",
            data={
                "client_id": settings.KEYCLOAK_ADMIN_CLIENT_ID,
                "username": settings.KEYCLOAK_ADMIN_USERNAME,
                "password": settings.KEYCLOAK_ADMIN_PASSWORD,
                "grant_type": "password"
            },
            timeout=5
        )
        res.raise_for_status()
        return res.json()["access_token"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keycloak admin auth failed: {str(e)}")


# -------------------------------
# Ensure Role Exists in Keycloak
# -------------------------------
def ensure_role(token: str, role_name: str):
    url = f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/roles"

    res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    roles = res.json()

    if any(r["name"] == role_name for r in roles):
        return

    requests.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={"name": role_name}
    )


# -------------------------------
# Assign Role to User
# -------------------------------
def assign_role(token: str, user_id: str, role_name: str):
    role_url = f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/roles/{role_name}"
    user_role_url = f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}/role-mappings/realm"

    role_res = requests.get(role_url, headers={"Authorization": f"Bearer {token}"})
    role_data = role_res.json()

    requests.post(
        user_role_url,
        headers={"Authorization": f"Bearer {token}"},
        json=[{
            "id": role_data["id"],
            "name": role_data["name"]
        }]
    )


# -------------------------------
# Create User (Admin Only)
# -------------------------------
@router.post("/create-user")
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    Admin creates a user:
    - Creates user in Keycloak
    - Assigns role in Keycloak
    - Stores full profile in DB
    """

    default_password = "Temp@123"

    # -------------------------------
    # Get admin token
    # -------------------------------
    token = get_admin_token()

    # -------------------------------
    # 1. Create user in Keycloak
    # -------------------------------
    try:
        res = requests.post(
            f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": data.phone,
                "enabled": True,
                "firstName": data.first_name,
                "lastName": data.last_name,
                "credentials": [{
                    "type": "password",
                    "value": default_password,
                    "temporary": False
                }]
            },
            timeout=5
        )

        if res.status_code not in [201, 204]:
            raise HTTPException(status_code=400, detail="Failed to create user in Keycloak")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keycloak user creation failed: {str(e)}")

    # -------------------------------
    # 2. Extract Keycloak User ID
    # -------------------------------
    location = res.headers.get("Location")

    if not location:
        raise HTTPException(status_code=500, detail="Failed to get Keycloak user ID")

    keycloak_id = location.split("/")[-1]

    # -------------------------------
    # 3. Ensure Role Exists
    # -------------------------------
    ensure_role(token, data.role)

    # -------------------------------
    # 4. Assign Role in Keycloak
    # -------------------------------
    assign_role(token, keycloak_id, data.role)

    # -------------------------------
    # 5. Save in DB
    # -------------------------------
    existing_user = db.query(User).filter(User.phone == data.phone).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        id=generate_enxu_id(db),
        keycloak_id=keycloak_id,
        first_name=data.first_name,
        last_name=data.last_name,
        dob=data.dob,
        designation=data.designation,
        role=data.role,
        phone=data.phone,
        location=data.location,
        rating=0
    )

    db.add(user)
    db.commit()

    return {
        "message": "User created successfully",
        "enxu_id": user.id,
        "default_password": default_password,
        "keycloak_id": keycloak_id
    }
