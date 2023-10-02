import cv2
import imutils


def detect_eye(frameCount):

    global vs, outputFrame, lock

    while True:
        # k += 1
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        with lock:
            outputFrame = frame.copy()
