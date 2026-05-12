# 📌 Sistema de Reserva de Salas

O sistema tem como objetivo **automatizar a reserva e distribuição de salas de aula** na instituição (UniEuro), substituindo o processo manual realizado atualmente em planilhas.

## 🚀 Visão Geral
- **Sistema web-based** (acessível via navegador).
- Voltado para uso direto da **Assessoria Administrativa** e setores integrados.
- Permite o gerenciamento de reservas **semestrais e avulsas**.
- Elimina conflitos de horário e aprimora a **visualização e gestão** global da infraestrutura de salas.

---

## 🛠️ Stack Tecnológica

O sistema foi desenvolvido utilizando as seguintes tecnologias e bibliotecas principais:

- **Framework Web:** Django 5.2.7
- **Painel Administrativo:** Jazzmin (`django-jazzmin` para uma interface mais amigável e moderna)
- **Banco de Dados:** PostgreSQL (Ambiente de Produção via Docker) / SQLite (Ambiente de Desenvolvimento Local)
- **Servidor de Aplicação:** Gunicorn / Waitress
- **Gerenciamento de Configurações:** `python-dotenv`
- **Geração de Relatórios:** ReportLab (Exportações em PDF)
- **Arquivos Estáticos:** WhiteNoise

---

## ✅ Requisitos Funcionais

- [x] **Cadastro e Gerenciamento de Salas**
  - Informações de Bloco, número, capacidade, presença de TV e pódio.
  - *Restrição:* Apenas o perfil do NTI possui permissão para cadastrar ou editar salas.
- [x] **Cadastro de Turmas**
  - Nome e código da turma, com suporte integrado a turmas mistas.
- [x] **Cadastro de Usuários**
  - Armazenamento de Nome, matrícula, e-mail, telefone, data de nascimento, sexo e cargo.
- [x] **Permissões de Acesso**
  - **Visualização:** Coordenação, Secretarias e Manutenção.
  - **Moderado:** NTI (gestão de salas e turmas).
  - **Total:** Assessoria Administrativa (Tatiana) e Diretor.
- [x] **Reserva de Salas**
  - Suporte a até **4 períodos por turno** (Manhã / Tarde / Noite).
  - Bloqueio automático de conflitos para a mesma sala no mesmo turno e período.
- [x] **Relatórios**
  - Geração de relatórios semestrais consolidados.
  - Filtros e recortes por curso, bloco, sala ou período específico.
- [x] **Visualização**
  - Exibição principal estruturada em **tabela** (focada em densidade de dados, sem uso de cards).
  - Filtros dinâmicos: bloco, sala, curso, turno e período.
  - Painel de detalhes exibido ao clicar em uma sala específica.

---

## 🔒 Requisitos Não Funcionais

- [x] **Plataforma:** 100% web, com layout responsivo e acessível remotamente.
- [x] **Usabilidade:** Interface simples, direta e intuitiva, projetada para exigir o mínimo de digitação manual e mitigar erros de entrada.
- [x] **Banco de Dados:** Facilidade na inclusão/edição e suporte à rotina de atualização de turmas e códigos a cada novo semestre.
- [x] **Segurança:** Controle rigoroso de acesso baseado em perfis (RBAC) e senhas devidamente criptografadas no banco de dados.

---

## ⚙️ Configuração e Execução Local (Ambiente de Homologação)

Para rodar o projeto localmente sem o uso de Docker (utilizando a adaptação para SQLite configurada na branch de homologação), siga os passos abaixo:

### 1. Clonar o Repositório e Preparar a Branch
```bash
git clone [https://github.com/softhub-unieuro/Reserva-de-sala.git](https://github.com/softhub-unieuro/Reserva-de-sala.git)
cd Reserva-de-sala

# Fazer o checkout da branch de Homologação
git checkout "origin/Homologação" -b homologacao

```

### 2. Configurar o Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows utilize: venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Variáveis de Ambiente e Banco de Dados

Crie o arquivo de ambiente local copiando o exemplo:

```bash
cp .env.example .env

```

> **Nota:** O arquivo `project/settings/dev.py` já está configurado para utilizar o banco de dados `sqlite3` localmente quando executado no modo de desenvolvimento.

### 4. Executar as Migrações

Defina as variáveis no terminal e aplique as migrações para estruturar o banco:

```bash
export DJANGO_SETTINGS_MODULE=project.settings.dev
export SECRET_KEY=test-key-for-dev
python manage.py migrate

```

### 5. Criação do Superusuário (Comando Customizado)

O projeto conta com uma rotina automatizada para provisionamento da conta de administrador e dos grupos de permissão padrão. Execute definindo as variáveis no seu terminal:

```bash
export ADMIN_MATRICULA=777777
export ADMIN_NOME="Admin Teste"
export ADMIN_EMAIL="admin@teste.com"
export ADMIN_TELEFONE=61977777777
export ADMIN_DATA_NASCIMENTO=1990-01-01
export ADMIN_SEXO=Masculino
export ADMIN_CARGO=Diretor
export ADMIN_PASSWORD=Teste123!

python manage.py setup_usuarios

```

*Este comando criará automaticamente os grupos de permissão do sistema (Diretor, Assessora Administrativa, NTI, Coordenador, Secretário, Núcleo de Apoio Psicopedagógico, Manutenção) e a conta de administrador.*

### 6. Inicializar o Servidor

```bash
python manage.py runserver 0.0.0.0:8001

```

---

## 🔑 Acesso e Credenciais de Teste

Com o servidor em execução, acesse o sistema através das URLs:

* **Aplicação Principal:** [http://localhost:8001/](https://www.google.com/search?q=http://localhost:8001/)
* **Painel Administrativo (Jazzmin):** [http://localhost:8001/admin/login/](https://www.google.com/search?q=http://localhost:8001/admin/login/)

**Credenciais do Superusuário Gerado:**

* **Matrícula (Usuário):** `777777`
* **Senha:** `Teste123!`

---

## 📊 Critérios de Sucesso

* [x] Distribuição de salas totalmente automatizada.
* [x] Interface ágil e limpa para registro de reservas.
* [x] Geração eficiente de relatórios de apoio institucional.
* [x] Mapa de disponibilidade visualizável com precisão por turno e período.

---

## 👥 Stakeholders

* **Assessoria Administrativa** (Tatiana)
* **Diretor**
* **Coordenadores de Curso**
* **NTI**
* **Professores e Alunos**
* **Equipe de Manutenção**

---

## ⚠️ Riscos Identificados

* Conflitos imprevistos de horários entre reservas simultâneas.
* Alta demanda e sobrecarga na alocação de salas no período matutino.
* Necessidade de realocações emergenciais decorrentes de manutenções ou reformas.
* Ocupação física indevida de salas que já constam como reservadas no sistema.
