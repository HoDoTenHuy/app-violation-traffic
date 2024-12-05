import io
import cv2
import uvicorn

from PIL import Image
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, HTMLResponse
from helpers.stream_helper import *
from utils.common import *
from pydantic import BaseModel
from fastapi.logger import logger
from fastapi.responses import StreamingResponse
from yolov8_detection import get_model as get_det_model
from fastapi import FastAPI, File, BackgroundTasks, UploadFile, HTTPException

detector_model = None

app = FastAPI(
    title="Vehicle Detector",
    description="Vehicle Detector using DL Models",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")

@app.on_event("startup")
def startup():
    global detector_model
    if detector_model is None:
        detector_model = get_det_model("./weights/best.pt")
    return detector_model


@app.post("/detection/run")
def run_app(file: UploadFile = File(...)):
    file_path, file_type = save_temp_file(file=file)
    global detector_model

    if file_type == "video":
        return StreamingResponse(process_frame(file_path, detector_model), media_type="multipart/x-mixed-replace; boundary=frame")
    else:
        image = Image.open(file_path)
        converted_img = detector_model.detect(image)
        image_pil = Image.fromarray(converted_img[0].plot()[..., ::-1])
        image_bytes = convert_pil2bytes(image_pil)

        os.remove(file_path)
        return StreamingResponse(io.BytesIO(image_bytes.read()), media_type="image/png")



@app.post("/detection/image")
def post_predict_detector_image(file: bytes = File(...)):
    logger.info("get image")
    global detector_model
    bytes_io = BytesIO(file)
    image_pil = Image.open(bytes_io)
    converted_img = detector_model.detect(image_pil)
    image_pil = Image.fromarray(converted_img[0].plot()[..., ::-1])
    image_bytes = convert_pil2bytes(image_pil)

    return StreamingResponse(io.BytesIO(image_bytes.read()), media_type="image/png")


@app.post("/detection/video")
async def post_predict_detector_video(video_data: str, background_tasks: BackgroundTasks):
    logger.info(f"Post Success Video")
    name = f"/var/lib/assets/detect1.mp4"
    logger.info(f"file: {name}")
    global detector_model

    if video_data.path:
        video_path = video_data.path
    else:
        video_path = "data/2.mp4"

    try:
        logger.info(f"file: {video_path}")

        background_tasks.add_task(
            detector_model.track, video_path, name
        )
    except Exception as e:
        logger.error(e)


@app.get("/detection/video/status")
async def get_predict_detector_video():
    global detector_model
    status, progress, save_path = detector_model.get_status()

    return {"status": status, "progress": progress, "save_path": save_path}


if __name__ == '__main__':
    uvicorn.run("server:app",
                host='0.0.0.0',
                port=8005, reload=True)
