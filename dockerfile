FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5002", "app:app"]