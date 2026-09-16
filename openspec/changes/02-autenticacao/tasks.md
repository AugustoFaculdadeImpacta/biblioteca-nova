## 1. Cliente HTTP e sessão

- [x] 1.1 Adicionar funções Xano para `POST /auth/login`, `POST /auth/signup` e `GET /auth/me`, normalizando `authToken`, usuário e erros; verificar payloads e respostas com smoke tests simulados.
- [x] 1.2 Adicionar suporte ao cabeçalho `Authorization: Bearer <token>` nas requisições protegidas do cliente; verificar que categorias não fazem chamadas autenticadas sem token.
- [x] 1.3 Implementar `AuthState` com token, usuário, estado de validação, mensagens e eventos de login, cadastro, restauração e logout; verificar limpeza completa após erro ou logout.
- [x] 1.4 Persistir o token em cookie de sessão sem armazenar senha; verificar restauração via `/auth/me` e invalidação quando a API rejeitar o token.

## 2. Telas de autenticação

- [x] 2.1 Criar a tela de login em português com e-mail, senha, ação de entrar, link para cadastro e feedback de carregamento/erro; verificar validação local e resposta de credenciais inválidas.
- [x] 2.2 Criar a tela de cadastro com nome, e-mail, telefone e senha, ação de cadastrar e link para login; verificar validação local e feedback sem exibir a senha.
- [x] 2.3 Implementar redirecionamento após login/cadastro bem-sucedidos e impedir ações duplicadas durante requisições; verificar que a rota protegida só abre após `/auth/me` confirmar a sessão.

## 3. Proteção da aplicação

- [x] 3.1 Adicionar guarda às páginas privadas de categorias e livros; verificar acesso direto sem sessão, estado de validação e ausência de carregamento de dados antes da autenticação.
- [x] 3.2 Atualizar a página de categorias para consumir o token do `AuthState` e exibir ação de logout; verificar que o usuário autenticado consegue carregar o CRUD e encerrar a sessão.
- [x] 3.3 Preparar a mesma guarda para a futura página de livros sem implementar o CRUD de livros; verificar comportamento de redirecionamento quando a rota for registrada.

## 4. Validação integrada

- [x] 4.1 Executar compilação Reflex e testes do cliente HTTP; verificar ausência de erros de sintaxe, componentes ou handlers.
- [x] 4.2 Validar login, cadastro, restauração, token inválido, proteção de rota e logout contra o Xano; verificar cada cenário de `specs/autenticacao/spec.md` sem registrar tokens nos logs.