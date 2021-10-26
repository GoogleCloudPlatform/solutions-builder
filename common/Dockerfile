# changed from slim for FireO
FROM python:3.7-slim

WORKDIR /opt


# needed for backports-datetime-fromisoformat in fireo
RUN apt-get update
RUN apt-get -y install gcc

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .
