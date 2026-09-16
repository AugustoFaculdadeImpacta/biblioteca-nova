## Purpose

Oferecer o gerenciamento completo das categorias do acervo, mantendo os dados no Xano e disponibilizando uma interface Reflex em português para as operações administrativas.

## ADDED Requirements

### Requirement: Integrar o recurso de categorias com a API
O sistema SHALL consumir a Base URL Xano configurada no projeto e SHALL disponibilizar as operações HTTP do recurso `/categorias`: `GET /categorias`, `POST /categorias`, `PATCH /categorias/{id}` e `DELETE /categorias/{id}`. As requisições de criação e atualização SHALL enviar `nome` e `descricao`, e as respostas bem-sucedidas SHALL ser interpretadas como registros contendo `id`, `nome` e `descricao`.

#### Scenario: Listar categorias com sucesso
- **WHEN** a tela de categorias é carregada e a API responde com sucesso ao `GET /categorias`
- **THEN** o sistema exibe todos os registros retornados, mostrando nome e descrição de cada categoria

#### Scenario: Criar categoria com sucesso
- **WHEN** um usuário envia dados válidos e a API responde com sucesso ao `POST /categorias`
- **THEN** o sistema informa que a categoria foi cadastrada, limpa o formulário e atualiza a lista com o registro criado

#### Scenario: Atualizar categoria com sucesso
- **WHEN** um usuário confirma a edição de uma categoria válida e a API responde com sucesso ao `PATCH /categorias/{id}`
- **THEN** o sistema informa que a categoria foi atualizada, encerra o modo de edição e exibe os novos dados na lista

#### Scenario: Excluir categoria com sucesso
- **WHEN** um usuário confirma a exclusão e a API responde com sucesso ao `DELETE /categorias/{id}`
- **THEN** o sistema informa que a categoria foi excluída e remove o registro da lista exibida

#### Scenario: API retorna erro
- **WHEN** qualquer operação contra `/categorias` falha, retorna status HTTP de erro ou devolve uma resposta inválida
- **THEN** o sistema preserva os dados já exibidos, informa uma mensagem compreensível e encerra o estado de carregamento

### Requirement: Gerenciar o estado do fluxo de categorias
O sistema SHALL manter a lista de categorias, os valores atuais do formulário, o identificador da categoria em edição, o estado de carregamento e mensagens de erro ou sucesso. O estado SHALL impedir o envio de operações concorrentes enquanto uma requisição estiver em andamento e SHALL manter os valores digitados quando uma operação falhar.

#### Scenario: Carregar lista
- **WHEN** a busca inicial ou uma atualização da lista é iniciada
- **THEN** o sistema indica carregamento, evita ações duplicadas durante a requisição e ao final apresenta os dados, uma mensagem de erro ou o estado vazio correspondente

#### Scenario: Iniciar edição
- **WHEN** o usuário seleciona uma categoria para editar
- **THEN** o formulário é preenchido com `nome` e `descricao`, o identificador do registro é preservado e a ação principal passa a representar atualização

#### Scenario: Cancelar edição
- **WHEN** o usuário cancela a edição
- **THEN** o identificador em edição é removido e o formulário retorna ao modo de cadastro sem alterar a categoria persistida

#### Scenario: Validar formulário localmente
- **WHEN** o usuário tenta cadastrar ou atualizar uma categoria sem nome
- **THEN** o sistema não chama a API e exibe uma mensagem de validação junto ao formulário

### Requirement: Disponibilizar interface CRUD de categorias
O sistema SHALL apresentar uma interface em português com formulário para nome e descrição, listagem das categorias e ações explícitas para editar e excluir cada registro. A interface SHALL apresentar um estado vazio quando não houver categorias e SHALL solicitar confirmação antes da exclusão.

#### Scenario: Cadastrar categoria pela interface
- **WHEN** o usuário preenche nome e, opcionalmente, descrição e aciona o cadastro
- **THEN** a interface envia os dados, informa o resultado e atualiza a listagem sem exigir recarregamento manual da página

#### Scenario: Editar categoria pela interface
- **WHEN** o usuário aciona a ação de edição de um item
- **THEN** a interface torna os dados editáveis no formulário e oferece uma ação para salvar e outra para cancelar

#### Scenario: Confirmar exclusão
- **WHEN** o usuário aciona a exclusão de uma categoria
- **THEN** a interface pede confirmação antes de chamar a API e não exclui o registro se a confirmação for cancelada

#### Scenario: Lista vazia
- **WHEN** a API retorna uma coleção vazia
- **THEN** a interface mostra uma mensagem orientando o cadastro da primeira categoria, sem apresentar uma tabela vazia sem contexto