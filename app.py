#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
from rtspstream import RtspStream


stream = RtspStream("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')
    
# socket.emit('request frame',{});  -> ME
# ME -> socket.on('redraw frame', function (msg) {});
@socketio.on('request frame')
def redraw(message):
    frame = stream.get_frame()
    if frame is not None:
        emit('redraw frame',{
            "base64": base64.b64encode(frame).decode("ascii")
        })
    else:
        emit('empty frame'),{
            "message": "empty"
        }

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
