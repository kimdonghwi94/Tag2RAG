FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install uv
COPY . /app

RUN uv pip install --system 'fastmcp' 'fastapi' 'uvicorn[standard]' 'httpx' 'redis'

CMD ["python", "-m", "server"]
