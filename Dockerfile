FROM python:3.5
ADD . /pairing_service
WORKDIR /pairing_service
RUN pip install -r requirements.txt