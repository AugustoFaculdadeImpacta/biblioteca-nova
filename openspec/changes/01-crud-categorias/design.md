## Context

O projeto contém apenas a página inicial padrão do Reflex e não possui cliente de API, estado de domínio ou specs existentes. A entidade Categoria tem `id`, `nome` e `descricao`; livros dependerão de sua existência por meio de `categoria_id`. A Base URL e o idioma do produto vêm de `openspec/config.yaml`, enquanto a restrição do projeto impede bibliotecas externas de UI.

## Goals / Non-Goals

**Goals:**

- Separar a comunicação HTTP do estado e da apresentação para que o padrão possa ser reutilizado pelos próximos CRUDs.
- Centralizar a transformação de respostas, erros HTTP e mensagens exibidas ao usuário.
- Fazer a tela funcionar com carregamento, sucesso, falha, edição, cancelamento e lista vazia.
- Manter o contrato da API restrito ao recurso `/categorias` e aos campos da entidade documentada.

**Non-Goals:**

- Implementar livros, usuários ou empréstimos.
- Criar autenticação, autorização ou persistência local.
- Alterar o modelo de dados do Xano ou adicionar endpoints alternativos.
- Introduzir uma biblioteca externa de componentes visuais.

## Decisions

### Cliente HTTP dedicado

Usar uma camada pequena e dedicada para construir as quatro operações do recurso e normalizar erros. A Base URL deve ser definida em um único ponto de configuração, evitando URLs espalhadas pela UI e facilitando a troca de ambiente.

Alternativa considerada: chamar HTTP diretamente nos handlers do estado. Foi rejeitada porque mistura transporte com regras de tela e dificulta a reutilização nos próximos módulos.

### Estado Reflex como orquestrador

Manter no `State` a coleção, os campos do formulário, o identificador em edição, o indicador de carregamento e as mensagens transitórias. Cada operação deve atualizar a lista somente após uma resposta válida; em caso de falha, os valores do formulário permanecem disponíveis para correção.

Alternativa considerada: recarregar a página após cada mutação. Foi rejeitada porque perde o contexto de edição, produz uma experiência mais lenta e não trata adequadamente erros parciais.

### Formulário único para cadastro e edição

Usar a mesma área de formulário nos dois modos, diferenciados pela presença de um identificador em edição. Isso reduz duplicação visual e garante que validação e mensagens sejam consistentes.

Alternativa considerada: modal separado para edição. Foi rejeitada nesta primeira change por acrescentar complexidade de foco e estado sem necessidade funcional.

### Atualização da lista após mutações

Após criar, atualizar ou excluir, o estado deve refletir a resposta confirmada. Quando o formato retornado não permitir atualizar localmente com segurança, o estado deve fazer novo `GET /categorias`, mantendo uma única fonte de verdade no Xano.

### Exclusão com confirmação

A ação de exclusão deve exigir confirmação explícita antes do `DELETE`. O cancelamento não deve alterar estado persistido nem remover o item da lista.

## Risks / Trade-offs

- [Contrato Xano diferente do modelo documentado] -> Validar durante a implementação os nomes dos campos, formato de coleção e convenção do identificador; encapsular ajustes no cliente HTTP.
- [Categoria vinculada a livros não pode ser excluída] -> Exibir o erro retornado pela API e manter o item na lista; a regra de dependência será definida pelo backend quando o CRUD de livros existir.
- [Falhas de rede durante uma mutação] -> Encerrar o carregamento em qualquer caminho, preservar o formulário e mostrar uma mensagem acionável.
- [Resposta de lista em formato inesperado] -> Tratar a resposta como erro de integração, sem substituir a lista válida já carregada por dados parciais.
- [Estado de carregamento não refletido na UI] -> Desabilitar ações concorrentes e validar manualmente os estados de carregamento e erro durante a implementação.

## Migration Plan

1. Implementar o cliente HTTP, o estado e a interface sob a change `01-crud-categorias`.
2. Confirmar os endpoints diretamente contra a API Xano e executar os cenários da especificação.
3. Substituir a página padrão pela tela de categorias e validar o fluxo completo em ambiente local.
4. Reverter removendo a tela e o cliente de categorias caso a integração não possa ser publicada; não há migração de banco prevista.