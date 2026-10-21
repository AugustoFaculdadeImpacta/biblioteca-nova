## Purpose

Permitir que usuários autenticados mantenham o catálogo de livros da biblioteca, associando cada registro a uma categoria existente e preservando o Xano como fonte dos dados.

## ADDED Requirements

### Requirement: Proteger o catálogo de livros
O sistema SHALL validar a sessão da aplicação antes de exibir ou carregar o catálogo de livros. Visitantes sem sessão válida SHALL ser redirecionados para a tela de login sem iniciar chamadas de dados do catálogo. Esta proteção é da interface: os endpoints e tabelas Xano inspecionados não declaram autenticação no backend.

#### Scenario: Visitante tenta abrir o catálogo
- **WHEN** uma pessoa sem sessão válida abre `/livros`
- **THEN** o sistema redireciona para `/login` e não solicita livros nem categorias para a tela privada

#### Scenario: Usuário autenticado abre o catálogo
- **WHEN** a sessão é válida e o usuário abre `/livros`
- **THEN** o sistema permite o acesso e carrega livros e categorias após validar a sessão da aplicação.

### Requirement: Consultar e manter livros
O sistema SHALL permitir listar, cadastrar, editar e excluir livros no catálogo usando os endpoints existentes do workspace Xano, sem substituir a fonte remota por armazenamento local. Cada livro SHALL apresentar identificador, título (`titulo`), autor (`autor`), ano de publicação (`ano_publicacao`), quantidade disponível (`quantidade_disponivel`) e categoria (`categoria_id`). ISBN não existe no schema Xano confirmado e não faz parte desta change. O formulário SHALL exigir título, autor e categoria; ano e quantidade podem ficar vazios, e quantidade informada SHALL ser um inteiro não negativo.

#### Scenario: Listar livros
- **WHEN** o catálogo é carregado com sucesso
- **THEN** a interface exibe os livros retornados, incluindo título, autor, ano, quantidade e o nome da categoria associada

#### Scenario: Cadastrar livro
- **WHEN** o usuário autenticado envia os dados válidos de um livro e uma categoria existente
- **THEN** o sistema persiste o livro no Xano, informa sucesso e atualiza a listagem

#### Scenario: Editar livro
- **WHEN** o usuário seleciona um livro, altera seus dados e salva
- **THEN** o sistema atualiza o registro correspondente no Xano e exibe os dados atualizados

#### Scenario: Cancelar edição
- **WHEN** o usuário cancela a edição de um livro
- **THEN** o sistema descarta os valores não salvos e mantém o registro persistido inalterado

#### Scenario: Confirmar exclusão
- **WHEN** o usuário confirma a exclusão de um livro e o Xano aceita a operação
- **THEN** o sistema informa sucesso e remove ou recarrega o livro na listagem

#### Scenario: Cancelar exclusão
- **WHEN** o usuário cancela a confirmação de exclusão
- **THEN** o sistema não chama a operação de exclusão e mantém o livro na listagem

#### Scenario: API retorna erro
- **WHEN** uma operação de leitura ou gravação falha, retorna erro HTTP ou resposta inválida
- **THEN** o sistema preserva os dados exibidos e os valores editáveis, apresenta uma mensagem compreensível e encerra o estado de carregamento

### Requirement: Associar livro a categoria existente
O sistema SHALL exigir a seleção de uma categoria existente ao cadastrar ou editar um livro e SHALL persistir seu identificador inteiro em `categoria_id`. O campo é anulável no Xano; a exigência desta change é somente da interface e não é imposta pelo backend. Se não houver categoria disponível, a interface SHALL orientar o usuário a cadastrar uma categoria antes de salvar o livro.

#### Scenario: Selecionar categoria
- **WHEN** o formulário de livro é exibido e há categorias disponíveis
- **THEN** o usuário pode selecionar uma categoria existente e a operação persiste sua referência

#### Scenario: Não há categorias disponíveis
- **WHEN** o usuário abre o formulário sem que existam categorias
- **THEN** a interface informa que uma categoria deve ser cadastrada primeiro e não envia um livro sem referência de categoria
