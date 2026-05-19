## 📌 Sistema de Reserva de Salas

O sistema tem como objetivo **automatizar a reserva e distribuição de salas de aula** na instituição, substituindo o processo manual feito atualmente em planilhas.

**Status**: ✅ **100% Pronto para Produção**  
**Versão**: 1.0  
**Tecnologia**: Django 6.0 + PostgreSQL + Docker

---

## 🚀 Quick Start

### Iniciar Localmente (Docker)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/reserva-salas.git
cd reserva-salas

# 2. Configure o ambiente
cp .env.example .env

# 3. Inicie os containers
docker-compose up

# 4. Acesse o sistema
# Navegador: http://localhost:8001
# Login: 123456 / Admin@123
```

**Pronto!** Tudo é automatizado. A primeira inicialização pode levar ~30s enquanto o banco sobe.

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [GUIA_PRODUCAO.md](./GUIA_PRODUCAO.md) | Deploy, configuração, troubleshooting e ambiente de produção |
| [TESTES_REALIZADOS.md](./TESTES_REALIZADOS.md) | Detalhes técnicos de todos os testes realizados |
| [Documentation/manual_reserva_salas.md](./Documentation/manual_reserva_salas.md) | Manual do usuário final (funcionalidades) |

---

## ✅ Requisitos Funcionais (Implementados)

- ✅ **Cadastro e Gerenciamento de Salas** - Blocos, números, capacidade, TV, pódio
- ✅ **Cadastro de Turmas** - Código, curso, turno, quantidade de alunos  
- ✅ **Cadastro de Usuários** - Nome, matrícula, e-mail, telefone, data nascimento
- ✅ **Permissões de Acesso** - 7 grupos pré-configurados com roles diferentes
- ✅ **Sistema de Reservas** - Com detecção automática de conflitos
- ✅ **Relatórios** - Exportação em PDF com mapa de salas
- ✅ **Dashboard** - Métricas em tempo real
- ✅ **Autenticação** - Login seguro com matrícula, recuperação de senha
- ✅ **Interface Responsiva** - Funciona em desktop e mobile

---

## 🎯 Principais Endpoints

| Função | URL |
|--------|-----|
| Página Inicial | `/` |
| Login | `/conta/login/` |
| Reservar Salas | `/salas/` |
| Ver Reservas | `/` (dashboard) |
| Relatórios | `/reservas/reservas/fechamento/` |
| Administração | `/admin/` |
| Perfil | `/conta/perfil/` |

---

## 🏗️ Tecnologia

```
Frontend:
  - HTML5 + CSS3 (Tailwind)
  - JavaScript (Vanilla)
  - Bootstrap para componentes

Backend:
  - Django 6.0 (Python 3.12)
  - PostgreSQL 16.13
  - Jazzmin (Admin UI)

DevOps:
  - Docker + Docker Compose
  - Entrypoint automático com setup inicial
```

---

## 🔐 Segurança

- ✅ Senhas com hash (Django ORM)
- ✅ CSRF protection habilitada
- ✅ Session-based authentication
- ✅ SQL injection prevention
- ✅ Usuários com permissões por grupo
- ✅ Admin panel Jazzmin protegido

**Para Produção**: Ver [GUIA_PRODUCAO.md](./GUIA_PRODUCAO.md#segurança)

---

## 📁 Estrutura do Projeto

```
.
├── docker-compose.yml      # Orquestração dos containers
├── Dockerfile              # Configuração da imagem
├── entrypoint.sh          # Script de inicialização automática
├── manage.py              # Gerenciador Django
├── requirements.txt       # Dependências Python
├── .env.example           # Variáveis de ambiente (exemplo)
│
├── project/               # Configurações Django
│   ├── settings/          # Base, Dev, Production
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── usuarios/              # App: Gerenciamento de Usuários
│   ├── models.py         # Modelo customizado de Usuario
│   ├── views.py          # Login, Perfil, Edição
│   ├── forms.py
│   └── templates/
│
├── salas/                 # App: Gerenciamento de Salas
│   ├── models.py         # Bloco, Sala, Curso, Turma
│   ├── views.py
│   ├── forms.py
│   └── templates/
│
├── reservas/             # App: Sistema de Reservas
│   ├── models.py         # Reserva, ReservaSala
│   ├── views.py
│   ├── forms.py
│   ├── services.py       # Lógica de validação
│   └── templates/
│
├── home/                 # App: Dashboard Principal
│   ├── views.py
│   └── templates/
│
├── templates/            # Templates base
├── static/               # CSS, JS, imagens
│
└── Documentation/        # Documentação
    └── manual_reserva_salas.md
```

---

## 🧪 Testes

Todos os testes foram executados e validados:

```bash
# Ver detalhes completos
cat TESTES_REALIZADOS.md
```

**Sumário**: 
- ✅ Docker + containers
- ✅ Banco de dados + migrações  
- ✅ Autenticação
- ✅ CRUD de salas/turmas/usuários
- ✅ Dashboard + métricas
- ✅ Sistema de reservas
- ✅ Validação de conflitos

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é propriedade de [Sua Instituição]. Todos os direitos reservados.

---

## 📧 Suporte

Para dúvidas, problemas ou sugestões:
1. Verifique a [Documentação](./GUIA_PRODUCAO.md)
2. Consulte os [Testes Realizados](./TESTES_REALIZADOS.md)
3. Abra uma issue no GitHub

---

**Desenvolvido com ❤️ - Maio 2026**
  - Por curso, bloco, sala ou período.
- [x] **Visualização**
  - Principal em **tabela** (não cards).
  - Filtros: bloco, sala, curso, turno, período.
  - Detalhes ao clicar em uma sala.

---

## 🔒 Requisitos Não Funcionais
- [x] **Plataforma**
  - 100% web, responsivo, acessível de qualquer lugar.
- [x] **Usabilidade**
  - Interface simples e intuitiva.
  - Pouca digitação para evitar erros.
- [x] **Banco de Dados**
  - Atualização de turmas/códigos a cada semestre.
  - Edição e inclusão simples.
- [x] **Segurança**
  - Controle de acesso baseado em perfis.
  - Senhas criptografadas no banco.

---

## ✨ Novidades da Versão Atual
- [x] **Dashboard Interativo**
  - Cards de métricas em tempo real (Salas ativas, Reservas hoje).
  - Tabela de reservas recentes com status visual.
- [x] **UI/UX Moderno**
  - Sistema de **Toast Notifications** para feedback instantâneo.
  - Alternância de visibilidade de senha (ícone de olho) para facilitar login/cópia.
  - Navegação otimizada e intuitiva no menu lateral.
- [x] **Segurança e Robustez**
  - Proteção de rotas com login obrigatório.
  - Validação de turno entre turmas e reservas.
  - Ambiente isolado via **Docker**.

---

## 📊 Critérios de Sucesso
- [x] Processo de distribuição automatizado.
- [x] Interface intuitiva para reservas com feedback visual.
- [x] Dashboard de gestão para rápida tomada de decisão.
- [x] Relatórios gerados para apoio institucional (PDF).
- [x] Disponibilidade de salas visível por período.

---

## 📅 Próximos Passos
- [x] Analisar planilhas atuais da assessoria.
- [x] Desenvolver cadastro de salas e turmas.
- [x] Criar interface de calendário e reservas.
- [x] Implementar relatórios visuais (PDF/Exportação).

---

## 👥 Stakeholders
- Assessoria administrativa (Tatiana)
- Diretor
- Coordenadores
- NTI
- Professores
- Alunos
- Manutenção

---

## ⚠️ Riscos Identificados
- Conflito de horários entre reservas.
- Sobrecarga de salas no período matutino.
- Realocações por manutenção/reformas.
- Ocupação indevida de salas já reservadas.
**
