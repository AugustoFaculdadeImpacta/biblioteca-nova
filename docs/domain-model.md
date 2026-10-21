# Modelo de Domínio - Sistema de Biblioteca

## Entidades e Atributos

### 1. Categoria (`categoria`)
- `id` (int): Identificador único.
- `nome` (string): Nome da categoria (ex: Ficção, Tecnologia).
- `descricao` (string): Descrição detalhada da categoria.

> O schema Xano atual de categorias contém `id` e `nome`; `descricao` permanece
> apenas no modelo conceitual e não é retornada pelo endpoint.

### 2. Livro (`livro`)
- `id` (int): Identificador único.
- `titulo` (string): Título do livro.
- `autor` (string): Autor do livro.
- `ano_publicacao` (int, opcional): Ano de publicação.
- `quantidade_disponivel` (int, opcional): Quantidade disponível no acervo.
- `categoria_id` (int, anulável no Xano): Identificador da categoria escolhida.

### 3. Usuário (`usuario`)
- `id` (int): Identificador único.
- `nome` (string): Nome completo do usuário.
- `email` (string): E-mail do usuário.
- `telefone` (string): Telefone de contato.

### 4. Empréstimo (`emprestimo`)
- `id` (int): Identificador único.
- `usuario_id` (int): Chave estrangeira referenciando `usuario`.
- `livro_id` (int): Chave estrangeira referenciando `livro`.
- `data_emprestimo` (date): Data de retirada do livro.
- `data_devolucao` (date): Data prevista ou realizada de devolução.
- `status` (string): Estado atual (`Ativo`, `Devolvido`, `Atrasado`).

## Relacionamentos
- Uma **Categoria** possui N **Livros** (1:N).
- Um **Usuário** pode realizar N **Empréstimos** (1:N).
- Um **Livro** pode estar presente em N **Empréstimos** ao longo do tempo (1:N).

No contrato Xano atual, `categoria_id` não tem relacionamento declarado com a
tabela de categorias. O fluxo de livros exige a seleção de categoria na
interface, mas essa regra não é imposta pelo backend.