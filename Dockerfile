FROM python:3.8-alpine@sha256:2f465e6659fdf5ed8c9d485cada123fd3db18966191fd5a1e78dcbc488e82126
WORKDIR /opt/app
COPY . .
RUN ["pip", "install", "pip", "--upgrade"]
RUN ["pip", "install", "-r", "requirements.txt"]
ENV APP_DB_CONNECTION_STRING=
ENV APP_LOOP_INTERVAL_SECONDS="3"
CMD ["python", "main.py"]