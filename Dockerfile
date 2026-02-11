FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Ee line valla app, scripts anni container loki velthayi
COPY . . 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]