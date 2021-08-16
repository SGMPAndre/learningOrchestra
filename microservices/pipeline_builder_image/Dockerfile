FROM python:3.7-slim

WORKDIR /usr/src/database_api
COPY . /usr/src/database_api
RUN pip install -r requirements.txt

ENV MICROSERVICE_IP "0.0.0.0"
ENV MICROSERVICE_PORT_VALUE 5000

ENV DATASET_VOLUME_PATH "/pipeline_builder"

CMD ["python", "server.py"]