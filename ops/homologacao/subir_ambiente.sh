#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"

cd "$PROJECT_ROOT"

if [ ! -f "$ENV_FILE" ]; then
  touch "$ENV_FILE"
fi

require_env_var() {
  local key="$1"
  local value
  value="$(grep -E "^[[:space:]]*${key}[[:space:]]*=" "$ENV_FILE" | tail -n 1 | sed -E "s/^[[:space:]]*${key}[[:space:]]*=[[:space:]]*//")"
  value="${value%\"}"
  value="${value#\"}"
  value="${value%\'}"
  value="${value#\'}"

  if [ -z "$value" ]; then
    echo "Erro: variavel ${key} nao encontrada ou vazia em ${ENV_FILE}." >&2
    exit 1
  fi
}

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Erro: Python nao encontrado para gerar SECRET_KEY." >&2
  exit 1
fi

existing_secret="$(grep -E '^[[:space:]]*SECRET_KEY[[:space:]]*=' "$ENV_FILE" | tail -n 1 | sed -E 's/^[[:space:]]*SECRET_KEY[[:space:]]*=[[:space:]]*//')"
existing_secret="${existing_secret%\"}"
existing_secret="${existing_secret#\"}"
existing_secret="${existing_secret%\'}"
existing_secret="${existing_secret#\'}"

if [ -z "$existing_secret" ]; then
  generated_secret="$($PYTHON_BIN - <<'PY'
import secrets
print(secrets.token_urlsafe(64))
PY
)"

  temp_file="$(mktemp)"
  awk -v new_secret="$generated_secret" '
    BEGIN { updated = 0 }
    /^[[:space:]]*SECRET_KEY[[:space:]]*=/ {
      if (updated == 0) {
        print "SECRET_KEY=" new_secret
        updated = 1
      }
      next
    }
    { print }
    END {
      if (updated == 0) {
        print "SECRET_KEY=" new_secret
      }
    }
  ' "$ENV_FILE" > "$temp_file"
  mv "$temp_file" "$ENV_FILE"
  echo "SECRET_KEY gerada e salva no .env"
fi

require_env_var "DB_USERNAME"
require_env_var "DB_PASSWORD"
require_env_var "DB_DATABASE"

docker-compose up --build -d

docker-compose exec -T web python manage.py migrate
docker-compose exec -T web python manage.py collectstatic --noinput
docker-compose exec -T web python manage.py setup_usuarios

echo "Ambiente de homologacao pronto."
