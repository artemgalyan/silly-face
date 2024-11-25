from time import sleep
from datetime import datetime, timedelta

import cv2

from ffpyplayer.player import MediaPlayer


class VideoPlayer:
    def __init__(self, path: str):
        self.path = path

        self.playing = False
        video = cv2.VideoCapture(path)

        self.fps = video.get(cv2.CAP_PROP_FPS)
        self.duration = timedelta(seconds=1. / self.fps)
        
        self.frames = []
        cap, frame = video.read()
        while cap:
            self.frames.append(frame)
            cap, frame = video.read()
        
        video.release()

        self.frame = self.frames[0]
        
    def run(self):
        while True:
            while not self.playing:
                self.frame = self.frames[0]

            player = MediaPlayer(self.path)
            while True:
                audio_frame, val = player.get_frame()
                
                if val != 'eof' and audio_frame is not None:
                    img, t = audio_frame
                else:
                    break

            for frame in self.frames:
                last_time = datetime.now()
                self.frame = frame
                now = datetime.now()
                if now - last_time < self.duration:
                    d = now - last_time
                    sleep(self.duration.total_seconds() - d.total_seconds())


            player.close_player()
            self.playing = False

    def start(self) -> None:
        self.playing = True