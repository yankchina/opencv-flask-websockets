# -*- coding: utf-8 -*-
import threading
import time
import cv2
from yolov5 import YOLOv5

yolov5_model_path = u'./models/yolov5n.pt'
frame_encoding_type = u".png"

class RtspStream:
    def __init__(self, rtsp_stream_url):
        self.thread = None
        self.current_frame  = None
        self.last_access = None
        self.is_running: bool = False
        self.rtsp_stream_url = rtsp_stream_url
        # self.stream = cv2.VideoCapture(rtsp_stream_url)
        self.stream = cv2.VideoCapture(0)
        self.model = YOLOv5(model_path=yolov5_model_path,device=u"cpu")
        if not self.stream.isOpened():
            raise Exception("Could not open rtsp stream url {0}".format(rtsp_stream_url))
        else:
            self.start()

    def __del__(self):
        self.stream.release()

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()

    def get_frame(self):
        self.last_access = time.time()
        return self.current_frame

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.thread = None

    def _capture(self):
        self.is_running = True
        self.last_access = time.time()
        while self.is_running:
            ret, frame = self.stream.read()
            if ret:
                results = self.model.predict(frame)
                results.render()
                ret, encoded = cv2.imencode(frame_encoding_type, frame)
                if ret:
                    self.current_frame = encoded
                else:
                    print("Failed to encode frame")
            else:
                print("Failed to capture frame")
        print("Reading thread stopped")
        self.thread = None
        self.is_running = False