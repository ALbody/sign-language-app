from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import pyttsx3
import threading
import time

app = Flask(__name__)
CORS(app)

engine = pyttsx3.init()
engine.setProperty('rate', 150)

net = cv2.dnn_DetectionModel('frozen_inference_graph.pb', 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
net.setInputSize(320, 230)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

with open('coco.names', 'rt') as f:
    class_names = f.read().rstrip('\n').split('\n')

@app.route("/")
def index():
    return jsonify({"message": "Server is running"})

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    def run():
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run, daemon=True).start()

def generate_frames():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("❌ Failed to open the camera")
        return

    last_speak_time = time.time()
    last_spoken_objects = set()
    last_empty_time = time.time()
    object_last_seen = {}

    while True:
        success, frame = cam.read()
        if not success:
            print("❌ Failed to read frame")
            break

        class_ids, confs, bbox = net.detect(frame, confThreshold=0.5)

        detected_objects = set()
        current_time = time.time()

        if len(class_ids) != 0:
            for class_id, confidence, box in zip(class_ids.flatten(), confs.flatten(), bbox):
                label = class_names[class_id - 1]
                detected_objects.add(label)
                object_last_seen[label] = current_time

                cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if not detected_objects:
            last_empty_time = current_time

        new_objects = detected_objects - last_spoken_objects
        reappeared_objects = {obj for obj in detected_objects if current_time - object_last_seen.get(obj, 0) > 1}

        if (new_objects or reappeared_objects) and (current_time - last_speak_time > 1):
            spoken_text = ", ".join(detected_objects)
            speak(spoken_text)
            last_spoken_objects = detected_objects
            last_speak_time = current_time

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cam.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)