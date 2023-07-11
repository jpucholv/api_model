FROM python:3.11.1
WORKDIR /app
COPY app_model_db.py .
COPY requirements.txt .
COPY /data /data
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
EXPOSE 5000
CMD ["python", "app_model_db.py"]