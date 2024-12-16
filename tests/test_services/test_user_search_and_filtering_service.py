from builtins import range
import pytest
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from datetime import datetime, timedelta, timezone



pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_search_users_by_username(db_session, users_with_same_role_50_users):
    """
    Test searching users by username using the `search_and_filter_users` method.
    """
    # Pick a target user dynamically
    target_user = users_with_same_role_50_users[0]
    partial_username = target_user.nickname[:3].lower()  # Take first 3 characters, lowercase

    filters = {"username": partial_username}
    total, users = await UserService.search_and_filter_users(db_session, filters, 0, 10)

    # Assertions
    assert total > 0, "Total users should be greater than 0"
    assert len(users) > 0, "At least one user should be returned"
    assert all(
        partial_username in user.nickname.lower() for user in users
    ), "All returned users should contain the partial username in a case-insensitive manner"


@pytest.mark.asyncio
async def test_filter_users_by_role(db_session, users_with_same_role_50_users):
    """
    Test filtering users by role using the `search_and_filter_users` method.
    """
    filters = {"role": UserRole.ADMIN.name}
    total, users = await UserService.search_and_filter_users(db_session, filters, 0, 10)

    # Assertions
    assert total >= 0, "Total users should be a non-negative integer"
    assert all(user.role == UserRole.ADMIN.name for user in users), "All returned users should have the ADMIN role"

@pytest.mark.asyncio
async def test_filter_users_by_account_status(db_session, users_with_same_role_50_users):
    """
    Test filtering users by account status using the `search_and_filter_users` method.
    """
    filters = {"is_locked": False}
    total, users = await UserService.search_and_filter_users(db_session, filters, 0, 10)

    # Assertions
    assert total >= 0, "Total users should be a non-negative integer"
    assert all(user.is_locked is False for user in users), "All returned users should have the 'is_locked' status as False"

from datetime import datetime

@pytest.mark.asyncio
async def test_filter_users_by_registration_date(db_session, users_with_same_role_50_users):
    """
    Test filtering users by registration date using the `search_and_filter_users` method.
    """
    filters = {
        "registration_date_start": datetime(2023, 1, 1),
        "registration_date_end": datetime(2023, 12, 31)
    }
    total, users = await UserService.search_and_filter_users(db_session, filters, 0, 10)

    # Assertions
    assert total >= 0, "Total users should be a non-negative integer"
    assert all(
        datetime(2023, 1, 1) <= user.created_at <= datetime(2023, 12, 31)
        for user in users
    ), "All returned users should have registration dates within the specified range"


@pytest.mark.asyncio
async def test_filter_users_by_email(db_session, users_with_same_role_50_users):
    """
    Test filtering users by email using the `search_and_filter_users` method.
    """
    filters = {"email": users_with_same_role_50_users[0].email}
    total, users = await UserService.search_and_filter_users(db_session, filters, 0, 10)

    # Assertions
    assert total >= 0, "Total users should be a non-negative integer"
    assert all(user.email == users_with_same_role_50_users[0].email for user in users), "All returned users should match the specified email"



@pytest.mark.asyncio
async def test_combination_of_filters(db_session, users_with_same_role_50_users):
    """
    Test combination of multiple filters using the `search_and_filter_users` method.
    """
    # Pick a user dynamically to ensure proper filtering
    target_user = users_with_same_role_50_users[0]

    filters = {
        "username": target_user.nickname,
        "role": target_user.role.name,
        "is_locked": target_user.is_locked,
    }
    total, users = await UserService.search_and_filter_users(db_session, filters, 0, 10)

    # Assertions
    assert total > 0, "Total users should be greater than 0"
    assert all(
        user.nickname == target_user.nickname
        and user.role.name == target_user.role.name
        and user.is_locked == target_user.is_locked
        for user in users
    ), "All returned users should match the specified filters"

@pytest.mark.asyncio
async def test_filter_users_case_insensitive(db_session, users_with_same_role_50_users):
    """
    Test case-insensitive filtering for username and email using the `search_and_filter_users` method.
    """
    # Test case-insensitive username filtering
    filters_username = {"username": users_with_same_role_50_users[0].nickname.upper()}
    total_by_username, users_by_username = await UserService.search_and_filter_users(db_session, filters_username, 0, 10)

    # Test case-insensitive email filtering
    filters_email = {"email": users_with_same_role_50_users[0].email.upper()}
    total_by_email, users_by_email = await UserService.search_and_filter_users(db_session, filters_email, 0, 10)

    # Assertions
    assert total_by_username >= 0, "Total users should be a non-negative integer for username filter"
    assert all(
        user.nickname.lower() == users_with_same_role_50_users[0].nickname.lower()
        for user in users_by_username
    ), "All returned users should match the username filter case-insensitively"

    assert total_by_email >= 0, "Total users should be a non-negative integer for email filter"
    assert all(
        user.email.lower() == users_with_same_role_50_users[0].email.lower()
        for user in users_by_email
    ), "All returned users should match the email filter case-insensitively"




@pytest.mark.asyncio
async def test_advanced_search_users_with_no_filters(db_session, users_with_same_role_50_users):
    """
    Test advanced search with no filters.
    """
    filters = {}
    total, users = await UserService.advanced_search_users(db_session, filters)

    assert total == len(users_with_same_role_50_users), "Total users should match all users"
    assert len(users) <= 10, "Default limit should apply when no pagination is provided"

@pytest.mark.asyncio
async def test_advanced_search_users_with_username_filter(db_session, users_with_same_role_50_users):
    """
    Test advanced search with a username filter.
    """
    target_user = users_with_same_role_50_users[0]
    filters = {"username": target_user.nickname[:3]}  # Partial match
    total, users = await UserService.advanced_search_users(db_session, filters)

    assert total > 0, "Total should reflect matching users"
    assert all(target_user.nickname[:3].lower() in user.nickname.lower() for user in users), "All returned users should match the username filter"

@pytest.mark.asyncio
async def test_advanced_search_users_with_email_filter(db_session, users_with_same_role_50_users):
    """
    Test advanced search with an email filter.
    """
    target_user = users_with_same_role_50_users[0]
    filters = {"email": target_user.email[:3]}  # Partial match
    total, users = await UserService.advanced_search_users(db_session, filters)

    assert total > 0, "Total should reflect matching users"
    assert all(target_user.email[:3].lower() in user.email.lower() for user in users), "All returned users should match the email filter"

@pytest.mark.asyncio
async def test_advanced_search_users_with_role_filter(db_session, users_with_same_role_50_users):
    """
    Test advanced search with a role filter.
    """
    filters = {"role": UserRole.AUTHENTICATED}
    total, users = await UserService.advanced_search_users(db_session, filters)

    assert total > 0, "Total should reflect users with the specified role"
    assert all(user.role == UserRole.AUTHENTICATED for user in users), "All users should have the specified role"

@pytest.mark.asyncio
async def test_advanced_search_users_with_date_range_filter(db_session, users_with_same_role_50_users):
    """
    Test advanced search with a date range filter.
    """
    # Use timezone-aware datetimes
    created_from = datetime.now(timezone.utc) - timedelta(days=30)
    created_to = datetime.now(timezone.utc)
    filters = {"created_from": created_from, "created_to": created_to}

    # Call the service method
    total, users = await UserService.advanced_search_users(db_session, filters)

    # Assertions
    assert total > 0, "Total should reflect users created within the date range"
    assert all(
        created_from <= user.created_at <= created_to for user in users
    ), "All users should be within the date range"

@pytest.mark.asyncio
async def test_advanced_search_users_with_pagination(db_session, users_with_same_role_50_users):
    """
    Test advanced search with pagination.
    """
    filters = {"skip": 10, "limit": 10}
    total, users = await UserService.advanced_search_users(db_session, filters)

    assert total == len(users_with_same_role_50_users), "Total users should match all users"
    assert len(users) == 10, "Pagination should limit the results to 10"

