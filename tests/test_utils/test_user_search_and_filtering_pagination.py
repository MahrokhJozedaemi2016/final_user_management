
import pytest
from starlette.datastructures import URL
from app.utils.link_generation import generate_pagination_links
from app.schemas.pagination_schema import PaginationLink
from urllib.parse import urlencode

# Mock Request class to simulate FastAPI's Request object
class MockRequest:
    def __init__(self, base_url, path):
        self.base_url = URL(base_url)  # Simulates request.base_url
        self.url = URL(f"{base_url.rstrip('/')}{path}")  # Simulates request.url

@pytest.mark.asyncio
async def test_generate_pagination_links():
    """
    Test generate_pagination_links function for valid pagination links.
    """
    # Initialize mock request
    request = MockRequest("http://localhost:8000", "/users")

    # Input parameters
    skip = 0
    limit = 10
    total_users = 45

    # Generate pagination links
    links = generate_pagination_links(request, skip, limit, total_users)

    # Convert the links to a dictionary for easier assertions
    link_dict = {link.rel: str(link.href) for link in links}

    # Define expected URLs
    expected_self_url = "http://localhost:8000/users?skip=0&limit=10"
    expected_first_url = "http://localhost:8000/users?skip=0&limit=10"
    expected_last_url = "http://localhost:8000/users?skip=40&limit=10"
    expected_next_url = "http://localhost:8000/users?skip=10&limit=10"

    # Assert links are correct
    assert link_dict["self"] == expected_self_url, "Self link is incorrect"
    assert link_dict["first"] == expected_first_url, "First link is incorrect"
    assert link_dict["last"] == expected_last_url, "Last link is incorrect"
    assert link_dict["next"] == expected_next_url, "Next link is incorrect"
    assert "prev" not in link_dict, "Prev link should not exist on the first page"

@pytest.mark.asyncio
async def test_pagination_edge_cases():
    """
    Test edge cases for pagination utility.
    """
    # Initialize mock request
    request = MockRequest("http://localhost:8000", "/users")

    # Case 1: Total items less than the limit
    links = generate_pagination_links(request, skip=0, limit=10, total_items=5)
    link_dict = {link.rel: str(link.href) for link in links}

    # Assert no "next" or "prev" links
    assert "next" not in link_dict, "Next link should not exist when total items < limit"
    assert "prev" not in link_dict, "Prev link should not exist when on first page"
    assert link_dict["self"] == "http://localhost:8000/users?skip=0&limit=10"

    # Case 2: Total items exactly a multiple of the limit
    links = generate_pagination_links(request, skip=0, limit=10, total_items=20)
    link_dict = {link.rel: str(link.href) for link in links}

    expected_last_url = "http://localhost:8000/users?skip=10&limit=10"

    # Assert correct "last" and "next" links
    assert link_dict["last"] == expected_last_url, "Last link is incorrect"
    assert "next" in link_dict, "Next link should exist when there are more pages"



@pytest.mark.asyncio
async def test_pagination_boundary(async_client, admin_token):
    """
    Test pagination boundary cases for the `/users` endpoint.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Ensure the endpoint URL matches the expected structure of your FastAPI app
    base_url = "/users/"

    # Case 1: Skip beyond total items
    query_params = {"skip": 10000, "limit": 10}
    response = await async_client.get(f"{base_url}?{urlencode(query_params)}", headers=headers)
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "items" in data, "Response should contain 'items' key"
    assert len(data["items"]) == 0, "No items should be returned when skip exceeds total items"
    assert data.get("total", 0) >= 0, "Total items count should be non-negative"

    # Case 2: Skip=0, Limit=1
    query_params = {"skip": 0, "limit": 1}
    response = await async_client.get(f"{base_url}?{urlencode(query_params)}", headers=headers)
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "items" in data, "Response should contain 'items' key"
    assert len(data["items"]) <= 1, "Only 1 item should be returned with limit=1"
    assert data.get("total", 0) >= 1, "Total items count should be at least 1 if data exists"
