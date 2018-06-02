FROM nginx:alpine

EXPOSE 80

# Install package dependencies
RUN apk add --update python3 python3-dev gcc make libc-dev libffi-dev linux-headers git vim 

# Install requirements
RUN mkdir -p /opt/arsenal-c2/
COPY requirements.txt /opt/arsenal-c2/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/arsenal-c2/requirements.txt

# Copy files
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY server /opt/arsenal-c2/server
COPY run.py /opt/arsenal-c2/run.py
COPY docker/uwsgi.ini /opt/arsenal-c2/uwsgi.ini
COPY docker/arsenal_key /opt/arsenal-c2/.arsenal_key
COPY docker/slack_key /opt/arsenal-c2/.slack_key

# Configure ENTRYPOINT
COPY docker/entrypoint.sh /opt/arsenal-c2/entrypoint.sh
RUN chmod 0755 /opt/arsenal-c2/entrypoint.sh
ENTRYPOINT ["/opt/arsenal-c2/entrypoint.sh"]
