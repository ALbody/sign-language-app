from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import os

app = Flask(__name__)
CORS(app)  # تفعيل CORS للسماح بالاتصال بين الفرونت والباك

# 📡 Route رئيسي للتأكد إن السيرفر شغال
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Backend is working with real-time analysis!"})

# 🎥 دالة لبث الفيديو مع تحليل الكائنات
def generate_frames():
    cam = cv2.VideoCapture(0)

    # تحميل نموذج الكشف عن الكائنات
    net = cv2.dnn_DetectionModel('frozen_inference_graph.pb', 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
    net.setInputSize(320, 230)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    # تحميل أسماء الكائنات
    with open('coco.names', 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    while True:
        success, frame = cam.read()
        if not success:
            print("Failed to grab frame")
            break

        # تحليل الفيديو واكتشاف الكائنات
        classIds, confs, bbox = net.detect(frame, confThreshold=0.5)

        # رسم الصناديق حول الكائنات
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, classNames[classId - 1], (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # تحويل الصورة لـ JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # بث الفيديو
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cam.release()

# 🌐 Route لبث الفيديو
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 🚀 تشغيل السيرفر
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
