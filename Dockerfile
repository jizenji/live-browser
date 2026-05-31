FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask

WORKDIR /app
COPY stream-server.py .

EXPOSE 8080

CMD ["python3", "stream-server.py"]
