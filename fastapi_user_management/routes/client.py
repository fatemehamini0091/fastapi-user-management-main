"""User Profile and its action as a uploader endpoints ``/client `."""
from typing import Annotated

import pydicom
from pydicom.dataelem import DataElement

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from pydantic import EmailStr
from sqlalchemy.orm import Session

from fastapi_user_management import crud

from fastapi_user_management.config import SETTINGS
from fastapi_user_management.core.database import get_db
from fastapi_user_management.models.user import UserModel
from fastapi_user_management.routes import auth
from fastapi_user_management.schemas.user import UserBase
from fastapi_user_management.schemas.dicom import DICOMCreate

router = APIRouter(
    tags=["User Profile"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
)


@router.get("/{username}", response_model=UserBase)
async def get_user_info(
    username: EmailStr,
    current_user: Annotated[UserBase, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db),
):
    """Read all users exist in database.

    Args:
        username : EmailStr
        current_user (Annotated[UserModel, Depends): logged-in user.
        db (Session, optional): db session. Defaults to Depends(get_db).

    Raises:
        HTTPException: raise exception for non-admin users with 403 status code.

    Returns:
        UserBase: current user
    """

    if crud.user.is_active(user=current_user):
        return crud.user.get_by_username(db=db, username=username)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


@router.post("/uploadfile/", response_model=DICOMCreate)
async def upload_dicom(
    current_user: Annotated[UserModel, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    if crud.user.is_active(user=current_user):
        # Read the DICOM file
        try:
            ds = pydicom.dcmread(file.file)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid DICOM file")

        # Create a new DataElement for the User ID
        new_element = DataElement(
            SETTINGS.DICOM_PRIVATE_TAG, "IS", str(current_user.id)
        )
        # 'IS' (Integer String) is a VR for integers

        # Add the new DataElement to the dataset
        ds[SETTINGS.DICOM_PRIVATE_TAG] = new_element

        # Save the modified DICOM file
        ds.save_as(file.filename)
        return crud.dicom.create(db=db, obj_in=ds)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
