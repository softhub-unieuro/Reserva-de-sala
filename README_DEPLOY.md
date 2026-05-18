Deploy.md


MANUAL DE DEPLOY - SISTEMA DE RESERVA DE SALAS


PRÉ-REQUISITOS DO SERVIDOR:
- Docker e Docker Compose instalados (Recomendado).
- OU Python 3.10+ e PostgreSQL.


OPÇÃO 1: DEPLOY COM DOCKER (RECOMENDADO)

O projeto já está configurado com Docker, o que facilita o deploy em qualquer servidor.

1. **Configurar Variáveis**: Duplique o arquivo `.env.example` para `.env` e ajuste as credenciais (ADMIN_MATRICULA, ADMIN_SENHA, etc.).
2. **Subir os Containers**:
   > docker compose up -d --build
3. **Acesso**: O sistema estará disponível em `http://localhost:8001`.

*O Docker cuida automaticamente das migrações, coleta de arquivos estáticos e criação do usuário inicial.*


OPÇÃO 2: DEPLOY MANUAL (LEGADO)


PASSO 1: CONFIGURAÇÃO DO AMBIENTE

1. Na pasta raiz, duplique o arquivo `.env.example` e renomeie para `.env`.
2. Abra o arquivo `.env` e preencha TODAS as variáveis solicitadas:
   - Dados de Conexão do Banco (DATABASE_URL)
   - Chave de Segurança (SECRET_KEY)
   - Domínios Permitidos (ALLOWED_HOSTS)
   - Configurações de E-mail (SMTP)
   - Dados do Administrador Inicial (ADMIN_MATRICULA, ADMIN_SENHA, etc.)
3. Certifique-se de que DEBUG=False no arquivo .env.

PASSO 2: INSTALAÇÃO DAS DEPENDÊNCIAS

No terminal, dentro da pasta do projeto (com virtualenv ativo, se houver):

> pip install -r requirements.txt

PASSO 3: BANCO DE DADOS E CONFIGURAÇÃO INICIAL

É necessário criar a estrutura do banco, preparar os arquivos estáticos e criar o primeiro acesso.
Execute os comandos na ordem abaixo:

1. Criar tabelas no banco de dados:
   > python manage.py migrate

2. Compilar arquivos estáticos (CSS/JS/Imagens):
   > python manage.py collectstatic --noinput

3. Configurar Permissões, Grupos e Criar o Superusuário:
   (Este comando usa os dados ADMIN_ preenchidos no .env)
   > python manage.py setup_usuarios

   *Se der tudo certo, você verá a mensagem "Configuração concluída".*

PASSO 4: RODAR O SERVIDOR DE APLICAÇÃO

O projeto utiliza 'waitress' como servidor WSGI (recomendado para Windows). Para ambientes Linux, recomenda-se o uso do Gunicorn (já configurado no Procfile).

Comando para Windows (Waitress):
> waitress-serve --listen=*:8000 project.wsgi:application

Comando para Linux (Gunicorn): 
> gunicorn project.wsgi --log-file -

Nota para TI: Recomenda-se configurar esse comando para rodar como serviço (Systemd no Linux ou Windows Service) para garantir que o sistema reinicie automaticamente caso o servidor desligue.


OBSERVAÇÃO CRÍTICA SOBRE HTTPS/SSL

O sistema está configurado para forçar HTTPS por segurança. 
Certifique-se de que o Load Balancer, Proxy Reverso ou Gateway (Nginx/IIS/Apache) esteja configurado para repassar o cabeçalho 'X-Forwarded-Proto'.

Sem esse cabeçalho, o sistema pode entrar em loop de redirecionamento.
