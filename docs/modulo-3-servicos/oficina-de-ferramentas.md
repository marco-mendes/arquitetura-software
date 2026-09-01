# Oficina de ferramentas: dois serviços, dois bancos e uma falha parcial

Esta oficina coloca no ar dois serviços separados, cada um com seu próprio banco de dados, e provoca de propósito a situação que define arquitetura distribuída: **um serviço cai e o outro continua funcionando pela metade**. Não é um exercício de Docker. É a chance de ver, em execução, três decisões que o livro-texto discute em teoria: propriedade de dados, fronteira física e falha parcial.

O caso é o mesmo das páginas anteriores. **Elegibilidade** decide se um beneficiário pode usar o plano. **Exames** registra uma solicitação clínica, e para isso precisa consultar a decisão de Elegibilidade. São duas capacidades de negócio distintas, com dados e ciclos de mudança próprios, e é por isso que servem para demonstrar uma fronteira.

### O que você vai observar, e por que importa

| O que a oficina mostra | O conceito do módulo |
| --- | --- |
| Cada serviço só alcança o próprio banco, por construção da rede | [Propriedade dos dados](conceitos.md#propriedade-dos-dados) e banco por serviço |
| Exames responde `200` na verificação de saúde e `503` na operação | [Falha parcial](conceitos.md#chamadas-sincronas-e-falhas-parciais): o sistema não cai inteiro, degrada em partes |
| A chamada entre serviços tem prazo de espera e traduz o erro do vizinho | O custo da [fronteira física](conceitos.md#fronteira-logica-e-fronteira-fisica), que a chamada local não tinha |

### Onde cada arquivo mora

Todos os comandos rodam a partir de `laboratorios/plataforma-hospitalar`.

```text
plataforma-hospitalar/
├── infra/
│   └── compose.servicos.yml        ← define os quatro contêineres e as redes
├── src/hospital/servicos/
│   ├── elegibilidade.py            o serviço que decide
│   └── exames.py                   o serviço que depende do primeiro
└── evidencias/modulo-3/            você criará esta pasta na preparação
```

| Arquivo | O que ele faz |
| --- | --- |
| [`infra/compose.servicos.yml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/compose.servicos.yml) | Descreve os quatro contêineres, as três redes e as verificações de saúde. É onde a fronteira entre os serviços fica declarada. |
| [`src/hospital/servicos/elegibilidade.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/src/hospital/servicos/elegibilidade.py) | O serviço que responde se um beneficiário é elegível, consultando apenas a própria base. |
| [`src/hospital/servicos/exames.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/src/hospital/servicos/exames.py) | O serviço que chama Elegibilidade por HTTP e grava na própria base. É aqui que o tratamento de falha parcial está escrito. |

As senhas do laboratório valem só para esta demonstração local e os dados são inventados. Ao final, `down -v` remove contêineres, redes e volumes.

## Ferramenta

| Ferramenta | O que é | Para que serve aqui |
| --- | --- | --- |
| **Docker Engine** | O programa que executa contêineres, que são processos isolados com seu próprio sistema de arquivos e sua própria rede. | Rodar quatro processos isolados na sua máquina como se fossem quatro servidores. |
| **Docker Compose** | Um utilitário que sobe vários contêineres de uma vez, a partir de um arquivo YAML que descreve o conjunto. | Declarar os dois serviços, os dois bancos e as redes entre eles num arquivo só. |
| **PostgreSQL 16** | Um banco de dados relacional. | Dar a cada serviço um armazenamento próprio e separado. |
| **FastAPI e Uvicorn** | A biblioteca que implementa as rotas e o servidor que as atende, já usados no Módulo 2. | Servir as duas APIs. |
| **httpx** | Uma biblioteca Python para fazer chamadas HTTP. | É por ela que Exames chama Elegibilidade, com prazo de espera configurado. |

Dois termos se repetem ao longo da oficina e vale fixá-los agora. Um **contêiner** é um processo empacotado com tudo de que precisa para rodar, isolado do resto da máquina. Uma **verificação de saúde** (*health check*) é um comando que o Docker executa periodicamente para decidir se aquele contêiner está saudável. A distinção entre "no ar" e "saudável" será o assunto do momento mais importante desta oficina.

**Objetivo**

Observar uma fronteira de dados e uma falha parcial em uma demonstração local.

**Pré-requisito**

Docker em execução e Python 3.11 ou superior.

## Pré-requisitos

Verifique `docker version`, `docker compose version` e `python --version` antes de continuar.

## Instalação

### Windows

Instale Docker Desktop e Python; use `py` quando `python` não estiver no PATH.

### macOS

Instale Docker Desktop e Python 3 pelo instalador oficial ou gerenciador de pacotes.

### Linux

Instale Docker Engine, o plugin Compose e Python 3 pelo método da sua distribuição.

## Preparação do laboratório

Na raiz do clone, entre na pasta do laboratório e prepare um local para evidências. Em Windows use `py` no lugar de `python`, se necessário.

```bash
cd laboratorios/plataforma-hospitalar
python -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-3
```

No PowerShell, o equivalente para o diretório é `New-Item -ItemType Directory -Force evidencias\modulo-3`.

## A fronteira declarada no Compose

Antes de subir qualquer coisa, vale ler o arquivo que define a topologia, porque **a fronteira entre os dois serviços está escrita ali**, e não no código Python.

Comece pelo bloco de redes, no fim do arquivo:

```yaml
networks:
  application-net:              # por onde os dois serviços conversam
  elegibilidade-db-net:
    internal: true              # sem saída para fora: só quem está nela se alcança
  exames-db-net:
    internal: true
```

São três redes, e não uma. Cada serviço é ligado a exatamente duas delas:

```yaml
  elegibilidade:
    networks:
      - application-net         # fala com o outro serviço
      - elegibilidade-db-net    # fala com o próprio banco

  exames:
    networks:
      - application-net
      - exames-db-net           # o banco de Exames, e nenhum outro
```

Repare no que isso produz. O serviço de Exames **não tem rota de rede** até `db_elegibilidade`: mesmo que alguém escrevesse no código uma consulta ao banco alheio, a conexão falharia por não haver caminho. A propriedade dos dados deixa de depender de disciplina da equipe e passa a ser uma propriedade da infraestrutura.

É essa a tese que o módulo defende ao dizer que banco por serviço é uma decisão de **autoridade**, e não de tecnologia. Os dois bancos aqui rodam o mesmo PostgreSQL, com a mesma versão. O que os separa é quem tem permissão de alcançá-los.

O bloco de dependências declara a ordem de inicialização:

```yaml
  exames:
    depends_on:
      db_exames:
        condition: service_healthy      # espera o banco ficar saudável
      elegibilidade:
        condition: service_healthy      # espera o outro serviço também
```

E cada serviço declara como provar que está saudável:

```yaml
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 2s        # verifica a cada 2 segundos
      timeout: 3s         # desiste se demorar mais que 3
      retries: 15         # marca como não saudável após 15 falhas
```

Guarde este detalhe, porque ele volta adiante: o comando de saúde chama `/health` do **próprio** serviço. Ele não verifica se as dependências estão de pé.

## Execução

O percurso tem quatro momentos: subir tudo e ver o estado nominal, criar uma solicitação que funciona, derrubar Elegibilidade e observar a falha parcial, e por fim recuperar.

**Execute**

Siga as etapas na ordem da tabela abaixo. Cada uma tem estado de entrada, evidência esperada e o que fazer se divergir.

**Observe**

Em cada etapa, olhe para duas coisas ao mesmo tempo: o que o `docker compose ps` diz sobre a saúde dos contêineres e o que a API responde a uma requisição real. O momento em que essas duas leituras discordam é o assunto da oficina.

**Compare**

Compare o estado nominal, com os quatro contêineres saudáveis, com o estado degradado, em que Exames continua saudável para o Docker mas não consegue concluir a operação que depende de Elegibilidade. A diferença entre "o processo está vivo" e "a capacidade está disponível" é o que distingue falha parcial de queda do sistema.

**Questões exploratórias**

Qual dependência permanece saudável e qual capacidade deixa de ser concluída?

### Roteiro de transição do ambiente

| Etapa | Estado de entrada | Ação e evidência esperada | Contingência |
| --- | --- | --- | --- |
| Validar configuração | Os quatro serviços estão parados. | Execute os dois comandos `config`; `--quiet` termina sem texto e `--services` lista `elegibilidade`, `exames`, `db_elegibilidade` e `db_exames`. | Se o Docker não responder, guarde a saída e faça só a validação estática. |
| Iniciar e inspecionar | Compose válido e serviços parados. | Suba a demonstração; `ps` mostra quatro serviços `healthy` e os dois `/health` retornam `200`. | Se uma porta estiver ocupada, escolha outras portas; não remova recursos fora deste projeto. |
| Demonstrar falha parcial | As duas aplicações e bases estão saudáveis. | Pare `elegibilidade`; Exames permanece saudável, mas `POST /exames` retorna `503 dependencia_indisponivel`. | Se o resultado divergir, guarde `ps` e logs antes de reiniciar. |
| Recuperar e verificar | Elegibilidade está parada e Exames continua saudável. | Execute `up -d --wait`; os dois `/health` voltam a `200`, então rode o teste de fronteiras. | Se o daemon não responder, execute somente os testes Python e registre a limitação. |
| Limpar | A demonstração pode estar em qualquer estado anterior. | `down -v` remove contêineres, redes e volumes; `ps -a` não lista recursos ativos. | Se houver resíduo, repita apenas esse `down -v`. |

### Escolher portas e validar a configuração

Defina portas livres para não disputar os padrões 8001 e 8002. Em shells POSIX:

```bash
export ELEGIBILIDADE_PORT=18001
export EXAMES_PORT=18002
```

No PowerShell:

```powershell
$env:ELEGIBILIDADE_PORT = 18001
$env:EXAMES_PORT = 18002
```

```bash
docker compose -f infra/compose.servicos.yml config --quiet
```

Resultado: nenhum texto e código zero significam que a configuração é sintaticamente válida. Essa validação não demonstra que Docker está em execução nem que os serviços estão saudáveis.

```bash
docker compose -f infra/compose.servicos.yml config --services
```

Confirme os quatro nomes apresentados. O comando ajuda a evitar iniciar um arquivo Compose diferente por engano.

## Iniciar e observar a demonstração

```bash
docker compose -f infra/compose.servicos.yml up -d --build --wait
```

## Resultado esperado

O `--wait` termina quando os quatro health checks ficam saudáveis. Se uma imagem não puder ser baixada ou uma porta estiver ocupada, guarde a saída e escolha outra porta; não remova recursos Docker fora deste projeto.

```bash
docker compose -f infra/compose.servicos.yml ps
```

A saída deve ser esta, com os quatro serviços saudáveis:

```text
SERVICE            STATUS                    PORTS
db_elegibilidade   Up 17 seconds (healthy)   5432/tcp
db_exames          Up 17 seconds (healthy)   5432/tcp
elegibilidade      Up 15 seconds (healthy)   0.0.0.0:18001->8000/tcp
exames             Up 12 seconds (healthy)   0.0.0.0:18002->8000/tcp
```

Duas leituras importam aqui. Os dois bancos mostram apenas `5432/tcp`, **sem** o prefixo `0.0.0.0:` — eles não têm porta publicada para a sua máquina, o que significa que você não consegue alcançá-los diretamente do seu terminal. Só quem está na rede interna deles chega lá. Já as aplicações mostram `0.0.0.0:18001->8000`, que se lê como "a porta 18001 da sua máquina encaminha para a porta 8000 dentro do contêiner".

Confirme a saúde a partir da sua máquina:

```bash
curl -i "http://localhost:${ELEGIBILIDADE_PORT}/health"
curl -i "http://localhost:${EXAMES_PORT}/health"
```

No PowerShell, `curl.exe` evita o alias `curl` para `Invoke-WebRequest`:

```powershell
curl.exe -i "http://localhost:$env:ELEGIBILIDADE_PORT/health"
curl.exe -i "http://localhost:$env:EXAMES_PORT/health"
```

Cada resposta deve ser `200`. Agora crie uma solicitação elegível:

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

PowerShell (201):

```powershell
curl.exe -i -X POST "http://localhost:$env:EXAMES_PORT/exames" `
  -H "Content-Type: application/json" `
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

A resposta completa:

```text
HTTP/1.1 201 Created
server: uvicorn
content-type: application/json

{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001","solicitacao_id":1,"situacao":"solicitado"}
```

O `201 Created` afirma que o recurso passou a existir, diferente do `202` do Módulo 2, que apenas aceitava o pedido para processar depois. Aqui a solicitação já está gravada quando a resposta chega.

Para produzir esse `201`, o serviço de Exames fez duas coisas nesta ordem: chamou Elegibilidade por HTTP e, só depois de receber a aprovação, gravou na própria base. O `solicitacao_id` vem dessa gravação e reinicia a contagem após `down -v`, porque o volume é removido junto.

## Interpretação

### Tornar a falha parcial observável

```bash
docker compose -f infra/compose.servicos.yml stop elegibilidade
```

```bash
docker compose -f infra/compose.servicos.yml ps
```

Repita a chamada abaixo. Ela deve retornar `503 Service Unavailable` e o código `dependencia_indisponivel`, enquanto `GET /health` de Exames ainda retorna `200`:

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

PowerShell (503):

```powershell
curl.exe -i -X POST "http://localhost:$env:EXAMES_PORT/exames" `
  -H "Content-Type: application/json" `
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

Esta é a saída que interessa:

```text
HTTP/1.1 503 Service Unavailable
server: uvicorn
content-type: application/json

{"detail":{"codigo":"dependencia_indisponivel"}}
```

E, ao mesmo tempo, a verificação de saúde do próprio Exames continua respondendo:

```text
HTTP/1.1 200 OK

{"status":"ok","servico":"exames"}
```

São duas respostas contraditórias do mesmo serviço, no mesmo instante, e é exatamente isso que caracteriza a falha parcial.

O serviço de Exames está saudável pela definição dele mesmo: o processo responde e a base própria está acessível. O que ele não consegue é concluir uma operação que depende de um vizinho. Numa arquitetura de serviços, "estar no ar" e "conseguir atender" deixam de ser a mesma coisa, e é por isso que monitorar apenas processos vivos dá uma falsa sensação de saúde.

Repare no que **não** aconteceu. O sistema não caiu inteiro: consultas a Elegibilidade que já tivessem sido feitas não foram desfeitas, a base de Exames continua íntegra, e qualquer operação de Exames que não dependa do vizinho seguiria funcionando. A falha ficou contida no caminho que atravessa a fronteira.

### Por que o erro é `503` e não `500`

Olhe como `exames.py` trata a chamada ao vizinho:

```python
try:
    response = cliente.get(f"/elegibilidades/{pedido.beneficiario_id}")
except httpx.HTTPError as error:                    # a rede falhou
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={"codigo": "dependencia_indisponivel"},
    ) from error
```

A escolha do `503` comunica algo específico: **o defeito é temporário e não é culpa de quem chamou**. Um `500` diria "quebrei por dentro"; um `400` culparia o consumidor por um pedido correto. O `503` diz "tente de novo mais tarde", que é a informação verdadeira e acionável.

O mesmo arquivo traduz cada falha possível do vizinho num significado próprio, e essa tabela é o cerne da aula:

| O que acontece com Elegibilidade | Exames responde | Por quê |
| --- | --- | --- |
| Não responde, ou a rede falha | `503 dependencia_indisponivel` | Problema transitório de infraestrutura. |
| Responde `5xx` | `503 dependencia_indisponivel` | O vizinho quebrou; para o consumidor de Exames é a mesma indisponibilidade. |
| Responde `404`, beneficiário desconhecido | `422 beneficiario_desconhecido` | O pedido é que está errado, então a culpa volta para quem chamou. |
| Responde algo fora do contrato esperado | `502 contrato_invalido` | Exames recebeu resposta ilegível de um serviço a montante. |
| Responde que o beneficiário não é elegível | `422 beneficiario_inelegivel` | Não é falha técnica: é uma decisão de negócio negativa. |

Duas lições de arquitetura de serviços estão embutidas nessa tabela.

A primeira: **Exames nunca repassa o código de status do vizinho**. Um `404` de Elegibilidade não vira `404` de Exames, porque significariam coisas diferentes — o recurso `/exames` existe; quem não existe é o beneficiário. Vazar o status do serviço interno acopla o consumidor à topologia interna do sistema.

A segunda: falha técnica e decisão de negócio recebem tratamentos distintos. Beneficiário inelegível não é erro; é a resposta correta a uma pergunta legítima, e por isso vira `422` com código próprio, e não `503`.

Repare também no prazo de espera declarado na criação do cliente HTTP:

```python
with httpx.Client(base_url=ELIGIBILIDADE_URL, timeout=2.0) as client:
```

Sem esse `timeout`, uma chamada a um serviço que não responde ficaria pendurada indefinidamente, prendendo o processo de Exames e transformando a indisponibilidade de um serviço na indisponibilidade dos dois. É o custo da fronteira física. Numa chamada dentro do mesmo processo, a espera indefinida pela rede simplesmente não é um cenário possível.

```bash
docker compose -f infra/compose.servicos.yml up -d --wait
```

## Verificar as fronteiras sem depender do Compose

Com os serviços saudáveis, execute:

```bash
python -m pytest tests/test_service_boundaries.py -q
```

Espere `4 passed`, incluindo `test_exames_makes_its_own_database_failure_observable`. Os testes verificam o contrato HTTP, a falha parcial, a falha da base própria e a ausência de SQL contra a tabela de Elegibilidade. Em Windows sem ambiente ativado, use `py -m pytest tests/test_service_boundaries.py -q`.

## Limpeza e contingência

### Limpar a demonstração

```bash
docker compose -f infra/compose.servicos.yml down -v
```

```bash
docker compose -f infra/compose.servicos.yml ps -a
```

## Evidência a entregar

Guarde em `laboratorios/plataforma-hospitalar/evidencias/modulo-3/` as saídas de versões, health checks, `201`, `503` e testes. Se o daemon nunca respondeu, faça somente `config --quiet` e os testes Python e registre: “Compose validado estaticamente; execução de contêineres não realizada porque o daemon não respondeu”. Não afirme que observou health checks sem uma execução real.
