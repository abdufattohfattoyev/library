# Python bazaviy image
FROM python:3.12-slim

# Ishchi katalog
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani nusxalash
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Port
EXPOSE 8000

# Start komandasi (gunicorn)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
