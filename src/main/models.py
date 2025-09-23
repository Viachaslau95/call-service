import datetime

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.main.infra.sql.models import TimestampMixin, Base


class Call(TimestampMixin, Base):
    __tablename__ = "calls"

    caller: Mapped[str]
    receiver: Mapped[str]
    started_at: Mapped[datetime.datetime]

    recording: Mapped["Recording"] = relationship(
        "Recording",
        back_populates="call",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Recording(TimestampMixin, Base):
    __tablename__ = "recordings"

    filename: Mapped[str]
    duration: Mapped[int]
    transcription: Mapped[str] = mapped_column(Text, nullable=True)

    call: Mapped[Call] = relationship("Call", back_populates="recording")
    call_id: Mapped[int] = mapped_column(ForeignKey("calls.id", ondelete="CASCADE"))
