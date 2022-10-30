FROM python:3.10

WORKDIR /home

ENV TELEGRAM_API_TOKEN="5366559478:AAFg40_LRnitgrRxSn2olbkGmSoB9LaYsao"
ENV TELEGRAM_ACCESS_ID="497469498"


ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "server.py"]

