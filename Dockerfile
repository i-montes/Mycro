FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev libpq-dev python3-eventlet

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN pip3 install --user eventlet

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "-c", "config/server.py", "main:app", "--threads=4"]