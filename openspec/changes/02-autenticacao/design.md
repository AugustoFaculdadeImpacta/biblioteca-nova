## Context

A aplicação Reflex atual concentra a página de categorias em um único módulo e possui um cliente HTTP Xano em `biblioteca_nova/api.py`. O Xano publica `POST /auth/login` e `POST /auth/signup`, ambos retornando `authToken`, além de `GET /auth/me`, que retorna os dados do usuário quando recebe um Bearer JWT válido. A autenticação precisa ser adicionada sem introduzir bibliotecas externas de UI e sem permitir que páginas privadas carreguem dados antes da validação da sessão.

## Goals / Non-Goals

**Goals:**

- Centralizar chamadas de autenticação e montagem do cabeçalho Bearer.
- Persistir o token entre requisições do navegador sem armazenar senha.
- Expor ao Reflex um `AuthState` único para login, cadastro, validação, proteção e logout.
- Separar telas públicas de autenticação das páginas administrativas protegidas.
- Garantir que o cliente de categorias possa receber o token sem duplicar lógica de sessão.

**Non-Goals:**

- Criar autorização por papéis ou permissões além de usuário autenticado.
- Implementar recuperação de senha, confirmação de e-mail ou refresh token.
- Alterar o modelo de usuário ou os endpoints existentes no Xano.
- Implementar o CRUD de livros nesta change.

## Decisions

### Cliente HTTP de autenticação

Adicionar funções dedicadas para `login`, `signup` e `me`, mantendo a URL-base em um único ponto e convertendo respostas de erro em `APIError`. As funções protegidas receberão o token e enviarão `Authorization: Bearer <token>`.

Alternativa considerada: fazer as chamadas diretamente nos componentes Reflex. Foi rejeitada porque espalharia detalhes HTTP pela UI e dificultaria a proteção uniforme de categorias e livros.

### Persistência do JWT

Usar cookie de sessão do Reflex para manter o token entre requisições e disponibilizá-lo ao `AuthState`; a senha nunca será persistida. O estado manterá também uma cópia transitória do usuário e um indicador de sessão validada.

Alternativa considerada: guardar o token somente em memória. Foi rejeitada porque um recarregamento perderia a sessão e obrigaria novo login.

### Proteção de rotas

Cada página privada validará o `AuthState` antes de disparar seu carregamento de dados. Quando a sessão não estiver autenticada, a página emitirá redirecionamento para a rota pública de login; durante a validação, exibirá estado de carregamento e não renderizará conteúdo privado.

Alternativa considerada: proteger apenas botões na interface. Foi rejeitada porque não impede navegação direta para URLs privadas nem chamadas indevidas à API.

### Fluxo após login, cadastro e logout

Login e cadastro salvarão o `authToken`, chamarão `/auth/me` e redirecionarão para a página inicial protegida. Logout limpará cookie e estado e redirecionará para login. Erros de login/cadastro permanecerão na tela pública com os campos não sensíveis preservados.

## Risks / Trade-offs

- [Cookie de sessão ausente ou expirado] -> Tratar como sessão não autenticada e redirecionar para login antes de qualquer carregamento privado.
- [Token inválido retornado pelo Xano] -> Invalidar cookie e usuário local quando `/auth/me` responder erro.
- [API exigir campos adicionais no futuro] -> Encapsular payloads no cliente e exibir a mensagem retornada sem expor dados sensíveis.
- [Página privada carregar antes da validação] -> Usar um estado explícito de inicialização da sessão e bloquear eventos de carga enquanto ele estiver ativo.
- [Configuração de cookie inadequada em produção] -> Usar atributos de sessão apropriados ao ambiente e nunca logar o JWT.

## Migration Plan

1. Adicionar funções e tipos necessários ao cliente Xano.
2. Criar `AuthState`, telas públicas e rotas de login/cadastro.
3. Integrar a proteção à página de categorias e preparar a mesma guarda para livros.
4. Validar login, cadastro, restauração, erro, logout e acesso direto a rota privada.
5. Reverter removendo as rotas e o estado de autenticação; os dados do acervo permanecem inalterados.