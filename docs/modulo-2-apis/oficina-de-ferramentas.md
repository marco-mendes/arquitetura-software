# Oficina de ferramentas: contrato, execução e comparação

Esta oficina usa dados sintéticos e dura aproximadamente noventa minutos na trilha essencial. Você executará a API FastAPI, observará `/docs`, importará OpenAPI no Bruno, validará o contrato com Spectral e rodará testes com `TestClient`. Nenhuma integração externa é chamada. Ao final há uma extensão opcional em .NET que coloca um gateway de API com Ocelot na frente de dois serviços.

## O que existe antes de você abrir o terminal

Você trabalhará no repositório desta disciplina, dentro de `laboratorios/plataforma-hospitalar`. Essa pasta contém uma aplicação didática local chamada **API de elegibilidades da plataforma hospitalar**. Ela não consulta uma operadora real, não acessa prontuários e não envia dados para fora do seu computador. Seu objetivo é tornar observável um contrato HTTP pequeno, não simular uma plataforma hospitalar completa.

O arquivo `src/hospital/api/main.py` inicia a aplicação FastAPI e expõe apenas duas operações públicas:

| Operação | O que faz nesta oficina | Resultado observável |
| --- | --- | --- |
| `POST /elegibilidades` | recebe CPF sintético, código de operadora e matrícula; valida o contrato e aceita o pedido | `202 Accepted`, corpo com `protocolo` e cabeçalho `Location` |
| `GET /elegibilidades/{protocolo}` | recupera o pedido aceito usando o protocolo retornado no `POST` | `200 OK` com a representação; `404` se o protocolo não existir |

Os dados aceitos ficam somente na memória do processo. Isso significa que parar ou reiniciar o servidor remove todos os protocolos criados. Esse limite é deliberado: a prática permite comparar contrato, consumo e implementação sem afirmar persistência, idempotência distribuída, autenticação ou integração externa.

Antes de instalar ou executar qualquer coisa, localize a raiz do clone e a pasta do laboratório:

```text
arquitetura-software/
└── laboratorios/
    └── plataforma-hospitalar/   ← os comandos desta oficina passam a ser executados aqui
        ├── contratos/openapi.yaml
        ├── src/hospital/api/main.py
        └── tests/test_api_contract.py
```

Quatro arquivos sustentam a oficina inteira. Vale abrir cada um antes de rodar qualquer comando; os links vão direto ao código no GitHub, para quem está lendo pelo site sem o repositório clonado.

| Arquivo | O que ele faz | Onde isso aparece na teoria |
| --- | --- | --- |
| [`contratos/openapi.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/contratos/openapi.yaml) | O contrato escrito à mão: as duas operações, os schemas e os exemplos que a API promete a quem consome. | É o **contrato** de [interface, contrato e implementação](conceitos.md), publicado num documento que existe independente do código. |
| [`src/hospital/api/models.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/src/hospital/api/models.py) | Os modelos Pydantic. O tipo declarado em cada campo é a própria regra de validação. | Onde o contrato deixa de ser documento e passa a ser código executável. |
| [`src/hospital/api/main.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/src/hospital/api/main.py) | A aplicação FastAPI: as duas rotas, o `202` com `Location` e os erros estruturados. | A **implementação**, que pode mudar por dentro sem quebrar quem consome, desde que o contrato fique de pé. |
| [`tests/test_api_contract.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/tests/test_api_contract.py) | Sete testes: cinco exercitam a API pela porta da frente, dois comparam o contrato publicado com o que o FastAPI gera. | A verificação de que a promessa publicada e o comportamento real não divergiram. |

Cada teste desse arquivo abre com uma explicação do que ele prova e por que aquilo importa. Ler os testes antes de rodá-los costuma ensinar mais sobre o contrato do que ler o próprio `openapi.yaml`.

A preparação termina quando quatro condições valem ao mesmo tempo. Existe uma pasta `.venv` e o interpretador dela responde com a versão do Python. O comando `python -m pytest tests/test_api_contract.py -q` termina com os testes aprovados. E o servidor, ao subir, informa que está atendendo em `http://127.0.0.1:8000`. Só então vale abrir `/docs` ou o Bruno.

## Ferramenta

| Ferramenta | Papel | Evidência |
| --- | --- | --- |
| Python 3.11 ou superior | executar aplicação e testes | saída do pytest |
| FastAPI e Uvicorn | implementar e servir HTTP local | respostas e `/docs` |
| OpenAPI 3.1 | declarar contrato explícito | `openapi.yaml` |
| Bruno | atuar como consumidor manual | requisições e respostas salvas |
| Node.js e npx | executar Spectral localmente | relatório de lint |
| Spectral CLI 6.16.1 | verificar regras do documento | contrato válido e falha deliberada |

Bruno ajuda a executar exemplos, mas uma execução manual não substitui regressão. Spectral encontra problemas estruturais e de estilo sem provar que o servidor obedece ao documento. Já o `TestClient` verifica o comportamento da implementação; a revisão semântica do contrato continua sendo trabalho humano. Use as três perspectivas.

## Pré-requisitos

**Objetivo**

Preparar um ambiente local descartável com Python, Bruno e Node.js. Reserve uma janela com acesso à internet para instalar dependências e para a primeira execução do `npx`. A oficina fixa Spectral CLI em `6.16.1` para tornar regras e diagnósticos reproduzíveis.

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

Se `winget` não existir, siga as [instruções oficiais de instalação do Python](https://docs.python.org/3/using/index.html) e os instaladores indicados nas [referências](sintese-e-referencias.md#ferramentas). Se um pacote já estiver instalado, continue.

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

Instale primeiro o [Homebrew pelo site oficial](https://brew.sh/) quando ele ainda não existir. Depois execute:

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
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.usebruno.Bruno
flatpak info com.usebruno.Bruno
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

As versões aparecem; `flatpak info` mostra nome, versão e origem do Bruno.

**Contingência**

Se `remote-add` falhar, execute `flatpak remotes` e confirme se `flathub` já existe; uma origem existente permite continuar. Se a distribuição fornecer Node antigo, instale uma versão LTS pelas instruções oficiais do Node.js. Como alternativa ao Flatpak, use os [pacotes oficiais do Bruno](https://www.usebruno.com/downloads).

## Preparação do laboratório

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

A última linha traz a contagem. É isso que você deve ver:

```text
.......                                                                  [100%]
=============================== warnings summary ===============================
.venv/lib/python3.13/site-packages/fastapi/testclient.py:1
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
7 passed, 1 warning in 0.73s
```

Cada `.` na primeira linha representa um teste aprovado, e são sete. O aviso sobre `httpx` vem de dentro do FastAPI e não indica problema no laboratório. O número total pode crescer em módulos posteriores; neste encontro, procure os sete testes de `test_api_contract.py`.

**Contingência**

Se `hospital.api` não for encontrado, repita a instalação editável com o interpretador da `.venv`.

**Observe**

O mesmo contrato aparece em quatro formas nesta pasta, e vale ver como cada uma expressa a mesma regra.

Em `src/hospital/api/models.py`, a regra é o tipo. O campo `cpf` é declarado como `Field(pattern=r"^\d{11}$")`, exigindo onze dígitos. Essa linha executa a validação por si mesma, sem precisar de código adicional que a interprete. `codigo_operadora` e `matricula_plano` declaram limites de tamanho da mesma maneira. E `model_config = ConfigDict(extra="forbid")` é o que faz um campo não previsto ser recusado em vez de silenciosamente ignorado.

Em `src/hospital/api/main.py`, a rota `POST` declara `status_code=status.HTTP_202_ACCEPTED` e, mais abaixo, escreve o cabeçalho `Location` à mão com o endereço do protocolo recém-criado. O `404` da rota `GET` também aparece ali, montado no mesmo formato de erro do `422`.

Em `contratos/openapi.yaml`, essas mesmas decisões estão escritas para quem consome, sem depender de ler Python. `PedidoElegibilidade` é o que se envia, `ElegibilidadeAceita` é o que volta no `202` e `ErroAPI` é o formato único de erro da API inteira.

Em `tests/test_api_contract.py`, cada uma dessas promessas vira uma verificação executável.

**Compare**

Nenhuma dessas quatro formas torna as outras dispensáveis, e é comum tratá-las como se fossem intercambiáveis. O `openapi.yaml` é a única que quem consome consegue ler sem acesso ao código, mas ele não executa nada: pode prometer um comportamento que a aplicação abandonou meses atrás. Os testes executam, só que apenas nas amostras que alguém teve o trabalho de escrever. Já o código atende qualquer caso que apareça, sem explicar em lugar nenhum por que aquele limite de onze dígitos existe.

## O que os testes estão verificando

Esta é a parte do laboratório que costuma ser executada sem ser lida. Vale abrir [`tests/test_api_contract.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/tests/test_api_contract.py) antes de rodar o pytest, porque o arquivo é a descrição executável do contrato que você acabou de ler em YAML.

Três elementos aparecem no topo do arquivo e explicam o resto:

- O `TestClient` chama a aplicação FastAPI diretamente, em memória, sem abrir porta nem subir Uvicorn. Por isso os testes rodam mesmo com a porta 8000 ocupada, e por isso um erro de conexão neles indica que você executou outro cliente por engano.
- O `setup_function` roda antes de cada teste e limpa os pedidos guardados. Como a aplicação mantém tudo em memória, sem essa limpeza um teste enxergaria os protocolos criados pelo anterior e passaria a depender da ordem de execução.
- O `PEDIDO_VALIDO` é o corpo sintético reaproveitado pelos testes, com CPF e matrícula que não existem fora deste laboratório.

Os sete testes se dividem em dois grupos, e a diferença entre eles é o assunto do módulo:

| Grupo | Testes | O que provam |
| --- | --- | --- |
| Comportamento da API | os cinco primeiros | Que a aplicação responde o que promete: `202` com `Location`, recuperação pelo `GET`, `422` com corpo estruturado para campo ausente e para campo a mais, `404` no mesmo formato de erro, e a distinção entre processo vivo e pronto para receber tráfego. |
| Acordo entre os dois contratos | os dois últimos | Que o `openapi.yaml` publicado e o contrato que o FastAPI gera a partir do código dizem a mesma coisa, e que os exemplos declarados no YAML são aceitos pela aplicação de verdade. |

O segundo grupo é o que pega o erro mais caro do módulo: alguém altera o código, o contrato gerado acompanha automaticamente, e o documento publicado continua prometendo o formato antigo para quem consome. Cada teste do arquivo abre com um texto explicando o que prova e por quê.

Vale saber também o que esses testes **não** cobrem. Eles comparam operações, campos obrigatórios e a resposta `202`, e não os dois documentos inteiros — uma comparação total quebraria a cada diferença de formatação. Descrições divergentes em outras respostas, exemplos ausentes e mudanças de significado num campo que manteve o mesmo tipo passariam sem alarme.

## As regras que o Spectral aplica

O **Spectral** é um verificador de contratos: ele lê um documento OpenAPI e reclama do que estiver fora das regras. Serve para o contrato, assim como um verificador de estilo de código serve para o código. Quem define essas regras é um arquivo de configuração, e neste laboratório ele está dividido em dois.

O `.spectral.yaml` da raiz tem apenas duas linhas úteis: ele aponta para o arquivo de dentro de `contratos/`. Essa indireção existe para que os comandos possam ser executados da raiz do laboratório enquanto a configuração vive ao lado do contrato que ela governa.

O `contratos/.spectral.yaml` é onde as decisões estão:

```yaml
extends: spectral:oas

rules:
  operation-operationId: error
  operation-description: error
  operation-tags: error
```

A primeira linha herda o conjunto de regras que o próprio Spectral distribui para OpenAPI, chamado `spectral:oas`. São dezenas de verificações prontas, e é dele que vem o `oas3-valid-media-example` que aparecerá mais adiante quando quebrarmos um exemplo de propósito.

O bloco `rules` acrescenta três exigências e as marca como `error`, e não como aviso. A diferença importa: `error` faz o comando terminar com código diferente de zero, o que reprova uma esteira de integração contínua. Aviso apenas imprime texto e deixa passar.

Cada uma das três exigências atende a um interessado concreto. O `operationId` é um identificador único da operação, e geradores de cliente o usam para nomear o método que vão criar — sem ele, o método sai com nome automático e ilegível. A descrição atende quem vai ler a documentação e decidir se aquela operação serve. As tags agrupam operações, o que só faz diferença quando a API cresce e a página de documentação precisa de navegação.

O que o Spectral **não** consegue fazer é julgar significado. Ele verifica que existe uma descrição, sem ter como saber se ela descreve a operação corretamente: um `POST /elegibilidades` descrito como "remove um beneficiário" passa na verificação. Decidir se o contrato diz a verdade sobre a intenção continua sendo trabalho humano, e é por isso que revisão de contrato não se automatiza inteira.

## Execução

Os blocos a seguir sobem a API e observam o contrato de três ângulos: pela documentação que o próprio FastAPI gera, por um cliente HTTP externo e pelos testes automatizados. Cada ângulo enxerga uma coisa que os outros dois não enxergam.

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

O terminal fica ocupado pelo servidor e mostra:

```text
INFO:     Will watch for changes in these directories: ['.../plataforma-hospitalar']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [41287] using StatReload
INFO:     Started server process [41289]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

`Application startup complete` é a linha que confirma que a API está no ar. O terminal não volta ao prompt: ele fica preso servindo requisições, e é assim mesmo. Deixe essa janela aberta e use outra para os comandos seguintes. Cada chamada que você fizer aparecerá aqui como uma linha de log.

**Contingência**

Se a porta 8000 estiver ocupada, encerre o processo antigo. Usar outra porta exigirá também alterar a URL no Bruno; não edite o contrato principal apenas por esse conflito local.

Abra `http://127.0.0.1:8000/docs`. Expanda `POST /elegibilidades`, use **Try it out**, mantenha o exemplo e execute.

**Resultado esperado**

A documentação mostra `202`, corpo com protocolo e o cabeçalho `location`. Copie o protocolo para a evidência.

**Observe**

Essa página não foi escrita por ninguém. O FastAPI a monta em tempo de execução a partir dos modelos Pydantic e das assinaturas das rotas, e é por isso que ela nunca fica desatualizada em relação ao código. É o **contrato gerado**, e ele descreve o que a aplicação faz hoje. Note que ele coexiste com o `openapi.yaml` escrito à mão, que é a promessa publicada — os dois podem divergir, e os dois últimos testes existem exatamente para detectar isso.

**Contingência**

Se `/docs` não abrir, acesse `http://127.0.0.1:8000/openapi.json`. Se o JSON abrir, recarregue `/docs`; se não abrir, a aplicação não está atendendo.

Abra o Bruno e escolha a opção de importar uma coleção a partir de OpenAPI. Selecione `contratos/openapi.yaml`, escolha uma pasta dentro de `evidencias/bruno` e confirme a importação. Defina a URL base como `http://127.0.0.1:8000` se o importador não a definir.

**Resultado esperado**

Bruno cria requisições para `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`.

**Observe**

O que acabou de acontecer é a razão de o contrato existir em formato de máquina. O Bruno nunca viu esta API nem teve acesso ao código. Ele leu o `openapi.yaml` e montou sozinho as duas requisições, com os campos certos. Um consumidor real faz o mesmo para gerar clientes em outra linguagem. É isso que se perde quando a documentação é apenas um texto em prosa.

**Contingência**

Se a interface não localizar o importador, consulte a opção **Import Collection** e escolha **OpenAPI**.

No Bruno, envie o `POST` com:

```json
{
  "cpf": "12345678901",
  "codigo_operadora": "OPS-001",
  "matricula_plano": "MAT-2026-001"
}
```

**Resultado esperado**

A resposta completa, com cabeçalhos e corpo:

```text
HTTP/1.1 202 Accepted
server: uvicorn
content-type: application/json
location: /elegibilidades/3d1bbeb6-92a7-4aab-a7ec-62df7296a580

{"protocolo":"3d1bbeb6-92a7-4aab-a7ec-62df7296a580","situacao":"recebida","criado_em":"2026-09-01T00:26:22.639666Z"}
```

O identificador será diferente no seu computador, porque é gerado a cada pedido. Repare que o valor depois de `location:` é o mesmo `protocolo` do corpo, montado como caminho. Copie o protocolo para o parâmetro do `GET` e envie a consulta: o resultado é `200 OK` com exatamente o mesmo corpo.

**Observe**

O `202` diz "recebi e ainda vou processar", e não "pronto". É por isso que a resposta não traz o resultado da elegibilidade: traz um protocolo e o endereço onde consultá-lo. O cabeçalho `Location` entrega esse endereço pronto, poupando o consumidor de montar a URL por convenção — e permitindo que o provedor mude o formato dela sem quebrar ninguém.

**Compare**

Compare com o que aconteceria num `200` que devolvesse a decisão na hora. O `202` compra o direito de processar depois, e cobra do consumidor uma segunda chamada. É a mesma escolha de [interface, contrato e implementação](conceitos.md) sendo exercida no nível do código de status.

**Contingência**

Se o `GET` retornar `404`, confirme que usa a mesma instância do servidor e que o protocolo não contém aspas ou espaços. Reiniciar Uvicorn limpa a memória; nesse caso, crie outro pedido.

Remova `cpf` do corpo e envie outro `POST`.

**Resultado esperado**

A resposta é `422 Unprocessable Entity`, e o corpo detalha o motivo:

```json
{
  "codigo": "dados_invalidos",
  "mensagem": "A requisição não atende ao contrato.",
  "detalhes": [
    {
      "campo": "body.cpf",
      "mensagem": "Field required",
      "tipo": "missing"
    }
  ]
}
```

O campo `detalhes` aponta exatamente onde está o problema: `body.cpf`, ausente. Um cliente consegue tratar isso programaticamente, destacando o campo no formulário do usuário.

**Observe**

O corpo do erro tem formato previsível: `codigo`, `mensagem` e a lista `detalhes` apontando o campo problemático. Isso permite que o consumidor trate a falha programaticamente, em vez de exibir texto solto ao usuário. O erro faz parte do contrato tanto quanto o caminho feliz.

**Compare**

Compare esse `422` com um `500`. O primeiro diz "seu pedido está errado, e aqui está onde"; o segundo diz "algo quebrou aqui dentro". Trocar um pelo outro transfere ao consumidor a culpa por um defeito do provedor, ou o contrário.

**Contingência**

Se receber `202`, confirme que o campo foi removido do corpo efetivamente enviado e não apenas de um exemplo exibido.

Valide o contrato. No PowerShell:

```powershell
npx @stoplight/spectral-cli@6.16.1 lint contratos/openapi.yaml 2>&1 | Tee-Object -FilePath evidencias\spectral-valido.txt
$spectralExit = $LASTEXITCODE
if ($spectralExit -ne 0) { exit $spectralExit }
```

Em macOS ou Linux:

```bash
set -o pipefail
npx @stoplight/spectral-cli@6.16.1 lint contratos/openapi.yaml 2>&1 | tee evidencias/spectral-valido.txt
```

**Resultado esperado**

Uma única linha, e é a que você quer ver:

```text
No results with a severity of 'error' found!
```

O comando também termina com código de saída zero, que é o que uma esteira de integração contínua verifica. Na primeira execução o `npx` baixa a versão `6.16.1` e demora mais.

**Contingência**

Se `npx` não for reconhecido, retorne à instalação do Node. Se houver erro de rede, repita quando a conexão estiver disponível; não interprete ausência de execução como contrato válido.

Execute somente os testes de contrato e capture o resultado. No PowerShell:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_api_contract.py -q 2>&1 | Tee-Object -FilePath evidencias\testes-contrato.txt
$pytestExit = $LASTEXITCODE
if ($pytestExit -ne 0) { exit $pytestExit }
```

Em macOS ou Linux:

```bash
set -o pipefail
python -m pytest tests/test_api_contract.py -q 2>&1 | tee evidencias/testes-contrato.txt
```

**Resultado esperado**

O resumo mostra `7 passed`.

**Observe**

Os sete testes não fazem a mesma coisa. Cinco chamam a API pela porta da frente e conferem status, corpo e cabeçalho. Os dois últimos comparam o `openapi.yaml` publicado com o contrato que o FastAPI gera a partir do código, que é onde uma divergência costuma passar despercebida: o código muda, o contrato gerado acompanha, e o documento publicado continua prometendo o formato antigo.

**Compare**

Compare o alcance de cada ferramenta desta oficina. O Spectral olha o documento e não sabe se a aplicação obedece. O Bruno mostra uma execução real e não protege contra regressão. Os testes verificam o comportamento e só cobrem os casos que alguém escreveu. Nenhuma das três dispensa a revisão humana da semântica do contrato.

**Contingência**

Leia o primeiro teste que falhou. Erro de conexão indica que você executou outro cliente, pois `TestClient` não depende de Uvicorn. Erro de exemplo indica possível divergência entre YAML e aplicação.

## Uma falha deliberada no contrato

Até aqui tudo passou. Um contrato só se mostra útil quando alguém quebra e o mecanismo acusa, então este bloco introduz um erro de propósito e observa quem o detecta.

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

No arquivo copiado, altere somente `cpf` de `12345678901` para `123` no exemplo de mídia da requisição. O caminho YAML completo é `paths./elegibilidades.post.requestBody.content.application/json.examples.pedidoValido.value.cpf`. Não altere a anotação `examples` do schema em `components`.

Valide a cópia no PowerShell e confirme que a falha realmente ocorreu:

```powershell
npx @stoplight/spectral-cli@6.16.1 lint evidencias\openapi-experimento.yaml
$spectralExit = $LASTEXITCODE
if ($spectralExit -eq 0) { throw "O exemplo inválido não foi detectado." }
$spectralExit
```

Em macOS ou Linux:

```bash
set +e
npx @stoplight/spectral-cli@6.16.1 lint evidencias/openapi-experimento.yaml
spectral_exit=$?
set -e
test "$spectral_exit" -ne 0
printf 'Código esperado: %s\n' "$spectral_exit"
```

**Resultado esperado**

Desta vez o Spectral acusa, e a saída aponta o lugar exato:

```text
/caminho/para/evidencias/openapi-experimento.yaml
 35:24  error  oas3-valid-media-example  "cpf" property must match pattern "^\d{11}$"  paths./elegibilidades.post.requestBody.content.application/json.examples.pedidoValido.value.cpf

✖ 1 problem (1 error, 0 warnings, 0 infos, 0 hints)
```

Vale ler essa saída por partes. O `35:24` é linha e coluna do erro. O `oas3-valid-media-example` é o nome da regra violada, herdada do conjunto `spectral:oas`. A mensagem diz qual restrição foi quebrada, e o caminho ao final localiza o campo dentro da estrutura do documento. O comando termina com código `1`, que é o que reprovaria uma esteira de integração contínua. **Essa falha é a evidência que você deve guardar.**

**Contingência**

Se não houver falha, confirme o caminho `paths./elegibilidades.post.requestBody.content.application/json.examples.pedidoValido.value.cpf`, preserve aspas em `'123'` e verifique se `.spectral.yaml` está na raiz do laboratório. Alterar `components.schemas.PedidoElegibilidade.examples` não exercita a regra de exemplo de mídia. No servidor, `cpf` igual a `123` também deve produzir `422`.

**Observe**

O erro foi detectado sem que a API fosse chamada. O Spectral leu apenas o documento e percebeu que o exemplo publicado viola o padrão declarado pelo próprio contrato. Um exemplo desatualizado é pior que exemplo nenhum, porque quem consome copia e não funciona.

**Compare**

Compare os dois momentos em que esse `cpf` inválido seria barrado. O Spectral barra na leitura do documento, antes de qualquer execução. O servidor barra na chamada, devolvendo `422`. São defesas em camadas diferentes, e a primeira é mais barata porque acontece antes de o código rodar.

Mantenha a cópia como evidência da falha deliberada e não substitua `contratos/openapi.yaml`.

## Extensão: gateway de API com Ocelot em .NET

Esta extensão é opcional e independente da trilha essencial: nada do que segue altera a API de elegibilidades. Ela demonstra o padrão de **gateway de API** com o [Ocelot](https://ocelot.readthedocs.io/), um gateway leve para .NET configurado por um arquivo JSON declarativo. Um processo na porta 4000 vira a única entrada para duas APIs internas nas portas 5001 e 5002, reescrevendo os caminhos públicos `/api/...` para os serviços de destino.

**Objetivo**

Observar um gateway roteando requisições por configuração declarativa, sem lógica de negócio própria: o consumidor enxerga uma única origem, e a topologia interna fica livre para mudar sem quebrar quem consome.

**Pré-requisito**

SDK do .NET 8 ou superior, verificado com `dotnet --version`. Instale com `winget install Microsoft.DotNet.SDK.8` no Windows, `brew install --cask dotnet-sdk` no macOS ou pelos [pacotes oficiais do .NET](https://dotnet.microsoft.com/download) no Linux. Reserve três terminais e as portas 4000, 5001 e 5002. Crie os projetos numa pasta de trabalho fora do clone da disciplina.

**Execute**

Crie os três projetos e adicione o pacote do Ocelot ao gateway. Os comandos do `dotnet` são idênticos no PowerShell, no macOS e no Linux; execute-os na pasta de trabalho:

```bash
dotnet new web -n ClienteService
dotnet new web -n ProdutoService
dotnet new web -n OcelotGateway
dotnet add OcelotGateway package Ocelot
```

Substitua o `Program.cs` do `ClienteService`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/clientes", () => new[] {
    new { Id = 1, Nome = "João Silva" },
    new { Id = 2, Nome = "Maria Oliveira" }
});

app.Run();
```

Substitua o `Program.cs` do `ProdutoService`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/produtos", () => new[] {
    new { Id = 1, Nome = "Produto A" },
    new { Id = 2, Nome = "Produto B" }
});

app.Run();
```

No `OcelotGateway`, substitua o `Program.cs` e crie um arquivo `ocelot.json` na raiz do projeto:

```csharp
using Ocelot.DependencyInjection;
using Ocelot.Middleware;

var builder = WebApplication.CreateBuilder(args);

builder.Configuration.AddJsonFile("ocelot.json", optional: false, reloadOnChange: true);
builder.Services.AddOcelot(builder.Configuration);

var app = builder.Build();

await app.UseOcelot();

app.Run();
```

```json
{
  "Routes": [
    {
      "DownstreamPathTemplate": "/clientes",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{ "Host": "localhost", "Port": 5001 }],
      "UpstreamPathTemplate": "/api/clientes"
    },
    {
      "DownstreamPathTemplate": "/produtos",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{ "Host": "localhost", "Port": 5002 }],
      "UpstreamPathTemplate": "/api/produtos"
    }
  ],
  "GlobalConfiguration": {
    "BaseUrl": "http://localhost:4000"
  }
}
```

Cada rota declara o caminho público (`UpstreamPathTemplate`) e o destino interno (`DownstreamPathTemplate`, esquema, host e porta). Para repassar subcaminhos inteiros a um serviço, o Ocelot aceita o coringa `{everything}` nos dois templates — por exemplo, `/api/clientes/{everything}` para `/clientes/{everything}`.

Inicie cada processo no próprio terminal, sempre a partir da pasta de trabalho:

```bash
dotnet run --project ClienteService --urls=http://localhost:5001
dotnet run --project ProdutoService --urls=http://localhost:5002
dotnet run --project OcelotGateway --urls=http://localhost:4000
```

Com os três processos ativos, consulte os serviços pelo gateway. No PowerShell:

```powershell
Invoke-RestMethod http://localhost:4000/api/clientes
Invoke-RestMethod http://localhost:4000/api/produtos
```

Em macOS ou Linux:

```bash
curl -s http://localhost:4000/api/clientes
curl -s http://localhost:4000/api/produtos
```

**Resultado esperado**

O gateway responde `200 OK` com os JSON dos serviços internos — clientes com João Silva e Maria Oliveira, produtos com Produto A e Produto B — sem que o consumidor conheça as portas 5001 e 5002. Consultar `http://localhost:5001/clientes` diretamente devolve o mesmo corpo: o gateway não transformou a resposta, apenas roteou a requisição.

**Contingência**

Se `dotnet` não for reconhecido, reabra o terminal após instalar o SDK. Se uma porta estiver ocupada, encerre o processo antigo ou ajuste a porta no `--urls` e no `ocelot.json` ao mesmo tempo. Se o gateway responder `404`, confirme que `ocelot.json` está na raiz do projeto `OcelotGateway` e que o caminho requisitado coincide com `UpstreamPathTemplate`. Se a restauração de pacotes falhar por rede, repita `dotnet add OcelotGateway package Ocelot` com a conexão disponível.

**Observe**

O gateway não tem lógica de negócio: as rotas são dados, não código. Versionar `ocelot.json` documenta a topologia da borda da mesma forma que `openapi.yaml` documenta o contrato de cada serviço.

**Compare**

A restrição REST de sistema em camadas aparece aqui na prática: o consumidor não sabe se fala com o serviço final ou com um intermediário. Na trilha essencial, o contrato OpenAPI protege a fronteira de um serviço; o gateway organiza a fronteira do conjunto. Ao terminar, encerre os três processos com `Ctrl+C` em cada terminal.

## Resultado esperado

Ao final, você terá observado `202`, `Location`, recuperação por `GET`, erro `422`, lint aprovado, lint deliberadamente reprovado e seis testes aprovados. Mais importante: conseguirá dizer qual ferramenta examina documento, implementação ou experiência do consumidor. Quem fez a extensão terá visto ainda um gateway de API roteando duas APIs por configuração declarativa.

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

Entregue `spectral-valido.txt`, `testes-contrato.txt`, a coleção Bruno importada, respostas de `POST`, `GET` e `422`, e uma nota curta comparando contrato explícito, contrato gerado e execução. Inclua a falha deliberada sem apresentá-la como defeito pendente. Se fizer a extensão do Ocelot, acrescente a saída das duas consultas feitas pelo gateway e o `ocelot.json` usado.

## Questões exploratórias

1. O que `202` permite ao provedor mudar sem quebrar o consumidor?
2. Por que `Location` é melhor que pedir ao consumidor para montar uma URL por convenção?
3. Qual divergência entre OpenAPI e aplicação os testes atuais ainda não detectam?
4. Quando uma chave de idempotência passaria a ser necessária?
5. Que parte do experimento deixaria de funcionar com duas instâncias e memória separada?
