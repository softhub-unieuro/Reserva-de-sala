## 📌 Sistema de Reserva de Salas

O sistema tem como objetivo **automatizar a reserva e distribuição de salas de aula** na instituição, substituindo o processo manual feito atualmente em planilhas.  

## 🚀 Visão Geral
- Sistema **web-based** (via navegador).
- Voltado para uso da **Assessoria Administrativa** e setores relacionados.
- Permite reservas **semestrais e avulsas**.
- Elimina conflitos de horário e melhora a **visualização e gestão** das salas.

---

## ✅ Requisitos Funcionais
- [x] **Cadastro e Gerenciamento de Salas**
  - Bloco, número, capacidade, TV, pódio.
  - Apenas o NTI pode cadastrar/editar.
- [x] **Cadastro de Turmas**
  - Nome/código da turma.
  - Suporte a turmas mistas.
- [x] **Cadastro de Usuários**
  - Nome, matrícula, e-mail, telefone, data de nascimento, sexo, cargo.
- [x] **Permissões de Acesso**
  - Visualização → Coordenação, secretarias, manutenção.
  - Moderado → NTI (salas e turmas).
  - Total → Tatiana e Diretor.
- [x] **Reserva de Salas**
  - Até **4 períodos por turno** (manhã/tarde/noite).
  - Impedir conflitos por sala/turno/período.
- [x] **Relatórios**
  - Semestral
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
