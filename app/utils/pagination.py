
from typing import List
from fastapi import Request
from app.schemas.pagination_schema import PaginationLink
from app.utils.link_generation import create_pagination_link

def generate_pagination_links(request: Request, skip: int, limit: int, total_items: int) -> List[PaginationLink]:
    """
    Generate pagination links for API responses.
    """
    base_url = str(request.url)  # Use the complete URL from the request
    total_pages = (total_items + limit - 1) // limit

    links = [
        create_pagination_link("self", base_url, {"skip": skip, "limit": limit}),
        create_pagination_link("first", base_url, {"skip": 0, "limit": limit}),
        create_pagination_link("last", base_url, {"skip": max(0, (total_pages - 1) * limit), "limit": limit}),
    ]

    if skip + limit < total_items:
        links.append(create_pagination_link("next", base_url, {"skip": skip + limit, "limit": limit}))

    if skip > 0:
        links.append(create_pagination_link("prev", base_url, {"skip": max(skip - limit, 0), "limit": limit}))

    return links
