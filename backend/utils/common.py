import os
import shutil
import tempfile

from io import BytesIO
from pathlib import Path
from fastapi import UploadFile, HTTPException
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


def get_content_type(content_type: str):
    if content_type.startswith("image/"):
        file_type = "image"
        suffix = ".jpg"
    elif content_type.startswith("video/"):
        file_type = "video"
        suffix = ".mp4"
    else:
        raise HTTPException(status_code=400, detail="Unsupported content type")

    return file_type, suffix

def save_temp_file(file):
    file_type, suffix = get_content_type(file.content_type)
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    return tmp_path, file_type
