from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    crew_assignments: Mapped[list["CrewAssignment"]] = relationship(back_populates="user")
    maintenance_logs: Mapped[list["MaintenanceLog"]] = relationship(back_populates="user")
    flight_notes: Mapped[list["FlightNote"]] = relationship(back_populates="user")


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_no: Mapped[str] = mapped_column(String(20), nullable=False)
    flight_date: Mapped[date] = mapped_column(Date, nullable=False)
    departure_airport: Mapped[str] = mapped_column(String(10), nullable=False)
    arrival_airport: Mapped[str] = mapped_column(String(10), nullable=False)
    sched_dep: Mapped[datetime] = mapped_column(nullable=False)
    sched_arr: Mapped[datetime] = mapped_column(nullable=False)
    actual_dep: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    actual_arr: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    crew_assignments: Mapped[list["CrewAssignment"]] = relationship(back_populates="flight")
    maintenance_logs: Mapped[list["MaintenanceLog"]] = relationship(back_populates="flight")
    flight_notes: Mapped[list["FlightNote"]] = relationship(back_populates="flight")


class CrewAssignment(Base):
    __tablename__ = "crew_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    seat: Mapped[str] = mapped_column(String(50), nullable=False)
    start_time: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    flight: Mapped["Flight"] = relationship(back_populates="crew_assignments")
    user: Mapped["User"] = relationship(back_populates="crew_assignments")


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    logged_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    flight: Mapped["Flight"] = relationship(back_populates="maintenance_logs")
    user: Mapped["User"] = relationship(back_populates="maintenance_logs")


class FlightNote(Base):
    __tablename__ = "flight_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    flight: Mapped["Flight"] = relationship(back_populates="flight_notes")
    user: Mapped["User"] = relationship(back_populates="flight_notes")



class WeatherReport(Base):
    """Persisted drone flight weather report."""

    __tablename__ = "weather_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    location: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    decision_detail: Mapped[str] = mapped_column(Text, nullable=False)
    sources_data: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="JSON-encoded list of WeatherSourceData dicts",
    )
    ai_analysis_data: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="JSON-encoded AI analysis result (GPT-4o output)",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Feedback(Base):
    """User feedback on a weather report decision."""

    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("weather_reports.id"),
        nullable=False,
        index=True,
    )
    correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
