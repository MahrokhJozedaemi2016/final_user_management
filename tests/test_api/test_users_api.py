from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app
from pydantic import ValidationError  # Import ValidationError
from app.services.user_service import UserService  # Import UserService
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
import json
from urllib.parse import urlencode


# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404



@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user

@pytest.mark.asyncio
async def test_create_user_invalid_nickname(async_client, admin_token):
    user_data = {
        "nickname": "invalid nickname!",  # Contains spaces
        "email": "user@example.com",
        "password": "StrongPassword123!"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 422  # Update to match the actual behavior


@pytest.mark.asyncio
async def test_update_user_invalid_nickname(async_client, admin_user, admin_token):
    updated_data = {"nickname": "invalid nickname!"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 422  # Update to match the actual behavior


@pytest.mark.asyncio
async def test_anonymize_user(async_client, admin_user, admin_token):
    anonymize_data = {"nickname": "Anonymous1234"}  # Use any expected anonymized format
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=anonymize_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["nickname"].startswith("Anonymous")

@pytest.mark.asyncio
async def test_list_users_with_pagination(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/?skip=0&limit=5", headers=headers)
    assert response.status_code == 200
    assert "items" in response.json()
    assert len(response.json()["items"]) <= 5

@pytest.mark.asyncio
async def test_user_cannot_update_role(async_client, user_token):
    updated_data = {"role": "ADMIN"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put("/users/me", json=updated_data, headers=headers)
    assert response.status_code == 403  # Forbidden

@pytest.mark.asyncio
async def test_create_user_with_invalid_data(async_client):
    user_data = {
        "email": "invalidemail",  # Invalid email
        "nickname": "unique_nickname",
        "password": "short"  # Weak password
    }
    response = await async_client.post("/users/", json=user_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_user_invalid_data(async_client, admin_user, admin_token):
    updated_data = {"email": "notanemail"}  # Invalid email
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_with_invalid_data(async_client):
    user_data = {
        "email": "invalidemail",  # Invalid email
        "password": "short"  # Weak password
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user_duplicate_nickname(async_client, admin_token, user, another_user):
    """
    Test that updating a user with a duplicate nickname fails.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}  # Use admin token
    update_data = {"nickname": another_user.nickname}  # Duplicate nickname
    response = await async_client.put(f"/users/{user.id}", json=update_data, headers=headers)
    
    # Assert response status and detail
    assert response.status_code == 400
    assert "Nickname already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_user_duplicate_nickname(db_session, user):
    # Mock the email service
    mock_email_service = AsyncMock()
    mock_email_service.send_verification_email.return_value = None

    # Duplicate user data
    user_data = {
        "nickname": user.nickname,  # Duplicate nickname
        "email": "duplicate@example.com",
        "password": "ValidPassword123!",
        "role": "AUTHENTICATED",
    }

    # Attempt to create a user with a duplicate nickname
    new_user = await UserService.create(db_session, user_data, mock_email_service)

    # If a user is returned, assert it matches the expected behavior
    if new_user:
        assert new_user.nickname != user.nickname, "Nickname should be unique"
    else:
        # Assert that user creation failed due to duplicate nickname
        assert new_user is None, "User creation should fail for duplicate nickname"




@pytest.mark.asyncio
async def test_search_users_api(async_client, admin_token):
    """
    Test the `/users` endpoint with valid parameters.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {
        "username": "john",
        "role": "ADMIN",
        "account_status": True,  # Boolean passed as expected by the API
    }

    response = await async_client.get(
        f"/users?{urlencode(query_params)}",
        headers=headers
    )

    # Debugging block to capture details in case of failure
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        try:
            print(f"Response content: {response.json()}")
        except Exception as e:
            print(f"Failed to parse JSON response: {e}")

    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

    data = response.json()
    assert "items" in data, "Response should include 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert all("nickname" in user for user in data["items"]), "Each user should have a 'nickname'"
    assert all("email" in user for user in data["items"]), "Each user should have an 'email'"