#!/bin/bash
set -e

echo "⏳ Aguardando o PostgreSQL ficar pronto..."
until python -c "
import psycopg2, os, sys
try:
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ.get('DB_PORT', '5432'),
        connect_timeout=3,
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f'   Aguardando: {e}')
    sys.exit(1)
"; do
    sleep 2
done
echo "✅ PostgreSQL está pronto!"

echo "📦 Executando migrações..."
python manage.py migrate --noinput

echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "👤 Configurando usuários e permissões..."
python manage.py setup_usuarios || echo "⚠️  setup_usuarios já executado ou falhou (ignorando)"

echo "🚀 Iniciando o servidor na porta 8001..."
exec python manage.py runserver 0.0.0.0:8001
