import pytest
from unittest.mock import patch, MagicMock, mock_open
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.utils.validators import validate_email_address, validate_url_safe_username
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import EmailNotValidError
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, Mock, patch
from app.models.user_model import User
import asyncio

from unittest.mock import AsyncMock, Mock, patch
from app.services.email_service import EmailService
from app.models.user_model import User
from app.utils.template_manager import TemplateManager
from app.utils.smtp_connection import SMTPClient
from settings.config import settings

# ---------------- SMTPClient Tests ----------------

@pytest.mark.asyncio
async def test_smtp_client_send_email_success():
    """Test sending an email successfully."""
    client = SMTPClient("smtp.example.com", 587, "user@example.com", "password")

    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        client.send_email("Test Subject", "<p>Hello</p>", "recipient@example.com")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@example.com", "password")
        mock_server.sendmail.assert_called_once()

@pytest.mark.asyncio
async def test_smtp_client_send_email_failure():
    """Test failing to send an email raises an exception."""
    client = SMTPClient("smtp.example.com", 587, "user@example.com", "password")

    with patch("smtplib.SMTP", side_effect=Exception("SMTP error")):
        with pytest.raises(Exception, match="SMTP error"):
            client.send_email("Test Subject", "<p>Hello</p>", "recipient@example.com")


# ---------------- TemplateManager Tests ----------------

def test_render_template_file_not_found():
    """Test rendering a template when a file is missing."""
    manager = TemplateManager()

    with patch("pathlib.Path.open", side_effect=FileNotFoundError("Template not found")):
        with pytest.raises(FileNotFoundError):
            manager.render_template("non_existent", name="John Doe")



@pytest.fixture
def template_manager():
    return TemplateManager()


def test_read_template_success(template_manager):
    """Test successful reading of a template file."""
    fake_content = "This is a test template."
    with patch("builtins.open", mock_open(read_data=fake_content)):
        result = template_manager._read_template("test_template.md")
        assert result == fake_content


def test_read_template_file_not_found(template_manager):
    """Test _read_template when the file is missing."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            template_manager._read_template("missing_template.md")


def test_apply_email_styles(template_manager):
    """Test applying inline email styles."""
    input_html = "<h1>Title</h1><p>Hello World</p>"
    result = template_manager._apply_email_styles(input_html)
    assert "font-family: Arial, sans-serif" in result
    assert 'style="font-size: 24px;' in result  # Check h1 style
    assert 'style="font-size: 16px;' in result  # Check p style


@pytest.fixture
def template_manager():
    return TemplateManager()

def test_render_template_missing_file(template_manager):
    """Test render_template when a required file is missing."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            template_manager.render_template("test_template", name="John Doe")



# ---------------- Validator Tests ----------------

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("", False),
    (None, False),
])
def test_validate_email_address(email, expected):
    """Test validating email addresses."""
    result = validate_email_address(email)
    assert result == expected

@pytest.mark.parametrize("username, expected", [
    ("valid_username", True),
    ("valid-username123", True),
    ("invalid username!", False),
    ("", False),
    (None, False),  # Test case for None input
])
def test_validate_url_safe_username(username, expected):
    """Test validating URL-safe usernames."""
    result = validate_url_safe_username(username)
    assert result == expected



@pytest.mark.parametrize("email, expected", [
    ("valid.email@example.com", True),
    ("invalid-email", False),
    ("", False),
    (None, False),
    ("another.valid_email@domain.org", True)
])
def test_validate_email_address(email, expected):
    """Test validation of email addresses."""
    result = validate_email_address(email)
    assert result == expected


def test_validate_email_address_with_exception():
    """Test validate_email_address when EmailNotValidError is raised."""
    with patch("email_validator.validate_email", side_effect=EmailNotValidError("Invalid email")):
        result = validate_email_address("invalid-email")
        assert result is False


@pytest.mark.parametrize("username, expected", [
    ("valid_username", True),
    ("valid-username123", True),
    ("invalid username!", False),
    ("", False),
    (None, False),
    ("__safe_username__", True)
])
def test_validate_url_safe_username(username, expected):
    """Test validation of URL-safe usernames."""
    result = validate_url_safe_username(username)
    assert result == expected

#--------------------email servicetests---------------------
import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.email_service import EmailService
from app.models.user_model import User
from app.utils.template_manager import TemplateManager
from app.utils.smtp_connection import SMTPClient
from settings.config import settings
import asyncio


# Fixture for the TemplateManager
@pytest.fixture
def mock_template_manager():
    return Mock(spec=TemplateManager)


# Fixture for the EmailService
@pytest.fixture
def email_service(mock_template_manager):
    return EmailService(template_manager=mock_template_manager)


# Mock User object
@pytest.fixture
def mock_user():
    return User(
        id="1234",
        first_name="John",
        email="john.doe@example.com",
        verification_token="fake-token"
    )


# Test: send_user_email with invalid email_type
@pytest.mark.asyncio
async def test_send_user_email_invalid_email_type():
    """Test that send_user_email raises ValueError for invalid email_type."""
    mock_template_manager = Mock(spec=TemplateManager)
    email_service = EmailService(template_manager=mock_template_manager)

    with pytest.raises(ValueError, match="Invalid email type"):
        await email_service.send_user_email(
            {"email": "test@example.com", "name": "Test User"}, "invalid_type"
        )


# Test: send_user_email successfully sends an email
@patch.object(SMTPClient, "send_email")
def test_send_user_email_success(mock_send_email, email_service, mock_template_manager):
    """Test that send_user_email calls SMTPClient with correct parameters."""
    mock_template_manager.render_template.return_value = "<p>Email Content</p>"

    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }

    asyncio.run(email_service.send_user_email(user_data, "email_verification"))

    mock_template_manager.render_template.assert_called_once_with("email_verification", **user_data)
    mock_send_email.assert_called_once_with(
        "Verify Your Account", "<p>Email Content</p>", "test@example.com"
    )


# Test: send_verification_email with proper input
@patch.object(EmailService, "send_user_email", new_callable=AsyncMock)
def test_send_verification_email_success(mock_send_user_email, email_service, mock_user):
    """Test that send_verification_email calls send_user_email correctly."""
    asyncio.run(email_service.send_verification_email(mock_user))

    expected_data = {
        "name": "John",
        "verification_url": f"{settings.server_base_url}verify-email/{mock_user.id}/{mock_user.verification_token}",
        "email": mock_user.email
    }

    mock_send_user_email.assert_awaited_once_with(expected_data, "email_verification")


##---------------------------test_dependencies--------------------

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException, Depends
from app.dependencies import (
    get_settings,
    get_email_service,
    get_db,
    get_current_user,
    require_role,
)
from app.services.email_service import EmailService
from settings.config import Settings
from app.services.jwt_service import decode_token
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_get_settings():
    """Test that get_settings returns a valid Settings instance."""
    settings = get_settings()
    assert isinstance(settings, Settings)


@pytest.mark.asyncio
async def test_get_email_service():
    """Test that get_email_service returns a valid EmailService instance."""
    email_service = get_email_service()
    assert isinstance(email_service, EmailService)
    assert email_service.template_manager is not None


@pytest.mark.asyncio
async def test_get_db_success():
    """Test that get_db yields a database session."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_factory = AsyncMock()
    mock_factory.__aenter__.return_value = mock_session

    with patch("app.database.Database.get_session_factory", return_value=lambda: mock_factory):
        async for session in get_db():  # Use async for with async generators
            assert session == mock_session


@pytest.mark.asyncio
async def test_get_current_user_invalid():
    """Test get_current_user raises HTTPException for invalid tokens."""
    with patch("app.services.jwt_service.decode_token", return_value=None):
        with pytest.raises(HTTPException) as exc:
            get_current_user(token="invalid_token")
        assert exc.value.status_code == 401
        assert "Could not validate credentials" in exc.value.detail


@pytest.mark.asyncio
async def test_require_role_valid():
    """Test require_role allows valid roles."""
    current_user = {"user_id": "user123", "role": "ADMIN"}
    role_dependency = require_role(["ADMIN"])
    result = role_dependency(current_user=current_user)
    assert result == current_user


@pytest.mark.asyncio
async def test_require_role_invalid():
    """Test require_role raises HTTPException for invalid roles."""
    current_user = {"user_id": "user123", "role": "USER"}
    role_dependency = require_role(["ADMIN"])
    with pytest.raises(HTTPException) as exc:
        role_dependency(current_user=current_user)
    assert exc.value.status_code == 403
    assert "Operation not permitted" in exc.value.detail

###--------------------main tests----------------------------


client = TestClient(app)

def test_app_metadata():
    assert app.title == "User Management"
    assert app.version == "0.0.1"
    assert app.description is not None
    assert app.contact == {
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    }
    