## Why

O sistema ainda possui apenas a página inicial padrão do Reflex e não oferece uma forma de manter as categorias que serão referenciadas pelos livros do acervo. Esta change estabelece o primeiro fluxo funcional do sistema, conectando a interface Reflex à API Xano e criando um CRUD reutilizável como base para os próximos módulos.

## What Changes

- Adicionar consumo HTTP da Base URL do Xano para o recurso `/categorias`, cobrindo listagem, criação, atualização via `PATCH` e exclusão.
- Adicionar estado Reflex para manter a lista de categorias, os dados do formulário, a categoria em edição e mensagens de carregamento, erro e sucesso.
- Substituir a página inicial padrão por uma interface em português para listar categorias e executar cadastro, edição e exclusão.
- Validar os campos da entidade Categoria antes do envio e refletir falhas ou sucessos da API na interface.
- Definir o contrato funcional de respostas vazias, erros de API e confirmação antes da exclusão.

## Capabilities

### New Capabilities

- `categorias`: Gerenciamento de categorias por meio de integração com a API Xano e interface CRUD no Reflex.

### Modified Capabilities

Nenhuma. Não existem capabilities formalizadas no projeto que precisem ter seus requisitos alterados.

## Impact

- Aplicação Reflex em `biblioteca_nova/biblioteca_nova.py`, que deixará de exibir a página de boas-vindas padrão.
- Nova camada de cliente HTTP para a Base URL Xano configurada em `openspec/config.yaml`, usando os endpoints `/categorias`.
- Estado e componentes de interface da aplicação, sem adoção de bibliotecas externas de UI.
- API Xano e seus contratos de dados para a entidade `categoria` (`id`, `nome` e `descricao`).
- Nenhuma alteração de banco de dados, autenticação ou outras entidades do domínio está incluída nesta change.