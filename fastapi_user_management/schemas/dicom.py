"""Module to define DICOM schemas."""
from pydantic import BaseModel, ConfigDict


class BaseDICOMCreate(BaseModel):
    """Base Schema for DICOM."""

    PatientID: str | None = None
    StudyInstanceUID: str | None = None
    SeriesInstanceUID: str | None = None
    Modality: str | None = None
    BodyPartExamined: str | None = None
    model_config = ConfigDict(from_attributes=True)


class DICOMCreate(BaseDICOMCreate):
    PatientID: str
    StudyInstanceUID: str
    SeriesInstanceUID: str
    Modality: str
    BodyPartExamined: str
    model_config = ConfigDict(from_attributes=True)
