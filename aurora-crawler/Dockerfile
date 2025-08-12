FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends bash ca-certificates && rm -rf /var/lib/apt/lists/*
COPY ./aurora-crawler /app
CMD ["bash","-lc","trap : TERM INT; sleep infinity & wait"]
