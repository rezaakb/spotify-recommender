FROM python:3.6-alpine
LABEL MAINTAINER="reza.akb98@gmail.com"

RUN pip3 install --upgrade redis jsonpickle requests flask pymongo spotipy pandas

WORKDIR /
COPY    rest-server.py /
CMD [ "python3", "rest-server.py"]
