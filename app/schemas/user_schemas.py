

from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re
from app.schemas.pagination_schema import PaginationLink


from app.utils.nickname_gen import generate_nickname
from app.utils.security import validate_password
from app.models.user_model import UserRole




def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

def validate_nickname(value: str) -> str:
    """
    Validate the nickname according to the rules:
    - Must start with a letter.
    - Must be 3-30 characters long.
    - Can only contain alphanumeric characters, underscores, or hyphens.
    - Uniqueness is enforced at the service layer and model
    """
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]{2,29}$", value):
        raise ValueError(
            "Nickname must start with a letter, be 3-30 characters long, and contain only alphanumeric characters, underscores, or hyphens."
        )
    return value

class UpdateBioRequest(BaseModel):
    bio: str = Field(..., max_length=500, description="The new bio for the user (max length: 500 characters).",example="Intern software developer with a bachelor degree")

class UpdateProfilePictureRequest(BaseModel):
    profile_picture_url: str = Field(..., description="The new profile picture URL.", example="https://example.com/profiles/john_new.jpg")

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(
        None,
        example=generate_nickname(),
        min_length=3,
        max_length=30,
        pattern=r'^[\w-]+$'  # URL-safe pattern
    )
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")
    

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)

    @validator("nickname", pre=True, always=True)
    def validate_nickname_field(cls, value):
        if value:
            return validate_nickname(value)
        return value
 
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

    @validator("password", pre=True, always=True)
    def validate_password_field(cls, value):
        if value:
            validate_password(value)  # Raises a ValueError if invalid
        return value

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    nickname: Optional[str] = Field(
        None,
        example=generate_nickname(),
        min_length=3,
        max_length=30,
        pattern=r'^[\w-]+$'
    )
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")
    
    
    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

    @validator("nickname", pre=True, always=True)
    def validate_nickname_field(cls, value):
        if value:
            return validate_nickname(value)
        return value

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(
        None,
        example=generate_nickname(),
        min_length=3,
        max_length=30,
        pattern=r'^[\w-]+$'
    )  
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED") 
    is_professional: Optional[bool] = Field(default=False, example=True)
    is_locked: Optional[bool] = Field(default=False, example=False)  # Add this field
    
    @validator("nickname", pre=True, always=True)
    def validate_nickname_field(cls, value):
        if value:
            return validate_nickname(value)
        return value

class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[{
        "id": uuid.uuid4(), "nickname": generate_nickname(), "email": "john.doe@example.com",
        "first_name": "John", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "last_name": "Doe", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "profile_picture_url": "https://example.com/profiles/john.jpg", 
        "linkedin_profile_url": "https://linkedin.com/in/johndoe", 
        "github_profile_url": "https://github.com/johndoe"
    }])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
    links: Optional[List[PaginationLink]]  # Accept PaginationLink objects directly
    filters: Optional["UserSearchFilterRequest"]  # Add filters for better client-side support

class UserSearchParams(BaseModel):
    username: Optional[str] = Field(None, example="john_doe")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    role: Optional[UserRole] = Field(None, example="ADMIN")
    account_status: Optional[bool] = Field(None, example=True)
    registration_date_start: Optional[datetime] = Field(None, example="2023-01-01T00:00:00Z")
    registration_date_end: Optional[datetime] = Field(None, example="2023-12-31T23:59:59Z")

class UserSearchFilterRequest(BaseModel):
    username: Optional[str] = Field(None, example="john_doe")
    email: Optional[str] = Field(None, example="john.doe@example.com")
    role: Optional[UserRole] = Field(None, example="ADMIN")
    is_locked: Optional[bool] = Field(None, example=True)
    created_from: Optional[datetime] = Field(None, example="2024-01-01T00:00:00")
    created_to: Optional[datetime] = Field(None, example="2024-12-31T23:59:59")
    skip: int = Field(0, ge=0, example=0)
    limit: int = Field(10, gt=0, le=100, example=10)



class UserSearchQueryRequest(BaseModel):
    username: Optional[str] = Field(None, example="john_doe", description="Search users by username.")
    email: Optional[str] = Field(None, example="john.doe@example.com", description="Search users by email.")
    role: Optional[UserRole] = Field(None, example="ADMIN", description="Filter users by role.")
    is_locked: Optional[bool] = Field(None, example=False, description="Filter users by account lock status.")
    skip: int = Field(0, ge=0, example=0, description="Pagination offset.")
    limit: int = Field(10, gt=0, le=100, example=10, description="Number of records to retrieve.")

from pydantic import BaseModel
UserListResponse.update_forward_refs()
UserSearchFilterRequest.update_forward_refs()


from pydantic import BaseModel, HttpUrl

class PaginationLink(BaseModel):
    """
    Schema for pagination links.
    """
    rel: str
    href: HttpUrl  # Ensure the URL is fully qualified (absolute URL)


