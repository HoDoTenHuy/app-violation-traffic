import cv2
import logging

logger = logging.getLogger(__name__)


class VideoPlayer:
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.video_cap = cv2.VideoCapture(video_path)
        if not self.video_cap.isOpened():
            logger.error('event={} message="{}"'.format('open-video-failure', 'Error opening video stream or file.'))
            self.video_cap = None
            return
        self.fps = int(self.video_cap.get(cv2.CAP_PROP_FPS))
        self.cv_wait_time = int(1000 / self.fps)
        self.width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.nfames = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        logger.critical('event={} message="{}"'.format('inited-video-capture',
                                                       'inited video capture \"{}\" | FPS: {} | Resolution: {}x{}'
                                                       .format(video_path, self.fps,
                                                               self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                                                               self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    def get_frame(self):
        ret, frame = self.video_cap.read()
        return ret, frame

    def reset(self):
        self.video_cap.release()
        self.video_cap = cv2.VideoCapture(self.video_path)

    def __del__(self):
        if self.video_cap is not None:
            self.video_cap.release()
