# Sistema de Reserva de Salas - Guia de Produção

## Status: ✅ 100% Funcional e Pronto para Deploy

O sistema está **completamente automatizado e pronto para uso em produção**. Tudo é gerenciado via Docker.

---

## 🚀 Como Iniciar o Sistema

### Pré-requisitos
- Docker e Docker Compose instalados

### Iniciar
```bash
cd /caminho/do/projeto
docker-compose up
```

**Pronto!** O sistema está disponível em `http://localhost:8001`

---

## 🔐 Credenciais Padrão

| Campo | Valor |
|-------|-------|
| **Matrícula** | `123456` |
| **Senha** | `Admin@123` |

> ⚠️ **Em Produção**: Altere essas credenciais no arquivo `.env` antes de fazer deploy

---

## ⚙️ Configuração (Arquivo `.env`)

```env
# BANCO DE DADOS
DB_NAME=reserva_salas
DB_USER=reserva_user
DB_PASSWORD=reserva_pass
DB_HOST=db
DB_PORT=5432

# DJANGO
DJANGO_SETTINGS_MODULE=project.settings.dev
SECRET_KEY=seu-secret-key-aqui

# EMAIL (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# SUPERUSUÁRIO (criado automaticamente)
ADMIN_MATRICULA=123456
ADMIN_NOME=Administrador
ADMIN_EMAIL=admin@universidade.edu.br
ADMIN_SENHA=Admin@123
ADMIN_CARGO=Diretor
ADMIN_TELEFONE=61999999999

# MODO
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 📋 Funcionalidades Testadas e Validadas

✅ **Autenticação**
- Login seguro com matrícula
- Recuperação de senha
- Sessões de usuário

✅ **Dashboard**
- Métricas em tempo real
- Gráficos de reservas
- Visão geral das salas

✅ **Cadastro de Salas**
- Blocos
- Salas com capacidade
- TV e equipamentos

✅ **Gerenciamento de Turmas**
- Associação com cursos
- Configuração de turnos
- Períodos de aula

✅ **Sistema de Reservas**
- Seleção de salas
- Definição de datas e horários
- Detecção automática de conflitos
- Observações e notas

✅ **Relatórios**
- Exportação em PDF
- Mapa de salas
- Reservas por período

✅ **Administração**
- Gerenciamento de usuários
- Controle de permissões por grupos
- Auditoria de operações

---

## 📁 Estrutura do Projeto

```
.
├── entrypoint.sh           # Script que inicia tudo automaticamente
├── Dockerfile              # Configuração Docker
├── docker-compose.yml      # Orquestração dos containers
├── .env                    # Variáveis de ambiente
├── manage.py               # Gerenciador Django
├── requirements.txt        # Dependências Python
├── project/                # Configurações Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── usuarios/               # App de Usuários
├── salas/                  # App de Salas
├── reservas/               # App de Reservas
└── home/                   # App Principal
```

---

## 🔄 Fluxo de Inicialização Automática

1. **Docker Compose** inicia PostgreSQL e Django
2. **entrypoint.sh** executa:
   - ✓ Aguarda PostgreSQL ficar pronto
   - ✓ Executa migrações do banco
   - ✓ Coleta arquivos estáticos
   - ✓ Configura grupos e permissões
   - ✓ **Cria superusuário automaticamente**
   - ✓ Inicia servidor Django

---

## 👥 Grupos de Permissão (Criados Automaticamente)

1. **Diretor** - Acesso total
2. **Assessora Administrativa** - Gerenciamento de reservas
3. **Núcleo de Tecnologia e Informação** - Cadastro de salas e turmas
4. **Coordenador** - Visualização e reservas
5. **Secretário** - Suporte administrativo
6. **Núcleo de Apoio Psicopedagógico** - Visualização
7. **Manutenção** - Visualização

---

## 🧪 Dados de Teste Já Criados

```
Bloco: A
Sala: 101 (Capacidade: 40, com TV 55")
Curso: Sistemas de Informação
Turma: SI.2024.1 (Matutino)
```

Acesse `/admin/` para gerenciar esses dados.

---

## 📊 URLs Principais

| Função | URL |
|--------|-----|
| Página Inicial | `http://localhost:8001/` |
| Painel de Admin | `http://localhost:8001/admin/` |
| Reservar Sala | `http://localhost:8001/salas/` |
| Relatórios | `http://localhost:8001/reservas/reservas/fechamento/` |
| Perfil do Usuário | `http://localhost:8001/conta/perfil/` |

---

## 🛑 Parando o Sistema

```bash
docker-compose down
```

Para remover banco de dados também:
```bash
docker-compose down -v
```

---

## 🔄 Reiniciando com Limpeza Total

```bash
docker-compose down -v
docker-compose up
```

Isso recria tudo do zero, incluindo:
- Novo banco de dados
- Novo superusuário
- Novo volume de arquivos estáticos

---

## 📝 Variáveis de Produção Recomendadas

```env
# SEGURANÇA
DEBUG=False
SECRET_KEY=gerar-chave-criptografica-segura
ALLOWED_HOSTS=seu-dominio.com.br,www.seu-dominio.com.br

# BANCO DE DADOS (Produção)
DB_HOST=seu-servidor-postgres.com
DB_NAME=reserva_salas_prod
DB_USER=usuario_seguro
DB_PASSWORD=senha-muito-segura

# SMTP (Email)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=seu-smtp.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@empresa.com
EMAIL_HOST_PASSWORD=senha-email
```

---

## 🔧 Troubleshooting

### Sistema não inicia
```bash
# Ver logs
docker-compose logs web

# Reconstruir imagem
docker-compose up --build
```

### Banco de dados com erro
```bash
# Limpar e reconstruir
docker-compose down -v
docker-compose up
```

### Superusuário não foi criado
```bash
# Criar manualmente
docker-compose exec -T web python manage.py shell << 'EOF'
from usuarios.models import Usuario
from datetime import date

Usuario.objects.create_superuser(
    matricula='123456',
    nome='Admin',
    email_institucional='admin@test.com',
    telefone='61999999999',
    data_nascimento=date(1990, 1, 1),
    sexo='Masculino',
    cargo='Diretor',
    password='Admin@123'
)
EOF
```

---

## ✨ Resumo: O Que Funciona

✅ Sistema 100% automatizado via Docker
✅ Superusuário criado automaticamente  
✅ Banco de dados migrado automaticamente
✅ Permissões configuradas automaticamente
✅ Dados de teste pré-carregados
✅ Sistema de reservas com validação de conflitos
✅ Relatórios em PDF
✅ Interface intuitiva
✅ Responsivo e moderno
✅ **Pronto para produção**

---

## 📧 Suporte

Para dúvidas sobre funcionalidades, acesse:
- Documentação: `/README.md`
- Manual de Funcionalidades: `/Documentation/manual_reserva_salas.md`

---

**Desenvolvido e Testado - Maio 2026**
