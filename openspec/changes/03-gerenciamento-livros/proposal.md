## Why

A rota `/livros` existe, mas ainda exibe somente uma mensagem de funcionalidade futura. O catálogo de livros é necessário para que a biblioteca relacione obras às categorias já gerenciadas e forme a base do futuro fluxo de empréstimos.

## What Changes

- Implementar um fluxo autenticado de consulta, cadastro, edição e exclusão de livros no Reflex.
- Usar o contrato do workspace aprovado: `titulo`, `autor`, `ano_publicacao`, `quantidade_disponivel` e `categoria_id`. ISBN não faz parte do schema Xano atual e fica fora desta change.
- Integrar os endpoints Xano existentes; não criar nem enviar XanoScript ou alterações remotas nesta change.
- Manter a sessão da aplicação como proteção da interface. Os endpoints/tabelas Xano inspecionados não declaram autenticação; isso não equivale a autorização no backend.
- Manter estados de carregamento, lista vazia, validação e mensagens de erro/sucesso consistentes com o CRUD de categorias.
- Exigir categoria no formulário, conforme decisão do usuário, embora `categoria_id` seja anulável no Xano e essa exigência não seja imposta pelo backend.
- Exigir título e autor na interface por decisão do usuário, mesmo que esses campos sejam anuláveis no schema Xano.
- Não implementar cópias físicas, empréstimos, devoluções, reservas ou papéis de usuário nesta change. A distinção entre título e exemplar deverá ser decidida antes de projetar empréstimos.
- Não enviar alterações ao Xano. Qualquer sincronização remota exigirá revisão explícita do usuário e uso de sandbox quando disponível.

## Capabilities

### New Capabilities

- `livros`: catálogo autenticado para consultar e manter os livros relacionados às categorias existentes.

### Modified Capabilities

Nenhuma. Ainda não há capabilities consolidadas em `openspec/specs/`.

## Impact

- `biblioteca_nova/biblioteca_nova.py`: substituir a página de livros atualmente informativa por fluxo de catálogo protegido.
- `biblioteca_nova/api.py`: acrescentar operações para livros conforme o contrato confirmado do workspace Xano.
- `xano/`: nenhuma alteração prevista; os endpoints necessários já existem no workspace.
- Workspace Xano e API REST: usar o contrato de livros/categorias existente; nenhuma alteração remota será feita nesta change.
- OpenSpec: introduzir a capability `livros` e validar o comportamento antes da implementação.
