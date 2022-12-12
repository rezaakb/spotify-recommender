FROM python:3.6-alpine
LABEL MAINTAINER="reza.akb98@gmail.com"

RUN pip3 install --upgrade redis jsonpickle requests flask scikit-learn pandas pymongo google-cloud-storage

WORKDIR /
COPY    worker-server.py /
CMD [ "python3", "worker-server.py"]
