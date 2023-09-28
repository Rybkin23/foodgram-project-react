FROM python:3.9.10-slim

WORKDIR /app
COPY ../ ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN python manage.py collectstatic --no-input
RUN mkdir backend_static/
RUN cp -r /app/collected_static/. /app/backend_static/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]