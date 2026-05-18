FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
# Convert requirements.txt from UTF-16 to UTF-8 if needed, then install
RUN python3 -c "data=open('requirements.txt','rb').read(); \
    open('requirements.txt','w').write(data.decode('utf-16') if data[:2] in [b'\xff\xfe', b'\xfe\xff'] else data.decode('utf-8-sig'))"
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN DJANGO_SETTINGS_MODULE=project.settings.dev \
    SECRET_KEY=build-placeholder \
    DB_NAME=x DB_USER=x DB_PASSWORD=x DB_HOST=x DB_PORT=5432 \
    python manage.py collectstatic --noinput 2>/dev/null || true

# Expose port
EXPOSE 8001

# Entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
