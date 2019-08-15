FROM python:3.6-alpine

COPY logic_server.py requirements.txt /home/app/

RUN adduser -D -h /home/app app && pip3 install -r /home/app/requirements.txt

WORKDIR /home/app

USER app

ENTRYPOINT ["python3", "logic_server.py"]
