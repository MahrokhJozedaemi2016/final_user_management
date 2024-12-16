from typing import List
from fastapi import Request
from app.schemas.link_schema import Link
from app.schemas.pagination_schema import PaginationLink
from uuid import UUID

# Utility function to create a generic link
def create_link(rel: str, href: str, method: str = "GET", action: str = None) -> Link:
    """
    Create a generic navigation link.
    """
    return Link(rel=rel, href=href, method=method, action=action)

# Utility function to create a pagination link
def create_pagination_link(rel: str, base_url: str, params: dict) -> PaginationLink:
    """
    Create a pagination link by combining base URL with query parameters.

    :param rel: Relation type (self, next, prev, etc.)
    :param base_url: Base absolute URL
    :param params: Query parameters for pagination
    :return: PaginationLink object
    """
    query_string = f"skip={params['skip']}&limit={params['limit']}"
    absolute_url = f"{base_url.rstrip('/')}{'?' if '?' not in base_url else '&'}{query_string}" # Ensure absolute URL
    return PaginationLink(rel=rel, href=absolute_url)

# Generate user-specific navigation links
def create_user_links(user_id: UUID, request: Request) -> List[Link]:
    """
    Generate navigation links for user actions.

    :param user_id: UUID of the user
    :param request: Incoming request object for URL generation
    :return: List of Link objects
    """
    actions = [
        ("self", "get_user", "GET", "view"),
        ("update", "update_user", "PUT", "update"),
        ("delete", "delete_user", "DELETE", "delete")
    ]
    return [
        create_link(rel, str(request.url_for(action, user_id=str(user_id))), method, action_desc)
        for rel, action, method, action_desc in actions
    ]
def generate_pagination_links(request: Request, skip: int, limit: int, total_items: int) -> List[PaginationLink]:
    """
    Generate pagination links for API responses.

    :param request: FastAPI Request object to extract the base URL
    :param skip: Current skip (offset) value
    :param limit: Number of items per page
    :param total_items: Total number of items
    :return: List of PaginationLink objects
    """
    base_url = str(request.base_url) + str(request.url.path)  # Combine base URL and path
    total_pages = (total_items + limit - 1) // limit  # Calculate total pages

    # List to store pagination links
    links = [
        create_pagination_link("self", base_url, {"skip": skip, "limit": limit}),
        create_pagination_link("first", base_url, {"skip": 0, "limit": limit}),
        create_pagination_link("last", base_url, {"skip": max(0, (total_pages - 1) * limit), "limit": limit}),
    ]

    # Add 'next' link if there are more pages
    if skip + limit < total_items:
        links.append(create_pagination_link("next", base_url, {"skip": skip + limit, "limit": limit}))

    # Add 'prev' link if we are past the first page
    if skip > 0:
        links.append(create_pagination_link("prev", base_url, {"skip": max(skip - limit, 0), "limit": limit}))

    return links
