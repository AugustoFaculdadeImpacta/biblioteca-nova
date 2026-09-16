## Why

O sistema atualmente permite acessar o gerenciamento de categorias sem identificar o usuário, deixando os dados administrativos expostos a qualquer visitante. Esta change estabelece autenticação baseada em JWT e uma sessão de usuário para que o CRUD existente e os próximos módulos sejam acessíveis somente após login válido.

## What Changes

- Adicionar tela de login com e-mail, senha, ação de entrar e feedback visual para carregamento, sucesso e erro.
- Adicionar tela de cadastro com e-mail, senha e feedback visual para validação e resultado da operação.
- Integrar o Reflex aos endpoints Xano `/auth/login`, `/auth/signup` e `/auth/me`.
- Criar um `AuthState` para armazenar o token JWT, os dados do usuário conectado e o estado da sessão.
- Validar a sessão existente ao carregar a aplicação e enviar o token Bearer nas requisições protegidas.
- Proteger as páginas de categorias e livros, redirecionando visitantes não autenticados para login.
- Adicionar logout, removendo a sessão local e redirecionando o usuário para a tela de login.

## Capabilities

### New Capabilities

- `autenticacao`: Login, cadastro, sessão JWT, proteção de páginas e logout de usuários do sistema.

### Modified Capabilities

Nenhuma. A capability de autenticação é nova; a proteção das páginas existentes é especificada como parte dela.

## Impact

- Aplicação Reflex, com novas telas de autenticação, estado global de sessão e redirecionamento de rotas.
- Cliente HTTP Xano, que deverá consumir `/auth/login`, `/auth/signup` e `/auth/me` e enviar `Authorization: Bearer <token>` aos recursos protegidos.
- Página atual de categorias e futura página de livros, que deixarão de ser públicas.
- API Xano e seus contratos de autenticação JWT.
- Dados de sessão no navegador, sem alterar o modelo das entidades de biblioteca.