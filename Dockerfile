# استخدم Python 3.10 كبيئة تشغيل
FROM python:3.10

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ جميع الملفات إلى الحاوية
COPY . /app

# تحديث الحزم وتثبيت المكتبة المفقودة لحل مشكلة OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# تحديث pip قبل تثبيت المتطلبات
RUN pip install --upgrade pip

# تثبيت المتطلبات من requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل التطبيق
CMD ["python", "main.py"]

CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]