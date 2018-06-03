FROM alpine:latest

EXPOSE 5000

# Install package dependencies
RUN apk add --update python3 uwsgi
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

# Install requirements
RUN mkdir -p /opt/pwnboard/
COPY lib /opt/pwnboard/
COPY pwnboard.py /opt/pwnboard/
COPY config/config.yml /opt/pwnboard/
COPY config/topology.json /opt/pwnboard/
COPY config/wsgi.yml /opt/pwnboard/

CMD ["uwsgi", "--yaml", "/opt/pwnboard/wsgi.yml"]
