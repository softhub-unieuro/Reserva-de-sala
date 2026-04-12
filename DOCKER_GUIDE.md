# Guia de Homologacao com Docker Compose

Este projeto agora possui automacao para subir o ambiente de homologacao com PostgreSQL + Django.

## Arquivos criados

- `docker-compose.yml`
- `Dockerfile`
- `subir.sh` (atalho na raiz)
- `subir.ps1` (atalho na raiz)
- `ops/homologacao/subir_ambiente.sh`
- `ops/homologacao/subir_ambiente.ps1`

## Pre-requisitos

- Docker
- Docker Compose (`docker-compose`)
- Bash (Git Bash, WSL ou Linux/macOS) para usar `.sh`
- PowerShell para usar `.ps1` no Windows

Variaveis obrigatorias no `.env`:

- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_DATABASE`
- `DB_HOST` (opcional, sera sobrescrito para `db` no container web)
- `DB_PORT` (opcional, sera sobrescrito para `5432` no container web)

## 1) Dar permissao de execucao no script

### Windows (PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\subir.ps1
```

### Linux/macOS/WSL (bash)

```bash
chmod +x subir.sh ops/homologacao/subir_ambiente.sh
./subir.sh
```

O script:

- valida se existe `SECRET_KEY` no `.env`
- gera uma chave segura automaticamente se estiver vazia/ausente
- executa `docker-compose up --build -d`
- roda no container `web`:
  - `python manage.py migrate`
  - `python manage.py collectstatic --noinput`
  - `python manage.py setup_usuarios`

## 3) Como acessar logs

Logs de todos os servicos:

```bash
docker-compose logs -f
```

Logs apenas do Django (`web`):

```bash
docker-compose logs -f web
```

Logs apenas do banco (`db`):

```bash
docker-compose logs -f db
```

## 4) Credenciais padrao

Baseado no `.env.example` informado:

- Matricula: `777777`
- Senha: `SenhaSegura777!`

## Observacao de banco

No `docker-compose.yml`, o Django recebe `DB_HOST=db` e `DB_PORT=5432`, garantindo conexao ao servico PostgreSQL interno do Compose.
