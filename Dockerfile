# استخدم Python 3.9 أو 3.10 (حسب الحاجة)
FROM python:3.10

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ جميع الملفات إلى الحاوية
COPY . /app

# تحديث pip قبل تثبيت المتطلبات
RUN pip install --upgrade pip

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل التطبيق
CMD ["python", "main.py"]