"""Module to define User schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr

from fastapi_user_management.models.user import UserStatusValues
from fastapi_user_management.schemas.role import RoleBase


class UserBase(BaseModel):
    """Base Schema for users."""

    fullname: str | None = None
    username: EmailStr | None = None
    status: UserStatusValues | None = None
    phone_number: str | None = None
    roles: list[RoleBase] | None = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema use for login request."""

    username: EmailStr
    password: SecretStr
    model_config = ConfigDict(from_attributes=True)


class BaseUserCreate(UserBase):
    """Schema to create new user."""

    fullname: str
    username: EmailStr
    password: SecretStr | None = None
    phone_number: str | None = None
    roles: list[RoleBase]
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseUserCreate):
    """Schema to create pre-defined users."""

    fullname: str
    username: EmailStr
    password: SecretStr
    phone_number: str | None = None
    roles: list[RoleBase]
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    """Schema to update user password."""

    new_password: SecretStr | None
    new_password_confirm: SecretStr | None
    last_login_at: datetime | None
