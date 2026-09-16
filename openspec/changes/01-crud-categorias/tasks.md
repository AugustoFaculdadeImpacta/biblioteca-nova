## 1. Cliente HTTP e contrato da API

- [x] 1.1 Criar a camada de cliente para centralizar a Base URL e os endpoints `GET /categorias`, `POST /categorias`, `PATCH /categorias/{id}` e `DELETE /categorias/{id}`; verificar que cada método monta a URL e o payload com `id`, `nome` e `descricao` corretamente.
- [x] 1.2 Implementar tratamento de status HTTP, falhas de rede e respostas inválidas; verificar que erros não são convertidos em categorias parciais e retornam mensagens utilizáveis pelo estado.
- [ ] 1.3 Confirmar o contrato real da API Xano em ambiente de desenvolvimento; verificar manualmente listagem, criação, atualização e exclusão com registros de teste e documentar qualquer ajuste no cliente.

## 2. Estado Reflex

- [x] 2.1 Substituir o estado vazio da aplicação por estado para coleção de categorias, campos do formulário, identificador em edição, carregamento e mensagens; verificar que os valores iniciais representam cadastro sem seleção.
- [x] 2.2 Implementar carregamento inicial e atualização da lista usando o cliente HTTP; verificar estados de sucesso, lista vazia, erro e encerramento do carregamento.
- [x] 2.3 Implementar validação local, cadastro e edição; verificar que nome vazio não chama a API, que dados válidos usam o método correto e que falhas preservam os valores digitados.
- [x] 2.4 Implementar cancelamento da edição, limpeza após sucesso e exclusão com confirmação; verificar que o cancelamento não chama `DELETE` e que uma exclusão confirmada remove ou recarrega o item corretamente.

## 3. Interface Reflex

- [x] 3.1 Substituir a página padrão por uma tela em português com formulário de nome e descrição; verificar que o formulário alterna claramente entre cadastro e edição e oferece cancelamento durante edição.
- [x] 3.2 Renderizar a lista de categorias com nome, descrição e ações de editar/excluir; verificar que cada ação atua no registro correspondente e que a lista vazia apresenta orientação para o primeiro cadastro.
- [x] 3.3 Exibir indicadores de carregamento, mensagens de sucesso/erro e confirmação de exclusão sem introduzir bibliotecas externas de UI; verificar visualmente os estados principais em ambiente local.

## 4. Validação integrada

- [ ] 4.1 Executar os fluxos de cadastro, edição, cancelamento, exclusão confirmada e exclusão cancelada contra a API Xano; verificar cada cenário correspondente em `specs/categorias/spec.md`.
- [x] 4.2 Executar a validação OpenSpec e a aplicação Reflex em ambiente local; verificar que a change fica válida e que a tela carrega sem erros de compilação ou runtime.