FROM python:3-alpine

ENV FLASK_APP=main.py

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD [ "python3", "main.py" ]