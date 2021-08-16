FROM python:3.7-slim

WORKDIR /usr/src/observer
COPY . /usr/src/observer

RUN pip install -r requirements.txt

ENV MICROSERVICE_NAME "observer"
ENV MICROSERVICE_PORT_VALUE 5010
ENV MICROSERVICE_IP "0.0.0.0"

EXPOSE 5010
CMD ["python", "server.py"]