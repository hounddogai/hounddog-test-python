import os
from datetime import date, datetime
from functools import cache
from typing import Any

from sqlalchemy import Engine, ForeignKey, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date]
    gender: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(100))
    address: Mapped[str | None] = mapped_column(Text)
    blood_type: Mapped[str | None] = mapped_column(String(10))
    allergies: Mapped[str | None] = mapped_column(Text)
    emergency_contact_name: Mapped[str | None] = mapped_column(String(100))
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(50))
    medical_history: Mapped[str | None] = mapped_column(Text)
    current_medications: Mapped[str | None] = mapped_column(Text)
    created_date: Mapped[datetime | None] = mapped_column(default=datetime.now)

    health_metrics: Mapped[list[HealthMetric]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    medical_records: Mapped[list[MedicalRecord]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    activities: Mapped[list[Activity]] = relationship(back_populates="patient", cascade="all, delete-orphan")

    def to_dict(self) -> dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "blood_type": self.blood_type,
            "allergies": self.allergies,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "medical_history": self.medical_history,
            "current_medications": self.current_medications,
            "created_date": self.created_date,
        }


class HealthMetric(Base):
    __tablename__ = "health_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(100), ForeignKey("patients.patient_id"), index=True)
    metric_type: Mapped[str] = mapped_column(String(100))
    value: Mapped[float]
    unit: Mapped[str | None] = mapped_column(String(50))
    date: Mapped[datetime]
    notes: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))

    patient: Mapped[Patient] = relationship(back_populates="health_metrics")

    def to_dict(self) -> dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "metric_type": self.metric_type,
            "value": self.value,
            "unit": self.unit,
            "date": self.date,
            "notes": self.notes,
            "category": self.category,
        }


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(100), ForeignKey("patients.patient_id"), index=True)
    record_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    doctor_name: Mapped[str | None] = mapped_column(String(100))
    facility_name: Mapped[str | None] = mapped_column(String(200))
    record_date: Mapped[date]
    file_path: Mapped[str | None] = mapped_column(String(500))
    file_name: Mapped[str | None] = mapped_column(String(200))
    file_type: Mapped[str | None] = mapped_column(String(100))
    file_size: Mapped[int | None]
    upload_date: Mapped[datetime | None] = mapped_column(default=datetime.now)

    patient: Mapped[Patient] = relationship(back_populates="medical_records")

    def to_dict(self) -> dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "record_type": self.record_type,
            "description": self.description,
            "doctor_name": self.doctor_name,
            "facility_name": self.facility_name,
            "record_date": self.record_date,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "upload_date": self.upload_date,
        }


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[str | None] = mapped_column(String(100), ForeignKey("patients.patient_id"), index=True)
    patient_name: Mapped[str | None] = mapped_column(String(200))
    activity_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now, index=True)

    patient: Mapped[Patient | None] = relationship(back_populates="activities")

    def to_dict(self) -> dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "type": self.activity_type,
            "description": self.description,
            "timestamp": self.timestamp,
            "date": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }


@cache
def get_engine() -> Engine:
    """Return the process-wide engine for DATABASE_URL, creating it on first use."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    return create_engine(database_url, pool_pre_ping=True)


@cache
def _get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine())


def get_session() -> Session:
    """Create and return a new database session bound to the shared engine."""
    return _get_session_factory()()


def init_database() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(get_engine())
