from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile

from src.config import config
from src.main.constants import ALLOWED_EXT, MAX_FILE_SIZE


def validate_extension(filename: str) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Unsupported file type")



async def save_uploaded_file(call_id: int, file: UploadFile) -> Path:
    recording_dir = Path(config.recordings_dir) / str(call_id)
    recording_dir.mkdir(parents=True, exist_ok=True)
    file_path = recording_dir / file.filename

    written = 0
    async with aiofiles.open(file_path, "wb") as out_file:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            written += len(chunk)
            if written > MAX_FILE_SIZE:
                await out_file.close()
                file_path.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="File too large")
            await out_file.write(chunk)

    return file_path