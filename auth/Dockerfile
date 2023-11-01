FROM python:3

ENV IN_DOCKER="True"
ENV DOCKER_HOST="host.docker.internal"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 9000
ENTRYPOINT ["gunicorn", "main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9000", "--access-logfile", "-"]
