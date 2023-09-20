from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def find_camera(id):
    cameras = [
        'rtsp://user01:ketiabcs@192.168.1.37:554/h264Preview_01_sub',
        'rtsp://user01:ketiabcs@192.168.1.38:554/h264Preview_01_sub',
        'rtsp://user01:ketiabcs@192.168.1.37:554/h264Preview_01_main',
        'rtsp://user01:ketiabcs@192.168.1.38:554/h264Preview_01_main']
    return cameras[int(id)]

def gen_frames(camera_id):
     
    cam = find_camera(camera_id)
    cap=  cv2.VideoCapture(cam)
    
    while True:
        # for cap in caps:
        # # Capture frame-by-frame
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
   
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010)