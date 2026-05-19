#!/bin/bash
set -e

echo "Aguardando o PostgreSQL ficar pronto..."
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
echo "PostgreSQL esta pronto!"

echo "Executando migracoes..."
python manage.py migrate --noinput

echo "Coletando arquivos estaticos..."
python manage.py collectstatic --noinput

echo "Configurando usuarios e permissoes..."
python manage.py setup_usuarios || echo "setup_usuarios ja executado (ignorando)"

echo "Criando superusuario inicial..."
python manage.py shell << 'SHELL_EOF'
from usuarios.models import Usuario
from datetime import date
import os

matricula = os.getenv('ADMIN_MATRICULA', '123456')
nome = os.getenv('ADMIN_NOME', 'Administrador')
email = os.getenv('ADMIN_EMAIL', 'admin@universidade.edu.br')
telefone = os.getenv('ADMIN_TELEFONE', '61999999999')
cargo = os.getenv('ADMIN_CARGO', 'Diretor')
senha = os.getenv('ADMIN_SENHA', 'Admin@123')

try:
    if not Usuario.objects.filter(matricula=matricula).exists():
        Usuario.objects.create_superuser(
            matricula=matricula,
            nome=nome,
            email_institucional=email,
            telefone=telefone,
            data_nascimento=date(1990, 1, 1),
            sexo='Masculino',
            cargo=cargo,
            password=senha
        )
        print("")
        print("=" * 60)
        print("SUPERUSUARIO CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"Matricula: {matricula}")
        print(f"Senha: {senha}")
        print(f"Email: {email}")
        print(f"Acesse: http://localhost:8001")
        print("=" * 60)
        print("")
    else:
        print(f"INFO: Superusuario {matricula} ja existe")
except Exception as e:
    print(f"AVISO: Erro ao criar superusuario: {e}")
SHELL_EOF

echo "Iniciando o servidor na porta 8001..."
exec python manage.py runserver 0.0.0.0:8001
