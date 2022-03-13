FROM python:3.9.10-slim-buster
ARG DEBIAN_FRONTEND=noninteractive
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN mkdir -p /app
WORKDIR /app
ARG HTTP_PORT=8787
ENV HTTP_PORT=$HTTP_PORT
COPY . /app/
EXPOSE $HTTP_PORT
ENTRYPOINT ["bash","./entrypoint.sh"]
CMD []