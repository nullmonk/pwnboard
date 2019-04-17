FROM alpine:latest

EXPOSE 5000

# Install package dependencies
RUN apk add --update python3 uwsgi
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

# Install requirements
RUN mkdir -p /opt/pwnboard/
COPY . /opt/pwnboard/

# Build the board file if one isnt given
RUN /bin/sh scripts/setup.sh

CMD ["uwsgi", "--yaml", "/opt/pwnboard/config/wsgi.yml"]
