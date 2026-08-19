from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from sqlalchemy import Date, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DB_PATH = Path("data/database.sqlite")


class Base(DeclarativeBase):
    pass


class JobRow(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str | None] = mapped_column(String(1000), unique=True, nullable=True)
    company: Mapped[str] = mapped_column(String(250))
    role: Mapped[str] = mapped_column(String(250))
    source_text: Mapped[str] = mapped_column(Text)
    analysis_json: Mapped[str] = mapped_column(Text)


class ApplicationRow(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(250))
    role: Mapped[str] = mapped_column(String(250))
    url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    fit_score: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(80), default="Draft")
    follow_up_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")


def engine():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    result = create_engine(f"sqlite:///{DB_PATH}")
    Base.metadata.create_all(result)
    return result


def save_job(company: str, role: str, source_text: str, analysis: dict, url: str | None = None) -> int:
    with Session(engine()) as session:
        existing = session.scalar(select(JobRow).where(JobRow.url == url)) if url else None
        if existing:
            existing.source_text, existing.analysis_json = source_text, json.dumps(analysis)
            session.commit(); return existing.id
        row = JobRow(company=company, role=role, source_text=source_text, analysis_json=json.dumps(analysis), url=url)
        session.add(row); session.commit(); return row.id


def save_application(company: str, role: str, fit_score: int, url: str | None, follow_up: date | None, notes: str) -> None:
    with Session(engine()) as session:
        session.add(ApplicationRow(company=company, role=role, fit_score=fit_score, url=url, follow_up_date=follow_up, notes=notes)); session.commit()


def list_applications() -> list[ApplicationRow]:
    with Session(engine()) as session:
        return list(session.scalars(select(ApplicationRow).order_by(ApplicationRow.id.desc())))
