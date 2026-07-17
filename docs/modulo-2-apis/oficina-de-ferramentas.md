# Oficina de ferramentas: contrato, execução e comparação

Esta oficina usa dados sintéticos e dura aproximadamente noventa minutos na trilha essencial. Você executará a API FastAPI, observará `/docs`, importará OpenAPI no Bruno, validará o contrato com Spectral e rodará testes com `TestClient`. Nenhuma integração externa é chamada.

## Ferramenta

| Ferramenta | Papel | Evidência |
| --- | --- | --- |
| Python 3.11 ou superior | executar aplicação e testes | saída do pytest |
| FastAPI e Uvicorn | implementar e servir HTTP local | respostas e `/docs` |
| OpenAPI 3.1 | declarar contrato explícito | `openapi.yaml` |
| Bruno | atuar como consumidor manual | requisições e respostas salvas |
| Node.js e npx | executar Spectral localmente | relatório de lint |
| Spectral | verificar regras do documento | contrato válido e falha deliberada |

Bruno ajuda a executar exemplos, mas uma execução manual não substitui regressão. Spectral encontra problemas estruturais e de estilo, mas não prova que o servidor obedece ao documento. `TestClient` verifica o comportamento da implementação, mas não substitui a revisão semântica. Use as três perspectivas.

## Pré-requisitos

**Objetivo**

Preparar um ambiente local descartável com Python, Bruno e Node.js. Reserve uma janela com acesso à internet para instalar dependências e para a primeira execução do `npx`.

**Pré-requisito**

Tenha o repositório disponível e um editor de texto. Todos os comandos partem da raiz do repositório, exceto quando o texto manda entrar em `laboratorios/plataforma-hospitalar`.

## Instalação

### Windows

Abra PowerShell. Instale Python, Node.js LTS e Bruno quando ainda não estiverem disponíveis:

```powershell
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
winget install Bruno.Bruno
```

**Resultado esperado**

Cada instalador termina com confirmação. Feche e reabra o PowerShell para atualizar o `PATH`.

**Contingência**

Se `winget` não existir, use os instaladores oficiais indicados nas [referências](sintese-e-referencias.md#ferramentas). Se um pacote já estiver instalado, o gerenciador informa isso e você pode continuar.

Crie o ambiente e instale o laboratório. A ativação é opcional; os passos seguintes usam o interpretador explícito da `.venv`:

```powershell
cd laboratorios\plataforma-hospitalar
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe --version
node --version
npx --version
```

Use exatamente `.venv\Scripts\python.exe -m pip install -e ".[dev]"` para garantir que o pacote entre no ambiente criado.

**Resultado esperado**

Python informa versão 3.11 ou superior, Node e npx informam versões, e a instalação editável termina sem erro.

**Contingência**

Se `py` não encontrar Python, reabra o terminal e tente o caminho fornecido pelo instalador. Se a criação parcial da `.venv` falhar, remova apenas essa pasta e repita. Não altere política permanente do PowerShell.

### macOS

Com Homebrew disponível:

```bash
brew install python@3.12 node
brew install bruno
cd laboratorios/plataforma-hospitalar
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python --version
node --version
npx --version
```

**Resultado esperado**

O terminal mostra `(.venv)`, Python 3.11 ou superior e versões de Node e npx.

**Contingência**

Se o Homebrew expuser `python3` em vez de `python3.12`, use `python3 -m venv .venv`. Se Bruno já existir, apenas abra o aplicativo.

### Linux

Os comandos usam Debian ou Ubuntu. Instale equivalentes na sua distribuição quando necessário:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm flatpak
flatpak install flathub com.usebruno.Bruno
cd laboratorios/plataforma-hospitalar
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python --version
node --version
npx --version
```

**Resultado esperado**

As versões aparecem e o Flatpak confirma a instalação do Bruno.

**Contingência**

Se o repositório da distribuição fornecer Node antigo incompatível com Spectral, instale uma versão LTS pelas instruções oficiais do Node.js. Se Flatpak não estiver configurado, use o pacote oficial do Bruno adequado à distribuição.

## Preparação do laboratório

### Essencial em aula

**Execute**

Confirme que está em `laboratorios/plataforma-hospitalar`. Crie uma pasta para evidências e execute todos os testes atuais.

No PowerShell:

```powershell
New-Item -ItemType Directory -Force evidencias
.venv\Scripts\python.exe -m pytest tests -q
```

Em macOS ou Linux:

```bash
mkdir -p evidencias
python -m pytest tests -q
```

**Resultado esperado**

O pytest encerra com todos os testes aprovados. O número total pode crescer em módulos posteriores; neste encontro, procure especificamente os seis testes de `test_api_contract.py`.

**Contingência**

Se `hospital.api` não for encontrado, repita a instalação editável com o interpretador da `.venv`. Se uma porta estiver ocupada, os testes ainda funcionam porque `TestClient` não abre servidor.

**Observe**

Abra `contratos/openapi.yaml`, `src/hospital/api/models.py`, `src/hospital/api/main.py` e `tests/test_api_contract.py`. Localize as duas operações, os schemas `PedidoElegibilidade`, `ElegibilidadeAceita` e `ErroAPI`, o status `202` e o cabeçalho `Location`.

### Exploração em dupla

**Execute**

Uma pessoa lê somente o OpenAPI e prevê as respostas. A outra lê somente os testes e identifica o que é comprovado. Depois comparem listas. Registrem uma promessa documentada que o teste ainda não verifica e uma asserção do teste que depende do contrato.

**Compare**

Contrato, teste e implementação têm sobreposição, mas não são equivalentes. A descrição explica intenção; o teste escolhe amostras; o código executa muitos casos possíveis.

### Extensão

**Execute**

Abra `.spectral.yaml`. As regras exigem tags, descrição e `operationId` em cada operação. Explique como cada item ajuda consumidores ou automação e identifique uma regra semântica que o linter não conseguiria decidir sozinho.

## Execução

### Essencial em aula

**Execute**

Inicie a API em um terminal dedicado. No PowerShell:

```powershell
.venv\Scripts\python.exe -m uvicorn hospital.api.main:app --reload
```

Em macOS ou Linux:

```bash
python -m uvicorn hospital.api.main:app --reload
```

**Resultado esperado**

Uvicorn informa que está atendendo em `http://127.0.0.1:8000`. Mantenha esse terminal aberto.

**Contingência**

Se a porta 8000 estiver ocupada, encerre o processo antigo. Usar outra porta exigirá também alterar a URL no Bruno; não edite o contrato principal apenas por esse conflito local.

Abra `http://127.0.0.1:8000/docs`. Expanda `POST /elegibilidades`, use **Try it out**, mantenha o exemplo e execute.

**Resultado esperado**

A documentação mostra `202`, corpo com protocolo e o cabeçalho `location`. Copie o protocolo para a evidência.

**Contingência**

Se `/docs` não abrir, confira o log do terminal e acesse `http://127.0.0.1:8000/openapi.json`. Se o JSON abrir, recarregue `/docs`; se não abrir, a aplicação não está atendendo.

Abra o Bruno e escolha a opção de importar uma coleção a partir de OpenAPI. Selecione `contratos/openapi.yaml`, escolha uma pasta dentro de `evidencias/bruno` e confirme a importação. Defina a URL base como `http://127.0.0.1:8000` se o importador não a definir.

**Resultado esperado**

Bruno cria requisições para `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`.

**Contingência**

Se a interface não localizar o importador, consulte a opção **Import Collection** e escolha **OpenAPI**. Se o arquivo não for aceito, valide-o com Spectral no passo seguinte antes de alterar a coleção.

No Bruno, envie o `POST` com:

```json
{
  "cpf": "12345678901",
  "codigo_operadora": "OPS-001",
  "matricula_plano": "MAT-2026-001"
}
```

**Resultado esperado**

A resposta é `202 Accepted`, contém `situacao` igual a `recebida` e apresenta `Location`. Copie o protocolo para o parâmetro do `GET` e envie a consulta; o resultado é `200 OK` com o mesmo protocolo.

**Contingência**

Se o `GET` retornar `404`, confirme que usa a mesma instância do servidor e que o protocolo não contém aspas ou espaços. Reiniciar Uvicorn limpa a memória; nesse caso, crie outro pedido.

Remova `cpf` do corpo e envie outro `POST`.

**Resultado esperado**

A resposta é `422 Unprocessable Entity`, com `codigo` igual a `dados_invalidos` e um detalhe cujo `campo` é `body.cpf`.

**Contingência**

Se receber `202`, confirme que o campo foi removido do corpo efetivamente enviado e não apenas de um exemplo exibido.

Valide o contrato. No PowerShell:

```powershell
npx @stoplight/spectral-cli lint contratos/openapi.yaml 2>&1 | Tee-Object -FilePath evidencias\spectral-valido.txt
```

Em macOS ou Linux:

```bash
npx @stoplight/spectral-cli lint contratos/openapi.yaml 2>&1 | tee evidencias/spectral-valido.txt
```

**Resultado esperado**

Spectral termina com `No results with a severity of 'error' found!` e código de saída zero. Na primeira execução, `npx` pode solicitar confirmação para obter o pacote.

**Contingência**

Se `npx` não for reconhecido, retorne à instalação do Node. Se houver erro de rede, repita quando a conexão estiver disponível; não interprete ausência de execução como contrato válido.

Execute somente os testes de contrato e capture o resultado. No PowerShell:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_api_contract.py -q 2>&1 | Tee-Object -FilePath evidencias\testes-contrato.txt
```

Em macOS ou Linux:

```bash
python -m pytest tests/test_api_contract.py -q 2>&1 | tee evidencias/testes-contrato.txt
```

**Resultado esperado**

O resumo mostra `6 passed`.

**Contingência**

Leia o primeiro teste que falhou. Erro de conexão indica que você executou outro cliente, pois `TestClient` não depende de Uvicorn. Erro de exemplo indica possível divergência entre YAML e aplicação.

### Exploração em dupla

**Execute**

Copie o contrato para não modificar a baseline. No PowerShell:

```powershell
Copy-Item contratos\openapi.yaml evidencias\openapi-experimento.yaml
```

Em macOS ou Linux:

```bash
cp contratos/openapi.yaml evidencias/openapi-experimento.yaml
```

**Resultado esperado**

O arquivo de experimento aparece em `evidencias`.

**Contingência**

Se o destino não existir, volte à preparação e crie a pasta `evidencias`.

No arquivo copiado, altere apenas o exemplo de `cpf` de `12345678901` para `123`. Valide a cópia:

```bash
npx @stoplight/spectral-cli lint evidencias/openapi-experimento.yaml
```

O mesmo comando funciona no PowerShell.

**Resultado esperado**

Spectral aponta que o exemplo não corresponde ao pattern de onze dígitos e termina com código diferente de zero. Essa falha é evidência desejada do experimento.

**Contingência**

Se não houver falha, confirme que alterou o valor em `components.schemas.PedidoElegibilidade.examples` e que `.spectral.yaml` continua acessível. Compare também com o servidor: enviar `cpf` igual a `123` deve produzir `422`.

**Compare**

Explique por que o contrato alterado falha antes de chamar a API e por que o servidor continua rejeitando o mesmo valor. Depois restaure a cópia ou mantenha-a somente como evidência da falha deliberada; não substitua `contratos/openapi.yaml`.

### Extensão

**Execute**

Leia `app.openapi()` no teste e acrescente, em uma cópia de estudo, uma comparação entre os status documentados e gerados. Não altere a API pública. Discuta que divergências são incompatibilidades e quais são apenas diferenças de descrição.

## Resultado esperado

Ao final, você terá observado `202`, `Location`, recuperação por `GET`, erro `422`, lint aprovado, lint deliberadamente reprovado e seis testes aprovados. Mais importante: conseguirá dizer qual ferramenta examina documento, implementação ou experiência do consumidor.

## Interpretação

O experimento demonstra que exemplos podem ser executáveis, que erros são parte do contrato e que semântica HTTP comunica estado temporal. Ele não demonstra persistência, segurança, escalabilidade ou integração externa. Reiniciar o servidor prova o limite do armazenamento em memória.

## Limpeza e contingência

**Execute**

No terminal do Uvicorn, pressione `Ctrl+C`. Feche o Bruno. Remova apenas artefatos descartáveis se não precisar entregá-los.

No PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
```

Em macOS ou Linux:

```bash
rm -rf .venv
```

**Resultado esperado**

O servidor para e o ambiente local é removido. `contratos`, `src` e `tests` permanecem.

**Contingência**

Se algum arquivo estiver em uso no Windows, feche terminais e editor ligados à `.venv` antes de repetir. Nunca remova a pasta do laboratório inteira para limpar o ambiente.

## Evidência a entregar

Entregue `spectral-valido.txt`, `testes-contrato.txt`, a coleção Bruno importada, respostas de `POST`, `GET` e `422`, e uma nota curta comparando contrato explícito, contrato gerado e execução. Inclua a falha deliberada sem apresentá-la como defeito pendente.

## Questões exploratórias

1. O que `202` permite ao provedor mudar sem quebrar o consumidor?
2. Por que `Location` é melhor que pedir ao consumidor para montar uma URL por convenção?
3. Qual divergência entre OpenAPI e aplicação os testes atuais ainda não detectam?
4. Quando uma chave de idempotência passaria a ser necessária?
5. Que parte do experimento deixaria de funcionar com duas instâncias e memória separada?
