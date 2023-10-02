from imutils.video import VideoStream
from flask import Response, Flask
import threading
import imutils
import time
import cv2
from service import detect_eye


outputFrame = None
lock = threading.Lock()
app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    t = threading.Thread(target=detect_eye, args=(32,))
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=8032, debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
