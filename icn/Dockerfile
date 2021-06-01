FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

# user modules
RUN pip install tensorflow

CMD ["bash", "./start.sh"]
