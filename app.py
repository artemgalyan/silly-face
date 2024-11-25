from datetime import datetime, timedelta
from threading import Thread

import cv2

from imutils.video import WebcamVideoStream

from detection import FaceDetectorYunet
from player import VideoPlayer



from detection import FaceDetectorYunet

CHECK_EVERY = 1


def smart_max(l: list[int]) -> int:
    m = max(l)
    if list(sorted(l, reverse=True)) == l:
        return -1

    return m


def main() -> None:
    cv2.namedWindow('X', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('X', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty('X', cv2.WND_PROP_TOPMOST, 1)
    
    face_detector = FaceDetectorYunet()
    stream = WebcamVideoStream()
    stream.start()

    player = VideoPlayer('data/s.mp4')
    thread = Thread(target=player.run, args=(), name='Video')
    thread.daemon = True
    thread.start()

    num_faces = 0
    previous = [num_faces]
    while True:
        frame = stream.read()
        f = cv2.resize(player.frame, (1920, 1080))
        cv2.putText(f, str(num_faces), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('X', f)

        detected = face_detector.detect(frame)
        if detected is None or len(detected) == 0:
            cf = 0
        else:
            cf = len(detected)
        
        if len(previous) < CHECK_EVERY:
            previous.append(cf)
        
        if len(previous) == CHECK_EVERY:
            if not player.playing and max(previous) > num_faces:
                player.start()
            
            num_faces = max(previous)
            previous = []
        
        num_faces = cf
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break

    stream.stop()
    stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
