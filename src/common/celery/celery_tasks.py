from pydub import AudioSegment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from src.common.celery.celery_app import celery
from src.config import config
from src.main.models import Recording

engine = create_engine(config.postgres.sync_uri, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@celery.task(name="src.celery_tasks.recording_tasks.process_recording")
def process_recording(recording_id: int, filepath: str):
    if not os.path.exists(filepath):
        return {"ok": False, "reason": "file_not_found"}

    audio = AudioSegment.from_file(filepath)
    duration_seconds = int(audio.duration_seconds)

    first_n_secs = min(20, duration_seconds)
    pseudo_transcript = f"Detected speech fragment: first {first_n_secs} seconds from file {os.path.basename(filepath)}"

    db = SessionLocal()
    try:
        rec = db.query(Recording).filter(Recording.id == recording_id).one_or_none()
        if rec is None:
            return {"ok": False, "reason": "recording_not_found"}
        rec.duration = duration_seconds
        rec.transcription = pseudo_transcript
        db.add(rec)
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

    return {"ok": True, "duration": duration_seconds}
