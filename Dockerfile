FROM python:3.8

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && apt-get install -y python3 \
    python3-dev \
    python3-pip \
    python3-setuptools

RUN mkdir -p /usr/workspace/mongo/media/{log}

WORKDIR /usr/workspace/mongo

COPY requirements.txt /usr/workspace/mongo/

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

RUN pip install uwsgi

RUN apt-get update && apt-get install -y nginx

RUN mkdir -p /etc/uwsgi/vassals

COPY . /usr/workspace/mongo/

RUN ln -s /usr/workspace/mongo/uwsgi/mongo.ini /etc/uwsgi/vassals/

RUN mv -f /usr/workspace/mongo/nginx/default /etc/nginx/sites-available/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]
