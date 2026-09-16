# Diretrizes Gerais para Agentes de IA

Você é um assistente de desenvolvimento integrado ao VS Code. Siga estas diretrizes ao trabalhar neste repositório:

1. **Metodologia OpenSpec**:
   - Respeite o fluxo obrigatório: `Explore` -> `Propose` -> `Review` -> `Apply` -> `Archive`.
   - NUNCA escreva código ou crie arquivos durante as etapas de `Explore` ou `Propose`.
   - Aguarde a aprovação do usuário (`Review`) antes de executar o `Apply`.

2. **Stack Tecnológica**:
   - Frontend: **Reflex** (Python).
   - Backend: **Xano** (BaaS / API REST).
   - Idioma: Todo o código, comentários, commits e documentações devem ser em **Português (Brasil)**.

3. **Boas Práticas de Código e Versionamento**:
   - Verifique o estado do repositório com `git status` antes e depois das operações.
   - Preserve arquivos existentes e evite alterações não solicitadas.
   - Crie componentes limpos, modulares e focados no Reflex.