from time import time

import cv2
import sys
import numpy as np

from PIL import Image
from typing import Generator

def process_frame(file_path : str, detector_model) -> Generator:
    cap = cv2.VideoCapture(file_path)
    start_time = time()
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        frame = detector_model.detect(frame)
        pil_img = Image.fromarray(frame[0].plot()[..., ::-1])
        frame = np.array(pil_img)

        elapsed_time = time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
        else:
            fps = 0

        processed_frame = cv2.putText(frame, f"FPS: {fps:.2f}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                      (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

    cap.release()
