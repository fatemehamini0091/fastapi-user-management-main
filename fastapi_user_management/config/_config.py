"""Fastapi application config."""
import os
import string
from random import SystemRandom
from typing import Any

from pydicom.tag import Tag

from omegaconf import OmegaConf
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi_user_management import __version__

APP_CUSTOM_CONFIG = OmegaConf.load("settings.yaml")


class Settings(BaseSettings):
    SECRET_KEY: str = os.environ.get("SECRET_KEY", None)

    # If SECRET_KEY is not provided as an environment variable, generate a random one
    if SECRET_KEY is None:
        SECRET_KEY = "".join(
            SystemRandom().choice(string.ascii_letters + string.digits)
            for _ in range(64)
        )

    ADMIN_FULLNAME: str
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str
    GROUP_TAG: str = os.environ.get("GROUP_TAG", None)
    ELEMENT_TAG: str = os.environ.get("ELEMENT_TAG", None)
    if ELEMENT_TAG and GROUP_TAG:
        DICOM_PRIVATE_TAG: Any = Tag(int(GROUP_TAG, 16), int(ELEMENT_TAG, 16))
    TITLE: str = APP_CUSTOM_CONFIG.fastapi.title
    DESCRIPTION: str = APP_CUSTOM_CONFIG.fastapi.description
    VERSION: str = __version__

    DOCS_URL: str = APP_CUSTOM_CONFIG.fastapi.docs_url
    REDOC_URL: str = APP_CUSTOM_CONFIG.fastapi.redoc_url

    ALGORITHM: str = APP_CUSTOM_CONFIG.fastapi.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        APP_CUSTOM_CONFIG.fastapi.access_token_expire_minutes
    )

    DATABASE_URI: str = APP_CUSTOM_CONFIG.database.uri
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


SETTINGS = Settings()
