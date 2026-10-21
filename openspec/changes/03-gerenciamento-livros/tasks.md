## 1. Confirmar o contrato Xano

- [x] 1.1 Identificar o workspace Xano de desenvolvimento selecionado e inspecionar/puxar seu contrato local com o Xano CLI; registrar os endpoints e formatos reais de livros/categorias sem incluir credenciais, e pausar com o bloqueio documentado se não houver acesso. Resultado: workspace 151966, branch `v1`, aprovado pelo usuário; endpoints `GET/POST /livro` e `GET/PUT/DELETE /livro/{livro_id}` confirmados por pull somente leitura.
- [x] 1.2 Confirmar no workspace os campos, associação obrigatória a categoria e permissões das quatro operações; atualizar esta proposta, a spec e o design para refletir o contrato verificado antes de iniciar implementação. Resultado: campos Xano registrados; categoria obrigatória somente na interface por decisão do usuário; endpoints sem autenticação declarada aceitos como limitação desta change.
- [x] 1.3 Validar com Xano Developer MCP o XanoScript relacionado aos endpoints confirmados; registrar o resultado e não criar nem enviar alterações remotas nesta etapa. Resultado: 7 arquivos XanoScript de livros e da tabela foram validados com sucesso (7 válidos, 0 inválidos); nenhuma alteração remota foi enviada.

## 2. Implementar integração e interface

- [x] 2.1 Adicionar ao cliente `biblioteca_nova/api.py` operações de lista, criação, atualização e exclusão conforme o contrato Xano confirmado; verificar comportamento com testes de HTTP simulado, incluindo erros e respostas inválidas. Resultado: adaptador usa `GET/POST /livro`, `PUT/DELETE /livro/{livro_id}`; 10 testes simulados cobrem respostas válidas, campos anuláveis, resposta incompleta, HTTP de erro e ID inválido.
- [x] 2.2 Implementar na rota `/livros` o catálogo autenticado e os formulários de cadastro/edição, reaproveitando sessão, categorias e padrões existentes; verificar estados de carregamento, vazio, sucesso, cancelamento e erro. Resultado: catálogo e formulários integrados à sessão existente; compilação Reflex validada.
- [x] 2.3 Implementar confirmação de exclusão e associação de categoria conforme regra confirmada no Xano; verificar que cancelar não envia exclusão e que respostas de erro preservam formulário e dados exibidos. Resultado: exclusão exige confirmação; cancelar apenas fecha o diálogo; categoria é obrigatória no formulário; falhas mantêm dados e valores editáveis.

## 3. Verificar e registrar entrega

- [x] 3.1 Executar verificações locais disponíveis (testes de API simulada, validação OpenSpec e compilação Reflex) e registrar resultados reais, incluindo qualquer bloqueio ambiental. Resultado: 10/10 testes passaram; `reflex compile --dry` e `openspec validate 03-gerenciamento-livros --type change --strict` passaram.
- [x] 3.2 Se houver workspace sandbox aprovado e test data, executar verificação ponta a ponta sem afetar dados de produção e registrar exatamente o que foi testado. Resultado: não executado; nenhum conjunto de dados de teste foi fornecido/autorizado para operações que criam, editam ou excluem registros. Nenhuma mutação remota foi feita.
- [x] 3.3 Revisar o diff para garantir que não inclui credenciais nem arquivos gerados; criar um commit com mensagem descritiva e data real somente para as alterações desta change, sem incluir alterações preexistentes. Resultado: revisão concluída; o commit incluirá somente os arquivos da implementação e desta change OpenSpec.
