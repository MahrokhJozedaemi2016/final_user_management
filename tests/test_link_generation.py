import pytest
from unittest.mock import MagicMock
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from uuid import uuid4
from starlette.datastructures import URL
from app.schemas.pagination_schema import PaginationLink
from app.utils.link_generation import create_user_links, create_pagination_link, generate_pagination_links


# Helper function to normalize URLs for consistent comparison
def normalize_url(url):
    """Normalize the URL for consistent comparison by sorting query parameters."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    sorted_query = sorted((k, sorted(v)) for k, v in query_params.items())
    normalized_query = urlencode(sorted_query, doseq=True)
    return urlunparse(parsed_url._replace(query=normalized_query)).rstrip("/")


@pytest.fixture
def mock_request():
    """
    Fixture to create a mock Request object with base_url and url.path.
    """
    class MockRequest:
        def __init__(self, base_url, path):
            self.base_url = URL(base_url.rstrip("/"))  # Simulates base_url
            self.url = URL(f"{self.base_url}{path}")   # Simulates url.path

        def url_for(self, action, user_id):
            return f"{self.base_url}/{action}/{user_id}"

    return MockRequest("http://testserver", "/users")


def test_create_user_links(mock_request):
    """
    Test create_user_links function to ensure proper user-specific links.
    """
    user_id = uuid4()
    links = create_user_links(user_id, mock_request)

    # Check the number of links created
    assert len(links) == 3

    # Define expected URLs
    expected_self_url = f"http://testserver/get_user/{user_id}"
    expected_update_url = f"http://testserver/update_user/{user_id}"
    expected_delete_url = f"http://testserver/delete_user/{user_id}"

    # Assert links are correct
    assert normalize_url(str(links[0].href)) == normalize_url(expected_self_url)
    assert normalize_url(str(links[1].href)) == normalize_url(expected_update_url)
    assert normalize_url(str(links[2].href)) == normalize_url(expected_delete_url)


def test_generate_pagination_links(mock_request):
    """
    Test generate_pagination_links function for valid pagination links.
    """
    skip = 10
    limit = 5
    total_items = 50

    # Generate pagination links
    links = generate_pagination_links(mock_request, skip, limit, total_items)

    # Convert the links to a dictionary for easier assertions
    link_dict = {link.rel: str(link.href) for link in links}

    # Define expected URLs
    expected_self_url = "http://testserver/users?skip=10&limit=5"
    expected_first_url = "http://testserver/users?skip=0&limit=5"
    expected_last_url = "http://testserver/users?skip=45&limit=5"
    expected_next_url = "http://testserver/users?skip=15&limit=5"
    expected_prev_url = "http://testserver/users?skip=5&limit=5"

    # Assert links are correct
    assert normalize_url(link_dict["self"]) == normalize_url(expected_self_url), "Self link is incorrect"
    assert normalize_url(link_dict["first"]) == normalize_url(expected_first_url), "First link is incorrect"
    assert normalize_url(link_dict["last"]) == normalize_url(expected_last_url), "Last link is incorrect"
    assert normalize_url(link_dict["next"]) == normalize_url(expected_next_url), "Next link is incorrect"
    assert normalize_url(link_dict["prev"]) == normalize_url(expected_prev_url), "Prev link is incorrect"
