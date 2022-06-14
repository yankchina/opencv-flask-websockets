# -*- coding: utf-8 -*-
import threading
import time

import cv2

class RtspStream:
    def __init__(self, rtsp_stream_url):
        print('rtspstream')
        self.thread = None
        self.current_frame  = None
        self.last_access = None
        self.is_running: bool = False
        self.rtsp_stream_url = rtsp_stream_url
        # self.stream = cv2.VideoCapture(rtsp_stream_url)
        self.stream = cv2.VideoCapture(0)
        if not self.stream.isOpened():
            raise Exception("Could not open rtsp stream url {0}".format(rtsp_stream_url))

    def __del__(self):
        self.stream.release()

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()

    # def get_frame(self):
    #     self.last_access = time.time()
    #     return self.current_frame
    
    def get_frame(self):
        cap = cv2.VideoCapture(0)
        frame = None
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                ret, encoded = cv2.imencode(".jpg",frame)
                if ret:
                    frame = encoded
                    print("END ENCODED")
        return frame

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.thread = None

    def _capture(self):
        self.is_running = True
        self.last_access = time.time()
        while self.is_running:
            time.sleep(0.1)
            ret, frame = self.stream.read()
            if ret:
                # print("Capture OK!")
                ret, encoded = cv2.imencode(".jpg", frame)
                if ret:
                    # print("Frame Encoding", encoded)
                    self.current_frame = encoded
                else:
                    print("Failed to encode frame")
            else:
                print("Failed to capture frame")
        print("Reading thread stopped")
        self.thread = None
        self.is_running = False
