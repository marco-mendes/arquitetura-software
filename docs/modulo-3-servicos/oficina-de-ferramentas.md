# Oficina de ferramentas: dois serviços, dois bancos e uma falha parcial

Nesta oficina você sobe quatro contêineres, confirma a propriedade dos dados, chama o fluxo nominal, interrompe uma dependência e guarda evidências. Os dados são sintéticos. As senhas do Compose valem somente para a rede local descartável e não devem ser reaproveitadas.

## Ferramenta

| Ferramenta | Uso na oficina | Verificação |
| --- | --- | --- |
| Docker Engine | executar contêineres e redes | `docker version` |
| Docker Compose v2 | coordenar processos e health checks | `docker compose version` |
| Python 3.11 ou superior | executar testes de contrato | `python --version` |
| FastAPI e httpx | oferecer e consumir HTTP | respostas em 8001 e 8002 |
| PostgreSQL 16 | persistir estados com propriedade separada | dois bancos saudáveis |

O Docker Compose fornece reprodução local, mas não representa orquestração de produção. O health check informa prontidão limitada ao processo e seu banco; não prova toda capacidade ponta a ponta.

## Pré-requisitos

**Objetivo**

Confirmar as ferramentas antes de criar qualquer recurso e trabalhar apenas na pasta do laboratório.

**Pré-requisito**

Tenha o repositório disponível, Python 3.11 ou superior e Docker com Compose v2. Reserve as portas `8001` e `8002`. Os comandos assumem que o terminal começa na raiz do repositório.

**Execute**

Confira as versões:

```text
Docker 24 ou superior
Docker Compose 2 ou superior
Python 3.11 ou superior
```

**Observe**

`docker version` possui seções Client e Server quando o daemon responde. Se aparecer apenas informação do cliente seguida de erro de conexão, a ferramenta está instalada, mas o ambiente de contêineres ainda não está pronto.

**Compare**

A validação `docker compose ... config --quiet` analisa o documento sem iniciar contêineres. O comando `up --wait` comprova execução e saúde. São evidências diferentes.

**Questões exploratórias**

- Qual evidência demonstra sintaxe válida sem demonstrar serviço ativo?
- Por que um health check local não garante o fluxo entre serviços?

## Instalação

### Windows

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/windows-install/) e Python pelas [instruções oficiais](https://docs.python.org/3/using/windows.html). Reinicie o terminal depois da instalação. Em PowerShell:

```powershell
docker version
docker compose version
py --version
cd laboratorios\plataforma-hospitalar
py -m pip install -e ".[dev]"
New-Item -ItemType Directory -Force evidencias\modulo-3
```

**Resultado esperado**

O servidor Docker responde, Compose informa versão 2, Python informa 3.11 ou superior e a instalação termina sem erro. A pasta `evidencias\modulo-3` existe dentro do laboratório.

**Contingência**

Se o servidor Docker não responder, abra Docker Desktop e aguarde a indicação de execução. Se a virtualização exigida estiver desabilitada, siga o diagnóstico oficial da instalação. Não altere arquivos do sistema para contornar essa condição. Ainda é possível executar a validação estática do Compose; registre que não houve evidência de contêineres ativos.

### macOS

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/mac-install/) e Python por [Homebrew](https://brew.sh/) ou pelo instalador oficial. No terminal:

```bash
docker version
docker compose version
python3 --version
cd laboratorios/plataforma-hospitalar
python3 -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-3
```

**Resultado esperado**

Client e Server aparecem, Compose informa versão 2 e Python informa 3.11 ou superior. A instalação editável permite importar `hospital`.

**Contingência**

Se o daemon não responder, abra Docker Desktop e aguarde. Em Mac com Apple Silicon, a imagem usada possui variante compatível; não force uma plataforma diferente. Se `python3 -m pip` recusar instalação global, crie `.venv` com `python3 -m venv .venv`, ative-a e repita.

### Linux

Instale Docker Engine e o plugin Compose pelas [instruções oficiais para Linux](https://docs.docker.com/engine/install/). Instale Python 3 com o gerenciador da distribuição. Depois:

```bash
docker version
docker compose version
python3 --version
cd laboratorios/plataforma-hospitalar
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-3
```

**Resultado esperado**

As versões são exibidas e o pacote é instalado no ambiente `.venv`.

**Contingência**

Se houver erro de permissão no socket Docker, use o procedimento pós-instalação oficial ou execute os comandos Docker com o mecanismo previsto pela sua distribuição. Não mude permissões do socket de forma ampla. Se o serviço estiver parado, inicie-o pelo gerenciador do sistema e repita `docker version`.

## Preparação do laboratório

### Essencial em aula

**Execute**

Dentro de `laboratorios/plataforma-hospitalar`, valide o arquivo antes de subir o ambiente:

```bash
docker compose -f infra/compose.servicos.yml config --quiet
```

No PowerShell, o comando é igual. Em seguida, leia os nomes dos serviços:

```bash
docker compose -f infra/compose.servicos.yml config --services
```

**Resultado esperado**

O primeiro comando não imprime conteúdo e termina com código zero. O segundo lista `db_elegibilidade`, `db_exames`, `elegibilidade` e `exames`.

**Observe**

Cada aplicação recebe somente sua `DATABASE_URL`. Exames também recebe `ELIGIBILIDADE_URL`, que aponta para o contrato HTTP. Os bancos não publicam portas na máquina. As credenciais legíveis são didáticas e limitadas ao ambiente local.

**Compare**

Dois schemas no mesmo servidor poderiam garantir propriedade com permissões. Dois contêineres tornam a demonstração física mais clara, ao custo de mais recursos.

**Questões exploratórias**

- Qual variável demonstra dependência autorizada de Exames?
- Qual configuração impediria o acesso direto mesmo sem o teste textual?

### Exploração em dupla

**Execute**

Uma pessoa identifica as garantias do Compose. A outra identifica o que somente os testes provam. Reúnam as listas e classifiquem configuração, comportamento e intenção.

**Observe**

Configuração pode declarar isolamento; a execução confirma que os componentes iniciam; o teste de fronteira detecta uma regressão de código. Nenhuma evidência isolada cobre tudo.

**Compare**

Relacione cada evidência a uma afirmação arquitetural específica.

**Questões exploratórias**

- Uma aplicação saudável pode ter uma operação indisponível?
- Um teste com transporte simulado elimina a necessidade de teste integrado?

### Extensão

**Execute**

Leia `infra/postgres/init.sql` e explique como `current_database()` escolhe o schema criado. Não altere o arquivo durante a execução principal.

**Observe**

O mesmo arquivo é incorporado nas duas imagens PostgreSQL didáticas, mas cada execução cria apenas a estrutura de seu proprietário.

**Compare**

Compare script de inicialização descartável com migrações versionadas necessárias em produção.

**Questões exploratórias**

- Como uma migração com rollback mudaria o processo?
- Que alerta detectaria falha repetida de inicialização?

## Execução

### Essencial em aula

**Execute**

Suba e aguarde os health checks:

```bash
docker compose -f infra/compose.servicos.yml up -d --build --wait
docker compose ps
```

**Resultado esperado**

O `up` termina com quatro serviços iniciados. `docker compose ps` mostra `db_elegibilidade`, `db_exames`, `elegibilidade` e `exames` como `healthy`. As aplicações publicam `0.0.0.0:8001->8000` e `0.0.0.0:8002->8000`.

**Contingência**

Se o build falhar por indisponibilidade de rede ao baixar imagens ou dependências, preserve o log e repita quando a conexão estiver estável. Se uma porta estiver ocupada, encerre apenas o processo local conhecido ou altere temporariamente o mapeamento e registre a nova URL. Não remova processos desconhecidos.

Consulte saúde. Em macOS ou Linux:

```bash
curl -i http://localhost:8001/health
curl -i http://localhost:8002/health
```

No PowerShell:

```powershell
curl.exe -i http://localhost:8001/health
curl.exe -i http://localhost:8002/health
```

**Resultado esperado**

Ambas respondem `HTTP/1.1 200 OK`. Os corpos são `{"status":"ok","servico":"elegibilidade"}` e `{"status":"ok","servico":"exames"}`.

Solicite um exame. Em macOS ou Linux:

```bash
curl -i -X POST http://localhost:8002/exames \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

No PowerShell:

```powershell
curl.exe -i -X POST http://localhost:8002/exames `
  -H "Content-Type: application/json" `
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

**Resultado esperado**

A resposta é `201 Created`, `solicitacao_id` é `1`, o beneficiário e o exame são repetidos e `situacao` é `solicitado`.

Interrompa somente Elegibilidade:

```bash
docker compose -f infra/compose.servicos.yml stop elegibilidade
docker compose -f infra/compose.servicos.yml ps
```

Repita o mesmo `POST /exames`.

**Resultado esperado**

Exames continua em execução, mas a operação responde `503 Service Unavailable` com `{"detail":{"codigo":"dependencia_indisponivel"}}`. Essa é a falha parcial observável.

**Observe**

O banco de Exames e seu processo não caíram. A capacidade não conclui porque depende de uma decisão remota. O timeout limita a espera e o código preserva a causa sem revelar detalhes internos.

**Compare**

Compare esse resultado com um processo único. A chamada local evitaria indisponibilidade de rede, mas também não ofereceria isolamento de implantação.

**Questões exploratórias**

- Por que não assumir `elegivel: true` como fallback?
- Que métrica diferenciaria erro do consumidor de falha da dependência?

Reinicie a dependência e aguarde:

```bash
docker compose -f infra/compose.servicos.yml start elegibilidade
docker compose -f infra/compose.servicos.yml wait elegibilidade || docker compose -f infra/compose.servicos.yml up -d --wait
```

Se sua versão de Compose interpretar `wait` como espera pelo encerramento, use diretamente o segundo comando. Confirme novamente os dois `/health` antes de continuar.

Execute o contrato de fronteira:

```bash
python -m pytest tests/test_service_boundaries.py -q
```

No Windows, se não ativou ambiente:

```powershell
py -m pytest tests/test_service_boundaries.py -q
```

**Resultado esperado**

O pytest informa `3 passed`. Um teste consome o contrato HTTP sem importar internals de Elegibilidade, outro observa `503` e o terceiro proíbe acesso direto à tabela alheia.

## Resultado esperado

Ao final da execução nominal, há evidência de quatro componentes saudáveis, duas respostas de saúde, um `201`, um `503` deliberado e três testes aprovados. Resultados diferentes devem ser registrados com comando, horário e saída; não substitua evidência ausente por uma descrição presumida.

## Interpretação

O experimento separa três afirmações. **Coesão:** cada serviço implementa uma capacidade pequena. **Propriedade:** cada processo recebe somente seu banco. **Acoplamento:** Exames ainda depende temporalmente de Elegibilidade. O `503` não é um defeito do laboratório; é o custo visível da decisão síncrona.

SAGA não resolveria indisponibilidade de uma consulta necessária antes da escrita. CQRS não faria a rede desaparecer. Um cache de elegibilidade poderia aumentar disponibilidade, mas introduziria defasagem e exigiria uma regra clínica explícita para validade.

## Limpeza e contingência

**Execute**

Remova contêineres, rede e volumes didáticos:

```bash
docker compose -f infra/compose.servicos.yml down -v
docker compose -f infra/compose.servicos.yml ps -a
```

**Resultado esperado**

O primeiro comando informa remoção dos quatro contêineres, da rede e dos volumes. O segundo não lista contêineres do projeto. Os arquivos em `evidencias/modulo-3` permanecem.

**Contingência**

Se o daemon esteve indisponível desde o início, execute apenas `docker compose -f infra/compose.servicos.yml config --quiet` e os testes Python. Registre literalmente “Compose validado estaticamente; execução de contêineres não realizada porque o daemon não respondeu”, junto do erro de `docker version`. Quando o daemon voltar, repita `up`, chamadas e `down -v`. Não declare health checks observados sem execução.

Se a oficina for interrompida depois do `up`, retorne à pasta do laboratório e execute `down -v`. Esse comando usa apenas recursos do projeto descrito no arquivo; não use limpeza global do Docker.

## Evidência a entregar

Organize em `evidencias/modulo-3`:

- `versoes.txt` com versões e resposta do servidor Docker;
- `compose-ps.txt` com quatro estados saudáveis;
- `health-elegibilidade.txt` e `health-exames.txt`;
- `exame-criado.txt` com `201`;
- `falha-parcial.txt` com `503`;
- `testes-fronteira.txt` com `3 passed`;
- `limpeza.txt` com remoção ou a contingência precisa.

### Exploração em dupla

Produzam um parágrafo relacionando cada arquivo a coesão, acoplamento, propriedade ou falha parcial. Identifiquem uma afirmação que a oficina não prova.

### Extensão

Proponha um novo teste que rejeite corpo incompatível do provedor e compare `502 contrato_invalido` com `503 dependencia_indisponivel`. Não implemente SAGA ou CQRS; registre apenas quando seriam justificáveis.
