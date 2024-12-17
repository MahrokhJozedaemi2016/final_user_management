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
from sqlalchemy.exc import DBAPIError
from datetime import datetime, timezone, timedelta




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

    # Ensure URL path matches API routing and avoids the 307 redirect
    response = await async_client.get(
        f"/users/?{urlencode(query_params)}",  # Note the trailing slash
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

    # Assert the status code is 200
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

    # Validate response content
    data = response.json()
    assert "items" in data, "Response should include 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert all("nickname" in user for user in data["items"]), "Each user should have a 'nickname'"
    assert all("email" in user for user in data["items"]), "Each user should have an 'email'"
    
    
@pytest.mark.asyncio
async def test_empty_filters_api(async_client, admin_token):
    """
    Test the `/users/` endpoint with no filters provided.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {}  # No filters applied

    # Ensure the endpoint URL has a trailing slash
    response = await async_client.get(f"/users/?{urlencode(query_params)}", headers=headers)

    # Assert the status code is 200
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

    # Validate response data
    data = response.json()
    assert isinstance(data["items"], list), "Response items should be a list"
    assert data["total"] > 0, "Response should return at least one user"

@pytest.mark.asyncio
async def test_fetch_all_users(async_client, admin_token):
    """
    Test the `/users/` endpoint with no filters to fetch all users.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {"skip": 0, "limit": 10}  # Basic pagination parameters

    # Ensure the endpoint URL has a trailing slash
    response = await async_client.get(f"/users/?{urlencode(query_params)}", headers=headers)

    # Assert the status code is 200
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

    # Validate response data
    data = response.json()
    assert "items" in data, "Response should include an 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert data["total"] >= 0, "Total users count should be a non-negative integer"
    
@pytest.mark.asyncio
async def test_search_users_pagination(async_client, admin_token):
    """
    Test the `/users/` endpoint with pagination parameters.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    query_params = {"skip": 0, "limit": 5}  # Test fetching the first 5 users

    # Ensure the endpoint URL has a trailing slash
    response = await async_client.get(f"/users/?{urlencode(query_params)}", headers=headers)

    # Assert the response for the first page
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert len(data["items"]) <= 5, "Number of users in the response should not exceed the limit"
    assert data["total"] >= len(data["items"]), "Total users should be greater or equal to the returned items"

    # Test the next page
    query_params = {"skip": 5, "limit": 5}  # Test fetching the next 5 users
    response = await async_client.get(f"/users/?{urlencode(query_params)}", headers=headers)

    # Assert the response for the next page
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"
    assert len(data["items"]) <= 5, "Number of users in the response should not exceed the limit"


@pytest.mark.asyncio
async def test_advanced_search_users_with_all_filters(async_client, admin_token):
    """
    Test advanced search with all filters applied together.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "username": "john",  
        "email": "example",  
        "role": "ADMIN",
        "is_locked": False,
        "created_from": (datetime.now(timezone.utc) - timedelta(days=30)).isoformat(),
        "created_to": datetime.now(timezone.utc).isoformat(),
        "skip": 0,
        "limit": 10
    }

    response = await async_client.post("/users-advanced", json=payload, headers=headers)

    # Assertions
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert data["total"] >= 0, "Total users count should be a non-negative integer"
    assert len(data["items"]) <= 10, "The number of users returned should not exceed the limit"

    # Verify each user matches the filters
    for user in data["items"]:
        assert "john" in user["nickname"], "Nickname should match the 'username' filter"
        assert "example" in user["email"], "Email should match the 'email' filter"
        assert user["role"] == "ADMIN", "Role should match the 'role' filter"
        assert user["is_locked"] is False, "Account status should match 'is_locked' filter"


@pytest.mark.asyncio
async def test_advanced_search_users_with_date_range_no_results(async_client, admin_token):
    """
    Test advanced search with a date range that returns no results.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "created_from": "2000-01-01T00:00:00+00:00",  # Date far in the past
        "created_to": "2000-01-31T23:59:59+00:00",    # Date far in the past
        "skip": 0,
        "limit": 10
    }

    response = await async_client.post("/users-advanced", json=payload, headers=headers)

    # Assertions
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert data["total"] == 0, "Total users should be 0 for an empty date range"
    assert len(data["items"]) == 0, "Response 'items' should be an empty list"


@pytest.mark.asyncio
async def test_advanced_search_users_with_invalid_role(async_client, admin_token):
    """
    Test advanced search with an invalid role filter.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "role": "INVALID_ROLE",  # Role that doesn't exist
        "skip": 0,
        "limit": 10
    }

    response = await async_client.post("/users-advanced", json=payload, headers=headers)

    # Assertions
    assert response.status_code == 422, "Expected status 422 for invalid input"
    data = response.json()

    assert "detail" in data, "Response should include 'detail' for validation errors"
    assert any("role" in err["loc"] for err in data["detail"]), "Validation error should be for 'role'"

@pytest.mark.asyncio
async def test_advanced_search_users_with_partial_email(async_client, admin_token):
    """
    Test advanced search with a partial email filter.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "email": "example",  # Partial email match
        "skip": 0,
        "limit": 10
    }

    response = await async_client.post("/users-advanced", json=payload, headers=headers)

    # Assertions
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert len(data["items"]) > 0, "Expected at least one user to match partial email"

    for user in data["items"]:
        assert "example" in user["email"], "Each user's email should match the partial filter"

@pytest.mark.asyncio
async def test_advanced_search_users_pagination_exceeding_total(async_client, admin_token):
    """
    Test advanced search with pagination parameters that exceed total results.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "skip": 1000,  # High offset to exceed total results
        "limit": 10
    }

    response = await async_client.post("/users-advanced", json=payload, headers=headers)

    # Assertions
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()

    assert "items" in data, "Response should include an 'items' key"
    assert len(data["items"]) == 0, "Response 'items' should be an empty list when offset exceeds total results"
    assert data["total"] >= 0, "Total users count should still be non-negative"

