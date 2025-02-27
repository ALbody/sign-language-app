from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import pyttsx3
import threading
import time
import numpy as np

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

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    def run():
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run, daemon=True).start()

def calculate_distance(box1, box2):
    center1 = (box1[0] + box1[2] // 2, box1[1] + box1[3] // 2)
    center2 = (box2[0] + box2[2] // 2, box2[1] + box2[3] // 2)
    return np.linalg.norm(np.array(center1) - np.array(center2))

def generate_frames():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("❌ Failed to open the camera")
        return

    last_speak_time = time.time()
    object_positions = {}

    while True:
        success, frame = cam.read()
        if not success:
            print("❌ Failed to read frame")
            break

        class_ids, confs, bbox = net.detect(frame, confThreshold=0.5)

        detected_objects = []
        current_time = time.time()

        if len(class_ids) != 0:
            for class_id, confidence, box in zip(class_ids.flatten(), confs.flatten(), bbox):
                label = class_names[class_id - 1]
                detected_objects.append((label, box))

                cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        new_objects = []
        updated_positions = {}

        for label, box in detected_objects:
            found_existing = False
            for prev_label, prev_box in object_positions.items():
                if label == prev_label and calculate_distance(box, prev_box) < 50:
                    found_existing = True
                    updated_positions[label] = box
                    break
            if not found_existing:
                new_objects.append(label)
                updated_positions[label] = box

        if new_objects and (current_time - last_speak_time > 1):
            speak(", ".join(new_objects))
            last_speak_time = current_time

        object_positions = updated_positions

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