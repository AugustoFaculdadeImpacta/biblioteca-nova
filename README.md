# Biblioteca Nova

Aplicação web feita com Python e Reflex. Este guia mostra como preparar o projeto
em um computador Windows novo e voltar a desenvolver.

## Requisitos

- Git
- Python 3.10 ou mais recente
- Acesso à internet para instalar as dependências e acessar a API da aplicação

## Preparação inicial neste computador

1. Instale o Git e o Python, se ainda não estiverem instalados. Durante a
   instalação do Python, habilite a opção para adicioná-lo ao `PATH`.
2. Abra o PowerShell e clone o repositório:

   ```powershell
   git clone https://github.com/AugustoFaculdadeImpacta/biblioteca-nova.git
   cd biblioteca-nova
   ```

   Se já recebeu o projeto de outra forma, entre no diretório que contém
   `rxconfig.py` em vez de cloná-lo novamente.
3. Confira se o Python está disponível:

   ```powershell
   py -3 --version
   ```

   Deve ser Python 3.10 ou mais recente.
4. Crie e ative um ambiente virtual Python para este projeto:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Quando estiver ativo, o PowerShell normalmente mostra `(.venv)` no início
   da linha de comando.
5. Instale as dependências definidas pelo projeto:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   O arquivo `requirements.txt` fixa a versão do Reflex usada pelo projeto.
6. Inicie a aplicação em modo de desenvolvimento:

   ```powershell
   reflex run
   ```

   Abra no navegador o endereço local indicado no terminal (normalmente
   `http://localhost:3000`). Deixe o terminal aberto enquanto estiver
   desenvolvendo; o Reflex atualiza a aplicação quando você salva alterações.
   Para parar o servidor, pressione `Ctrl+C`.

## Próximas vezes

Depois que o ambiente virtual e as dependências já tiverem sido criados, basta
abrir o PowerShell, entrar na pasta do projeto, ativar o ambiente e iniciar o
servidor:

```powershell
cd C:\caminho\para\biblioteca-nova
.\.venv\Scripts\Activate.ps1
reflex run
```

Substitua o caminho de exemplo pelo local em que o repositório está salvo.
Ative o ambiente virtual sempre antes de executar comandos do projeto.

## Observações

- Execute `reflex run` a partir da raiz do projeto, onde está `rxconfig.py`.
- Não é preciso executar `reflex init`: este projeto já está inicializado.
- O aplicativo usa uma API remota; ações que carregam ou salvam dados precisam
  de conexão com a internet e de que esse serviço esteja disponível.
- Se o PowerShell não encontrar `py`, instale o Python e habilite sua inclusão
  no `PATH`. Se não encontrar `reflex`, confirme que o ambiente virtual está
  ativo e que a instalação das dependências terminou sem erros.
