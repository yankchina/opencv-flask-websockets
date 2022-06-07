#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64

from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit

from rtspstream import RtspStream

app = Flask(__name__)
socketio = SocketIO(app)

stream = RtspStream("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4")


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


@socketio.on("request-frame", namespace="/stream-feed")
def stream_frame_requested(message):
    frame = stream.get_frame()
    if frame is not None:
        emit("new-frame", {
            "base64": base64.b64encode(frame).decode("ascii")
        })


if __name__ == "__main__":
    try:
        stream.start()
        print("stream is started.")
        socketio.run(app, host="0.0.0.0", port=8080)
        print("flask app is open")
    except KeyboardInterrupt:
        stream.stop()

