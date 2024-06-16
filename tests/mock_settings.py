# mock_settings.py
from pydantic import EmailStr
from pydantic_settings import BaseSettings

from pydicom.tag import Tag
from typing import Any


class MockSettings(BaseSettings):
    SECRET_KEY: str = "testsecretkey"
    ADMIN_FULLNAME: str = "admin"
    ADMIN_EMAIL: EmailStr = "admin@example.com"
    ADMIN_PASSWORD: str = "password"
    GROUP_TAG: str = "0010"
    ELEMENT_TAG: str = "0010"
    DICOM_PRIVATE_TAG: Any = Tag(0x0010, 0x0010)
    TITLE: str = "Test API"
    DESCRIPTION: str = "Test Description"
    VERSION: str = "0.1.0"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URI: str = "sqlite:///./test.db"


mock_settings = MockSettings()
