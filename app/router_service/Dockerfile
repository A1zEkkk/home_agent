FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY app/router_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/router_service ./router_service

EXPOSE 8000

CMD ["uvicorn", "router_service.main:app", "--host", "0.0.0.0", "--port", "8000"]