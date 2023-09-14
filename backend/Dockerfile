FROM python:3.9.10-slim
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y libpq-dev gcc netcat
WORKDIR /app
COPY ../ ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get update && apt -y install mc
RUN python manage.py collectstatic --no-input
RUN mkdir backend_static/

RUN cp -r /app/collected_static/. /app/backend_static/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]
#RUN chmod +x run_app.sh
#ENTRYPOINT [ "/app/run_app.sh" ]
