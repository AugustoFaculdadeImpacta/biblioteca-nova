# Xano no VS Code

## Requisitos do projeto

Este projeto usa Reflex/Python e chama a API REST do Xano pelo cliente HTTP em `biblioteca_nova/api.py`. O fluxo acadêmico também exige a linguagem XanoScript e o Xano Developer MCP; por isso o workspace recomenda a extensão oficial atual e declara o MCP em `.vscode/mcp.json`.

## XanoScript

A extensão recomendada é [XanoScript Language Support](https://marketplace.visualstudio.com/items?itemName=xano.xanoscript-language-server), identificador `xano.xanoscript-language-server`. Ela fornece suporte de linguagem para arquivos `.xs`. A antiga extensão `xano.xanoscript` foi descontinuada em favor desta extensão mais recente, combinada com Xano CLI e Developer MCP.

No momento da revisão, o projeto não continha arquivos `.xs`; a configuração da extensão prepara o editor, mas não converte por si só as chamadas REST existentes em código XanoScript.

## Xano Developer MCP

O arquivo `.vscode/mcp.json` configura o servidor oficial publicado como `@xano/developer-mcp`, iniciado localmente por `npx`. Ao iniciar o servidor pela primeira vez, `npx` pode baixar o pacote. VS Code precisa estar em modo confiável para iniciar servidores MCP do workspace. O servidor oferece documentação e validação de XanoScript; para consultar ou modificar um workspace real, o fluxo também requer Xano CLI instalado e autenticado.

Configurar o servidor não conecta uma conta Xano. Faça a autenticação e escolha o workspace com o Xano CLI no computador de cada desenvolvedor. As credenciais ficam fora do repositório; não adicione tokens a arquivos de configuração versionados. Para autenticar e consultar os workspaces disponíveis no PowerShell:

```powershell
xano auth
xano workspace list
```

Para baixar apenas os documentos do workspace selecionado, sem variáveis de ambiente ou registros, informe o ID e a branch e use uma pasta local dedicada:

```powershell
xano workspace pull --workspace <id> --branch <branch> --directory .\xano-workspace
```

O pull é somente leitura na conta Xano. Não execute `xano workspace push` sem revisar e aprovar explicitamente as alterações locais e o destino.

## Extensões Python

O workspace também recomenda Python, Pylance, Python Environments e Python Debugger, e configura `.venv` como interpretador padrão. Essas extensões Python já estavam instaladas nesta máquina quando o projeto foi inspecionado.

## Validação que depende da conta Xano

As tarefas OpenSpec de confirmação manual do CRUD de categorias continuam pendentes. É preciso validar listagem, cadastro, edição e exclusão com registros de teste no workspace Xano correto antes de marcá-las como concluídas.

## Referências oficiais

- [Xano: configurar Developer MCP no Codex](https://docs.xano.com/developer-mcp/clients/codex)
- [Xano Developer MCP](https://github.com/xano-inc/xano-developer-mcp)
- [XanoScript Language Support no Marketplace](https://marketplace.visualstudio.com/items?itemName=xano.xanoscript-language-server)
