"""CRUD module for DICOMModel table."""

from sqlalchemy.orm import Session

from fastapi_user_management.crud.crud_base import CRUDBase
from fastapi_user_management.models.dicom import DicomModel
from fastapi_user_management.schemas.dicom import BaseDICOMCreate, DICOMCreate


class CRUDdicom(CRUDBase[DicomModel, DICOMCreate, BaseDICOMCreate]):
    """CRUD for dicom objects."""

    def create(self, db: Session, *, obj_in: BaseDICOMCreate) -> DicomModel:
        """Creat new DICOM in database.

        Args:
            db (Session): database session
            obj_in (BaseDICOMCreate): DICOM object from schema

        Returns:
            DicomModel: created DICOM
        """
        # Extract the required fields
        dicom_series_data = DICOMCreate(
            PatientID=obj_in.PatientID if "PatientID" in obj_in else "",
            StudyInstanceUID=(
                obj_in.StudyInstanceUID if "StudyInstanceUID" in obj_in else ""
            ),
            SeriesInstanceUID=(
                obj_in.SeriesInstanceUID if "SeriesInstanceUID" in obj_in else ""
            ),
            Modality=obj_in.Modality if "Modality" in obj_in else "",
            BodyPartExamined=(
                obj_in.BodyPartExamined if "BodyPartExamined" in obj_in else ""
            ),
        )

        # Create a new DicomSeries object
        new_dicom_series = DicomModel(**dicom_series_data.dict(), uploaded_by=None)

        # Save to the database
        db.add(new_dicom_series)
        db.commit()
        db.refresh(new_dicom_series)
        return new_dicom_series

    # Storing the tag in an environment variable


dicom = CRUDdicom(DicomModel)
