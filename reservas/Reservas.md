# 📅 App: Reservas

## 🎯 Função
Gerenciar o agendamento de salas por turno, período e turma, evitando conflitos de horários.

---

## ✅ Requisitos Funcionais

- [x] **Cadastro de Reservas**
  - Cada sala pode ter até **4 períodos por turno**.
  - Períodos:
    - 1º: 08h00 - 08h50  
    - 2º: 08h50 - 09h40  
    - 3º: 10h00 - 10h50  
    - 4º: 10h50 - 11h40
  - Campos:
    - Sala (FK)
    - Turma (FK)
    - Turno
    - Período
    - Data
    - Usuário responsável

- [x] **Prevenção de Conflitos**
  - Impedir duas reservas para a mesma sala/turno/período.

- [ ] **Relatórios**
  - Gerar relatórios:
    - Semestral
  - Exportar em PDF.

- [ ] **Histórico de Reservas**
  - Armazenar registros por até 1 ano.
  - Permitir reset mediante a retirada do relatório a cada semestre.

---

## ⚙️ Tarefas Técnicas

- [x] Criar modelos `Reserva` e `Turma`.
- [x] Implementar `UniqueConstraint` para evitar conflitos.
- [x] Criar lógica de validação de horários.
- [x] Views para:
  - Criar reserva
  - Listar reservas (tabela com filtros)
  - Detalhes da reserva
- [ ] Filtros por bloco, andar, curso, data inicial, capacidade.
- [ ] Relatórios com `weasyprint` (PDF).
- [ ] Automatizar limpeza anual de dados antigos.

---

## 🧱 Banco de Dados
Tabelas:
- `reservas_reserva`
  - `id`, `sala_id`, `turma_id`, `data`, `turno`, `periodo`, `usuario_id`.
- `reservas_turma`
  - `id`, `codigo`, `curso`, `tipo`, `semestre`.

---

## 📊 Critérios de Sucesso
- [x] Sistema impede conflitos de agendamento.
- [ ] Reservas podem ser filtradas por data, sala, curso.
- [ ] Geração de relatórios funcional.
- [ ] Reset de semestre automatizado.
- [x] Interface clara e rápida para Tatiana.

