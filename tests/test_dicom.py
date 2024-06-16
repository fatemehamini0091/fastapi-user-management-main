import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
import os

from fastapi_user_management.schemas.dicom import BaseDICOMCreate
from fastapi_user_management.models.dicom import DicomModel
from fastapi_user_management.crud.crud_dicom import CRUDdicom

# Initialize the CRUDdicom instance
crud_dicom = CRUDdicom(DicomModel)


@pytest.fixture(scope="module")
def setup_env():
    """Setup environment variables for testing."""
    os.environ["GROUP_TAG"] = "0010"
    os.environ["ELEMENT_TAG"] = "0010"
    yield
    del os.environ["GROUP_TAG"]
    del os.environ["ELEMENT_TAG"]


@pytest.fixture
def db_session():
    """Fixture for the database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def dicom_data():
    """Fixture for DicomModel instance data."""
    return {
        "PatientID": "12345",
        "StudyInstanceUID": "1.2.3",
        "SeriesInstanceUID": "1.2.3.4",
        "Modality": "CT",
        "BodyPartExamined": "HEAD",
        "uploaded_by": "user1",
    }


@pytest.fixture
def dicom_instance(dicom_data):
    """Fixture for a DicomModel instance."""
    return DicomModel(**dicom_data)


@patch(
    "fastapi_user_management.crud.crud_dicom.SETTINGS",
    new_callable=lambda: __import__("mock_settings").mock_settings,
)
@patch("pydicom.tag.Tag", autospec=True)
def test_create_dicom(
    mock_tag, mock_settings, setup_env, db_session, dicom_instance, dicom_data
):
    mock_tag.return_value = (0x0010, 0x0010)
    mock_settings.DICOM_PRIVATE_TAG = mock_tag.return_value

    obj_in = BaseDICOMCreate(
        PatientID=dicom_data["PatientID"],
        StudyInstanceUID=dicom_data["StudyInstanceUID"],
        SeriesInstanceUID=dicom_data["SeriesInstanceUID"],
        Modality=dicom_data["Modality"],
        BodyPartExamined=dicom_data["BodyPartExamined"],
    )

    with patch("fastapi_user_management.models.dicom.DicomModel") as DicomModelMock:
        DicomModelMock.return_value = dicom_instance

        created_dicom = crud_dicom.create(db=db_session, obj_in=obj_in)

        assert isinstance(created_dicom, DicomModel)
