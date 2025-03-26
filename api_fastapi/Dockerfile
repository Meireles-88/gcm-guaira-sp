FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn python-multipart psycopg2-binary
CMD ["uvicorn", "emergencia.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
