import io
import os
import time
import json
import logging
import requests

from PIL import Image
import streamlit as st
from pydantic import BaseModel
from requests_toolbelt.multipart.encoder import MultipartEncoder

backend = "http://fastapi:8000"


class VideoData(BaseModel):
    path: str


def detect_image(data, server):
    m = MultipartEncoder(fields={"file": ("filename", data, "image/jpeg")})

    resp = requests.post(
        server + "/detection/image",
        data=m,
        headers={"Content-Type": m.content_type},
        timeout=8000,
    )

    return resp


def detect_video(path_video, server):
    video_data = VideoData(path=path_video)

    resp = requests.post(
        server + "/detection/video",
        json=video_data.dict(),
        headers={"Content-Type": "application/json"},
        timeout=8000,
    )

    return resp


def get_video_status(server):
    resp = requests.get(
        server + "/detection/video/status",
        timeout=8000,
    )

    return resp


def main():
    st.title("Vehicle Detector Application")

    st.write(
        """Test Vehicle Image
            This streamlit example uses a FastAPI service as backend.
            Visit this URL at `:8000/docs` for FastAPI documentation."""
    )  # description and instructions

    # Side Bar
    st.sidebar.title("Test Models")
    app_mode = st.sidebar.selectbox("Choose Model", ["YOLO_V8"])

    if app_mode == "YOLO_V8":
        run_app()


def run_app():
    data_type = st.selectbox("Choose Data Type", ["Image", "Video"])
    input_data = st.file_uploader(f"insert {data_type}")  # image upload widget
    time.sleep(1)

    if st.button("Detect Vehicle"):

        col1, col2 = st.beta_columns(2)

        if data_type == "Image":

            if input_data:
                pred = detect_image(input_data, backend)
                original_image = Image.open(input_data).convert("RGB")
                converted_image = pred.content
                converted_image = Image.open(io.BytesIO(converted_image)).convert("RGB")

                col1.header("Original")
                col1.image(original_image, use_column_width=True)
                col2.header("Detected")
                col2.image(converted_image, use_column_width=True)

            else:
                # handle case with no image
                st.write("Insert an image!")

        elif data_type == "Video":

            temp_path = "/var/lib/assets"
            for t in os.listdir(temp_path):
                os.remove(temp_path + "/" + t)

            origin_video = input_data.read()

            video_path = "/var/lib/assets/video1.mp4"
            if os.path.isfile(video_path):
                os.remove(video_path)

            with open(video_path, "wb") as wfile:
                wfile.write(origin_video)
                logging.info(f"{video_path} added")

            time.sleep(1)
            wfile.close()
            detect_video(video_path, backend)

            time.sleep(1)

            status = None
            bar = st.progress(0)
            # with stqdm(total=1, st_container=st) as pbar:
            while status != "Success":
                resp = get_video_status(backend)
                resp_dict = json.loads(resp.content.decode("utf-8"))
                status = resp_dict["status"]
                if status != "Pending":
                    progress = resp_dict["progress"]
                    # pbar.update(int(progress))
                    bar.progress(int(progress))

                time.sleep(1)

            time.sleep(3)

            save_path = "/var/lib/assets/detect1.mp4"
            convert_path = "/var/lib/assets/detect2.mp4"
            os.system(f"ffmpeg -i {save_path} -vcodec libx264 {convert_path}")

            video_file = open(convert_path, "rb")
            video_bytes = video_file.read()

            col1.header("Original")
            col2.header("Detected")
            col1.video(origin_video, format="video/mp4")
            col2.video(video_bytes, format="video/mp4")


if __name__ == "__main__":
    main()
