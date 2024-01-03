import os
import shutil

from io import BytesIO
from pathlib import Path
from fastapi import UploadFile
from tempfile import NamedTemporaryFile


def convert_pil2bytes(image_pil):
    # Convert the image to bytes
    image_bytes = BytesIO()
    image_pil.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    return image_bytes


def save_upload_file_tmp(upload_file) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def delete_tmp_file(path: str):
    if os.path.exists(path):
        os.remove(path)
