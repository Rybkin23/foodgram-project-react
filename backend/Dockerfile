FROM python:3.9.10-slim
WORKDIR /app
COPY ../ ./
RUN pip install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]