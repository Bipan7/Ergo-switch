import cv2


class Camera:
    def __init__(self, cam_id=0, width=680, height=480):
        self.cap = cv2.VideoCapture(cam_id)
        self.width = width
        self.height = height

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def start(self):
        if not self.cap.isOpened():
            self.cap.open(0)

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return False, None

        frame = cv2.resize(frame, (self.width, self.height))
        return True, frame

    def capture(self):
        ret, frame = self.read()
        return frame if ret else None

    def stop(self):
        if self.cap.isOpened():
            self.cap.release()