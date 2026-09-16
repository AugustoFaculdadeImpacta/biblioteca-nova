## Purpose

Permitir que usuários se cadastrem, entrem e mantenham uma sessão autenticada no sistema, protegendo o gerenciamento do acervo contra acesso não autorizado.

## ADDED Requirements

### Requirement: Permitir login e cadastro de usuário
O sistema SHALL disponibilizar telas em português para login e cadastro. O login SHALL coletar `email` e `senha` e enviar `POST /auth/login`; o cadastro SHALL coletar `nome`, `email`, `telefone` e `senha` e enviar `POST /auth/signup`. As telas SHALL exibir estados de carregamento, sucesso e erro sem expor a senha informada.

#### Scenario: Login realizado com sucesso
- **WHEN** o usuário informa e-mail e senha válidos e a API responde com `authToken`
- **THEN** o sistema armazena a sessão, busca os dados do usuário autenticado e redireciona para uma página protegida

#### Scenario: Cadastro realizado com sucesso
- **WHEN** o usuário informa nome, e-mail, telefone e senha válidos e a API responde com `authToken`
- **THEN** o sistema cria a sessão, busca os dados do usuário autenticado e redireciona para uma página protegida

#### Scenario: Credenciais rejeitadas
- **WHEN** o login ou cadastro retorna erro da API
- **THEN** o sistema permanece na tela de autenticação, exibe uma mensagem compreensível e não cria uma sessão autenticada

#### Scenario: Campos obrigatórios inválidos
- **WHEN** o usuário tenta enviar um formulário sem e-mail, senha ou outro campo obrigatório do cadastro
- **THEN** o sistema exibe validação local e não chama a API

### Requirement: Gerenciar a sessão autenticada
O sistema SHALL manter o token JWT e os dados do usuário conectado no `AuthState`. Após obter um token, o sistema SHALL validar a sessão por meio de `GET /auth/me` com o cabeçalho `Authorization: Bearer <token>`. O sistema SHALL tratar token ausente, expirado, inválido ou rejeitado como sessão não autenticada.

#### Scenario: Restaurar sessão válida
- **WHEN** a aplicação é carregada com um token armazenado e `/auth/me` responde com os dados do usuário
- **THEN** o sistema popula o usuário conectado e mantém o acesso às páginas protegidas

#### Scenario: Rejeitar sessão inválida
- **WHEN** `/auth/me` retorna erro para o token armazenado
- **THEN** o sistema remove o token e os dados do usuário e redireciona para login

#### Scenario: Requisição protegida
- **WHEN** o usuário autenticado acessa categorias, livros ou outro recurso protegido
- **THEN** as requisições HTTP incluem o token no cabeçalho Bearer

### Requirement: Proteger páginas administrativas
O sistema SHALL bloquear o acesso às páginas de gerenciamento de categorias e livros quando não houver usuário autenticado. Visitantes não autenticados SHALL ser redirecionados para a tela de login, e a página protegida não SHALL executar carregamentos de dados antes da sessão ser validada.

#### Scenario: Visitante acessa categorias
- **WHEN** um visitante sem sessão tenta abrir o CRUD de categorias
- **THEN** o sistema redireciona para login e não carrega a lista de categorias

#### Scenario: Usuário autenticado acessa categorias
- **WHEN** a sessão do usuário é válida e ele abre o CRUD de categorias
- **THEN** o sistema permite o acesso e carrega os dados usando o token JWT

#### Scenario: Visitante acessa livros
- **WHEN** um visitante sem sessão tenta abrir o CRUD de livros
- **THEN** o sistema redireciona para login e não carrega dados de livros

### Requirement: Permitir logout
O sistema SHALL oferecer uma ação de logout visível ao usuário autenticado. Ao executar logout, o sistema SHALL remover o token JWT e os dados do usuário, invalidar a sessão local e redirecionar para a tela de login.

#### Scenario: Logout concluído
- **WHEN** o usuário autenticado aciona logout
- **THEN** o sistema limpa a sessão local e apresenta a tela de login

#### Scenario: Acesso após logout
- **WHEN** o usuário tenta voltar para uma página protegida após o logout
- **THEN** o sistema bloqueia o acesso e redireciona novamente para login