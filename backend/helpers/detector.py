import os
import cv2
import logging
import numpy as np
import torch

from ultralytics import YOLO
from PIL import Image

logger = logging.getLogger(__name__)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class ObjectDetectionHelper:
    def __init__(self, config: dict) -> None:
        self.config = config
        if self.config:
            try:
                self.weights_path = self.config.get('weights_path')
                self.conf_thresh = self.config.get('confidence_score')
                self.iou = self.config.get('non_maxima_suppression_threshold')
                self.input_shape = self.config.get('image_size')
                self.show = self.config.get('show_results')
                self.device = self.config.get('device')
                self.save_path = None
                self.status = "Pending"
                self.progress = 0.0
            except KeyError as e:
                logger.critical('event={} message="{}"'.format('load-config-failure',
                                                               'The config file is invalid: {}'.format(e)))
        else:
            logger.critical('event={} message="{}"'.format('load-config-failure', 'The config file is empty.'))

        self.model = self.load_model()

    def load_model(self):
        model = YOLO(self.weights_path)
        if torch.cuda.is_available():
            model.to('cuda')
        return model

    def get_status(self):
        return self.status, self.progress, self.save_path

    def detect(self, image):
        outputs = self.model.predict(image, show=self.show, imgsz=self.input_shape,
                                     conf=self.conf_thresh, iou=self.iou, device=self.device)
        return outputs

    def track(self, video_path, save_path=f"/var/lib/assets/detect1.mp4"):
        logger.info("Start Track")

        camera_player = cv2.VideoCapture(video_path)

        if not camera_player.isOpened():
            logger.error('event={} message="{}"'.format('load-video-failure', 'The video not found!'))
            exit(-1)

        self.status = "In Progress"
        fps = camera_player.get(cv2.CAP_PROP_FPS)
        width = int(camera_player.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera_player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
        nfames = int(camera_player.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            grabbed, frame = camera_player.read()

            if not grabbed:
                break

            frame = self.detect(frame)
            frame_id = 1
            self.progress = (frame_id / nfames) * 100

            if video_path != save_path:
                vid_path = save_path
                if isinstance(camera_player, cv2.VideoWriter):
                    camera_player.release()  # release previous video writer

            pil_img = Image.fromarray(frame[0].plot()[..., ::-1])
            frame = np.array(pil_img)
            out.write(frame)
            frame_id += 1

        self.status = "Success"
        camera_player.release()
        out.release()
        cv2.destroyAllWindows()
