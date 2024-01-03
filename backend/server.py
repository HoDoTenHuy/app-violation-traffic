import io
import cv2
import uvicorn

from PIL import Image
from utils.common import *
from pydantic import BaseModel
from fastapi.logger import logger
from fastapi.responses import StreamingResponse
from yolov8_detection import get_model as get_det_model
from fastapi import FastAPI, File, BackgroundTasks, UploadFile

detector_model = get_det_model("./weights/best.pt")

app = FastAPI(
    title="Vehicle Detector",
    description="Vehicle Detector using DL Models",
    version="0.1.0",
)


class VideoData(BaseModel):
    path: str


tasks = {}


@app.post("/detection/image")
def post_predict_disease_detector_image(file: bytes = File(...)):
    logger.info("get image")
    bytes_io = BytesIO(file)
    image_pil = Image.open(bytes_io)
    converted_img = detector_model.detect(image_pil)
    image_pil = Image.fromarray(converted_img[0].plot()[..., ::-1])
    image_bytes = convert_pil2bytes(image_pil)

    return StreamingResponse(io.BytesIO(image_bytes.read()), media_type="image/png")


@app.post("/detection/video")
async def post_predict_disease_detector_video(video_data: VideoData, background_tasks: BackgroundTasks):
    logger.info(f"Post Success Video")
    name = f"/var/lib/assets/detect1.mp4"
    logger.info(f"file: {name}")

    if video_data.path:
        video_path = video_data.path
    else:
        video_path = "data/2.mp4"

    try:
        logger.info(f"file: {video_path}")
        cap = cv2.VideoCapture(video_path)

        background_tasks.add_task(
            detector_model.track, video_path, name
        )
    except Exception as e:
        logger.error(e)


@app.get("/detection/video/status")
async def get_predict_disease_detector_video():
    status, progress, save_path = detector_model.get_status()

    return {"status": status, "progress": progress, "save_path": save_path}


if __name__ == '__main__':
    uvicorn.run("server:app",
                host='0.0.0.0',
                port=8005, reload=True)
