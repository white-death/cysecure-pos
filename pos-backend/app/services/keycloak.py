import requests
from app.core.config import settings

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "pos-realm"


def get_admin_token():
    url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"

    data = {
        "client_id": settings.KEYCLOAK_ADMIN_CLIENT_ID,
        "username": settings.KEYCLOAK_ADMIN_USERNAME,
        "password": settings.KEYCLOAK_ADMIN_PASSWORD,
        "grant_type": "password"
    }

    res = requests.post(url, data=data)
    return res.json()["access_token"]


def create_user_in_keycloak(data, password):
    token = get_admin_token()

    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users"

    payload = {
        "username": data.phone,
        "enabled": True,
        "firstName": data.first_name,
        "lastName": data.last_name,
        "credentials": [{
            "type": "password",
            "value": password,
            "temporary": False
        }]
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)

    return res.headers["Location"].split("/")[-1]


def assign_role(user_id, role_name):
    token = get_admin_token()

    role_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/roles/{role_name}"
    role = requests.get(role_url, headers={"Authorization": f"Bearer {token}"}).json()

    assign_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users/{user_id}/role-mappings/realm"

    requests.post(assign_url, json=[role], headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })
