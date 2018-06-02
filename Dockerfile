FROM nginx:alpine

EXPOSE 80
EXPOSE 443

# Install package dependencies
RUN apk add --update python3 nginx uwsgi redis

# Install requirements
RUN mkdir -p /var/www/pwnboard/
RUN mkdir -p /
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

