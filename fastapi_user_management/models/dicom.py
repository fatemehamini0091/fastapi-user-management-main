"""Define dicom Model Table."""

from sqlalchemy import Integer, String, ForeignKey, Column

from fastapi_user_management.models.base import Base
from .user import UserModel


class DicomModel(Base):
    """Dicom Database Table."""

    __tablename__ = "dicom_series"
    PatientID = Column(String, primary_key=True, index=True)
    StudyInstanceUID = Column(String, index=True)
    SeriesInstanceUID = Column(String, index=True)
    Modality = Column(String, index=True)
    BodyPartExamined = Column(String, index=True)
    uploaded_by = Column(Integer, ForeignKey(UserModel.id))
