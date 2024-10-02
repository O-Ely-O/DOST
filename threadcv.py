import cv2
import threading
from threading import Thread
import time

class SpeedmeUp:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.fps = self.stream.get(cv2.CAP_PROP_FPS)
        self.delay = 1 / self.fps if self.fps > 0 else 0 # Calculate delay based on fps
        (self.grabbed, self.frame) = self.stream.read()
        self.frame = None
        self.stopped = False
        self.lock = threading.Lock()
    
    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.stopped:
            with self.lock:
                grabbed, self.frame = self.stream.read()
                if not grabbed:
                    print("Frame not grabbed. Reinitializing stream...")
                    self.stop()
            # Introduce a delay to control playback speed
            time.sleep(self.delay)  # Introduce a delay to control playback speed

    def restart(self):
        """Restart the video stream."""
        self.stop()
        time.sleep(1)
        self.start()
        
    def read(self):
        with self.lock:
            return self.frame
    
    def stop(self):
        self.stopped=True
        self.stream.release()  # Release the stream when stopping