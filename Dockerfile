FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# Normalizes requirements encoding because the repository file may be UTF-16.
RUN python - <<'PY'
from pathlib import Path

source = Path('/app/requirements.txt').read_bytes()
for encoding in ('utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1'):
    try:
        text = source.decode(encoding)
    except UnicodeDecodeError:
        continue
    if '\x00' in text:
        continue
    Path('/app/requirements.docker.txt').write_text(text, encoding='utf-8')
    break
else:
    raise RuntimeError('Could not decode requirements.txt with supported encodings.')
PY

RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.docker.txt

COPY . /app

RUN python manage.py collectstatic --noinput --settings project.settings.production

EXPOSE 8000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
