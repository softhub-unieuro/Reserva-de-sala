# 👥 App: Usuários

## 🎯 Função
Gerenciar o cadastro, autenticação e controle de acesso dos usuários do sistema de reserva de salas.

---

## ✅ Requisitos Funcionais

- [x] **Cadastro de Usuários**
  - Campos obrigatórios:
    - Nome completo
    - Matrícula institucional
    - E-mail institucional
    - Telefone
    - Data de nascimento
    - Sexo
    - Cargo

- [x] **Sistema de Login e Logout**
  - [x] Autenticação via matrícula + senha.
  - [x] Senhas criptografadas no banco.
  - [x] Função de redefinir senha.

- [x] **Controle de Acesso (Permissões)**
  - Tipos de acesso:
    - **Total**: Assessora Administrativa e Diretor.
    - **Moderado**: NTI.
    - **Visualização**: Coordenações, secretarias, manutenção.
  - Implementar com `User Groups` e `@permission_required`.

- [x] **Gerenciamento de Perfis**
  - [x] Cada usuário deve ter um perfil vinculado a um grupo.
  - [x] Editar informações pessoais e cargo (somente admin).

---

## ⚙️ Tarefas Técnicas

- [x] Criar modelo `Usuario` (extendendo `AbstractUser` ou `BaseUser`).
- [x] Configurar autenticação no `settings.py`.
- [x] Criar formulários de registro e edição (`forms.py`).
- [x] Implementar views para:
  - [x] Login
  - [x] Logout
  - [x] Cadastro
  - [x] Edição de perfil
- [x] Restringir acesso por nível de permissão.
- [x] Criar página de administração para usuários.

---

## 🧱 Banco de Dados
Tabela: `usuarios_usuario`
Campos principais:
- `id`, `nome`, `matricula`, `email`, `telefone`, `cargo`, `data_nascimento`, `sexo`, `password`, `grupo`.

---

## 📊 Critérios de Sucesso
- [x] Apenas usuários autenticados podem acessar o sistema.
- [x] Níveis de permissão respeitados.
- [x] Senhas seguras e criptografadas.
- [x] Cadastro e edição funcionais via formulário e admin.

