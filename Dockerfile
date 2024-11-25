FROM python:3-alpine

ENV ETHM_HOST=localhost
ENV ETHM_PORT=7094

WORKDIR /app

COPY requirements.txt app.py  /app
COPY satel_integra2 /app/satel_integra2


RUN pip3 install -r /app/requirements.txt


ENTRYPOINT ["python3", "app.py"]
