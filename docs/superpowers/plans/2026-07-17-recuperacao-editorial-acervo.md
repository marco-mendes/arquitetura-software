# Recuperação editorial do acervo de Arquitetura de Software — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reintegrar os conceitos e diagramas relevantes do acervo original no site MkDocs como uma narrativa didática única, e tornar todos os exercícios claros, auto-contidos e coerentes com a Taxonomia de Bloom.

**Architecture:** O acervo da raiz é tratado como fonte editorial, nunca como conteúdo colado no site. Uma matriz interna rastreia cada documento fonte até uma página canônica e sua decisão editorial. O validador passa a garantir feedback expansível em Recordar/Compreender e roteiro auto-contido nas atividades avançadas; a recuperação de conteúdo ocorre módulo a módulo, respeitando o visual, a navegação e a progressão já existentes.

**Tech Stack:** Markdown, MkDocs Material, Mermaid, CSS existente, Python `unittest`, `scripts/validate_content.py`.

## Global Constraints

- Não exibir no site rótulos como “conteúdo recuperado”, “material legado”, “migração” ou uma matriz de fontes.
- Todo conceito do acervo deve ser integrado, consolidado ou descartado com justificativa editorial rastreável; cópia literal não é objetivo.
- Diagramas estruturais devem preferir Mermaid; figuras externas só permanecem com função didática, fonte verificável, legenda, texto alternativo e leitura textual.
- Recordar e Compreender usam um `<details>` individual por pergunta, com `<summary>Ver resposta</summary>`.
- Aplicar, Analisar, Avaliar e Criar devem declarar objetivo, situação, papel, artefato, preparação, execução, evidência esperada, entrega e critérios.
- Cada comando de oficina informa intenção, resultado observável e contingência; o aluno não deve inferir qual processo, arquivo ou serviço está em uso.
- Não publicar gabaritos de atividades avançadas; critérios orientam evidências e insuficiência.
- Preservar o caso integrador hospitalar, laboratórios locais/open source e suporte Windows/macOS/Linux.
- Preservar os caminhos Markdown legados existentes e seu corpo, exceto pela nota de transição já aprovada.

---

## File structure

| Caminho | Responsabilidade após a recuperação |
| --- | --- |
| `docs/superpowers/traceability/recuperacao-editorial.md` | Matriz interna: fonte, destino canônico, ação editorial, conceitos e decisão sobre cada figura. Excluída da publicação. |
| `tests/test_editorial_recovery.py` | Regressões para cobertura da matriz, feedback expansível, roteiro auto-contido e integração de estilos na Unidade 1. |
| `scripts/validate_content.py` | Validação de formato dos exercícios e de figuras/leituras textuais já usada no build. |
| `docs/assets/stylesheets/extra.css` | Aparência acessível e consistente dos blocos expansíveis, caso o tema não a forneça suficientemente. |
| `docs/modulo-*/conceitos.md` | Narrativa conceitual integrada e progressiva. |
| `docs/modulo-*/padroes-e-decisoes.md` | Comparações, forças, anti-padrões e critérios de escolha. |
| `docs/modulo-*/exemplo-arquitetural.md` | Aplicação do conceito ao caso hospitalar, com diagramas e leitura textual. |
| `docs/modulo-*/estudo-de-caso.md` | Estudos de caso reescritos ou ampliados como análise, não como anedota de fornecedor. |
| `docs/modulo-*/oficina-de-ferramentas.md` | Roteiro instrumental que apresenta previamente artefato, processo local e evidências. |
| `docs/modulo-*/exercicios.md` | Perguntas Bloom com respostas expansíveis e atividades avançadas auto-contidas. |

---

### Task 1: Criar a rastreabilidade editorial e seus testes

**Files:**
- Create: `docs/superpowers/traceability/recuperacao-editorial.md`
- Create: `tests/test_editorial_recovery.py`
- Modify: `tests/test_content_contract.py`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: todos os arquivos `^[1-5].*\.md` da raiz e os módulos públicos em `docs/modulo-*`.
- Produces: matriz interna com colunas `Arquivo-fonte`, `Destino canônico`, `Ação editorial`, `Conceitos integrados`, `Figura/diagrama`; testes reutilizados pelas tarefas 2–9.

- [ ] **Step 1: Escrever o teste vermelho de cobertura da matriz**

```python
class EditorialRecoveryTest(unittest.TestCase):
    def test_traceability_covers_every_numbered_legacy_markdown(self):
        traceability = (ROOT / "docs/superpowers/traceability/recuperacao-editorial.md").read_text(encoding="utf-8")
        sources = sorted(ROOT.glob("[1-5]*.md"))
        self.assertGreater(len(sources), 30)
        for source in sources:
            self.assertIn(f"`{source.name}`", traceability, source.name)
```

Run: `python -m unittest tests.test_editorial_recovery.EditorialRecoveryTest.test_traceability_covers_every_numbered_legacy_markdown -v`

Expected: FAIL porque a matriz ainda não existe.

- [ ] **Step 2: Criar a matriz interna completa**

Criar uma tabela para todos os arquivos numerados das famílias 1–5. Cada linha informa o destino público e uma das ações: `integrar`, `consolidar`, `substituir figura` ou `referenciar`. Para cada capítulo fonte, registrar conceitos concretos que entram no site. Para cada mídia ou Mermaid de valor didático, indicar `manter`, `recriar em Mermaid`, `adaptar` ou `não usar`, seguido de justificativa curta.

Incluir explicitamente, entre outros: mapa de estilos; camadas; pipes and filters; microkernel; tipos e plataforma de APIs; gateway; todos os capítulos 3.1–3.12; broker, mediator e comparação de mensageria; IaaS/PaaS/SaaS, contêineres, orquestração, iFood e Taco Bell.

- [ ] **Step 3: Excluir a matriz da publicação**

Adicionar `superpowers/**` a `exclude_docs` em `mkdocs.yml` caso a configuração atual não cubra todo o diretório. Manter planos e especificações fora da navegação e fora do build público.

- [ ] **Step 4: Testar cobertura e exclusão**

Run:

```bash
python -m unittest tests.test_editorial_recovery.EditorialRecoveryTest.test_traceability_covers_every_numbered_legacy_markdown -v
python -m unittest tests.test_content_contract.ContentContractTest.test_mkdocs_excludes_internal_planning_documents -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/traceability/recuperacao-editorial.md tests/test_editorial_recovery.py tests/test_content_contract.py mkdocs.yml
git commit -m "docs: map editorial recovery sources"
```

### Task 2: Estabelecer o contrato de exercícios auto-contidos

**Files:**
- Modify: `scripts/validate_content.py`
- Modify: `tests/test_content_contract.py`
- Modify: `tests/test_editorial_recovery.py`
- Modify: `docs/assets/stylesheets/extra.css`
- Modify: `docs/comecar/como-usar.md`

**Interfaces:**
- Consumes: seções `## Recordar`, `## Compreender`, `## Aplicar`, `## Analisar`, `## Avaliar` e `## Criar` em `exercicios.md`.
- Produces: validação que exige resposta expansível por pergunta inicial e os nove rótulos do roteiro para cada atividade avançada.

- [ ] **Step 1: Escrever testes vermelhos para o feedback expansível e o roteiro**

```python
def test_record_and_understand_questions_have_individual_expandable_feedback(self):
    text = "## Recordar\\n1. Defina conector.\\n<details>\\n<summary>Ver resposta</summary>\\nUm mecanismo de colaboração.\\n</details>"
    self.assertEqual([], expandable_feedback_errors(text, "exemplo.md"))

def test_advanced_exercise_declares_context_before_execution(self):
    text = """## Aplicar
**Objetivo**
**Situação**
**Seu papel**
**Artefato que você irá usar**
**Antes de executar**
**O que fazer**
**Evidência esperada**
**Entrega esperada**
**Critérios de avaliação**
"""
    self.assertEqual([], self_contained_activity_errors(text, "exemplo.md"))
```

Run: `python -m unittest tests.test_editorial_recovery -v`

Expected: FAIL porque `expandable_feedback_errors` e `self_contained_activity_errors` ainda não existem.

- [ ] **Step 2: Implementar parsing mínimo no validador, sem ativá-lo globalmente ainda**

Adicionar as constantes e funções abaixo a `scripts/validate_content.py`. Elas usam `bloom_sections()` e `_mask_fenced_code()` já existentes; nesta tarefa as funções são cobertas por testes de texto sintético, mas só são chamadas por `_validate_exercises()` na Task 9, quando os seis módulos já estiverem adaptados.

```python
_SELF_CONTAINED_LABELS = (
    "**Objetivo**", "**Situação**", "**Seu papel**",
    "**Artefato que você irá usar**", "**Antes de executar**",
    "**O que fazer**", "**Evidência esperada**",
    "**Entrega esperada**", "**Critérios de avaliação**",
)

def expandable_feedback_errors(text: str, location: str) -> list[str]:
    errors: list[str] = []
    for level in ("Recordar", "Compreender"):
        section = bloom_sections(text).get(level, "")
        items = re.split(r"(?m)(?=^\\d+\\.\\s)", section)
        for item in (item for item in items if re.match(r"^\\d+\\.\\s", item)):
            if not re.search(
                r"<details>\\s*<summary>Ver resposta</summary>.*?</details>",
                item,
                re.DOTALL,
            ):
                errors.append(f"{location}: {level}: pergunta sem resposta expansível")
    return errors

def self_contained_activity_errors(text: str, location: str) -> list[str]:
    errors: list[str] = []
    for level in ("Aplicar", "Analisar", "Avaliar", "Criar"):
        section = bloom_sections(text).get(level, "")
        if not section:
            continue
        previous = -1
        for label in _SELF_CONTAINED_LABELS:
            current = section.find(label, previous + 1)
            if current == -1:
                errors.append(f"{location}: {level}: marcador obrigatório ausente: {label}")
            elif current < previous:
                errors.append(f"{location}: {level}: marcador fora da ordem: {label}")
            previous = max(previous, current)
    return errors
```

Na Task 9, adicionar `errors.extend(expandable_feedback_errors(text, location))` e `errors.extend(self_contained_activity_errors(text, location))` ao final de `_validate_exercises()`.

- [ ] **Step 3: Padronizar a aparência de feedback expansível**

Em `extra.css`, estilizar `details` no conteúdo principal com borda, fundo claro, espaçamento e `summary:focus-visible` de alto contraste. Não esconder o indicador nativo nem depender exclusivamente de cor.

- [ ] **Step 4: Atualizar o guia de estudo**

Em `docs/comecar/como-usar.md`, explicar que respostas expansíveis são autocorreção após tentativa e que atividades avançadas apresentam todo o contexto, artefatos e evidências antes de pedir execução.

- [ ] **Step 5: Verificar as funções ainda não conectadas ao contrato público**

Run:

```bash
python -m unittest tests.test_editorial_recovery.EditorialRecoveryTest.test_expandable_feedback_parser -v
python -m unittest tests.test_editorial_recovery.EditorialRecoveryTest.test_self_contained_activity_parser -v
```

Expected: PASS. O build global continua verde porque o novo parsing ainda não foi conectado ao contrato público; a conexão obrigatória e a verificação global ocorrem na Task 9.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_content.py tests/test_content_contract.py tests/test_editorial_recovery.py docs/assets/stylesheets/extra.css docs/comecar/como-usar.md
git commit -m "feat: define self-contained exercise contract"
```

### Task 3: Recuperar a Unidade 1 — estilos como mapa e decisões

**Files:**
- Modify: `docs/modulo-1-visao-geral/index.md`
- Modify: `docs/modulo-1-visao-geral/conceitos.md`
- Modify: `docs/modulo-1-visao-geral/padroes-e-decisoes.md`
- Modify: `docs/modulo-1-visao-geral/exemplo-arquitetural.md`
- Modify: `docs/modulo-1-visao-geral/oficina-de-ferramentas.md`
- Modify: `docs/modulo-1-visao-geral/exercicios.md`
- Modify: `tests/test_module_one.py`
- Modify: `tests/test_editorial_recovery.py`

**Interfaces:**
- Consumes: `1.1 Mapa e Estilos de Backend.md`, `1.2 Estilo em Camadas.md`, `1.3 Pipes-filters.md`, `1.4 Micro-kernel.md`, `1.5 O Racional arquitetural e o conceito de ADRs.md` e exercícios relacionados.
- Produces: mapa inicial de estilos que prepara as unidades 2–6; quatro explicações aprofundadas e exercícios auto-contidos.

- [ ] **Step 1: Escrever testes vermelhos de cobertura de estilos e feedback**

```python
def test_unit_one_introduces_the_complete_style_map(self):
    text = read_module_page("modulo-1-visao-geral", "conceitos.md")
    for term in ("Camadas", "MVC", "Hexagonal", "Microkernel", "Pipes and Filters", "DDD", "microsserviços", "APIs", "eventos", "nuvem", "contêineres"):
        self.assertIn(term, text)

def test_unit_one_recall_and_understand_use_expandable_answers(self):
    text = read_module_page("modulo-1-visao-geral", "exercicios.md")
    self.assertGreaterEqual(text.count("<summary>Ver resposta</summary>"), 12)
```

Run: `python -m unittest tests.test_module_one tests.test_editorial_recovery -v`

Expected: FAIL para mapa incompleto e respostas agrupadas.

- [ ] **Step 2: Reescrever o mapa e a progressão conceitual**

Em `conceitos.md`, abrir com as quatro famílias do mapa original e um Mermaid que relacione família, força e unidade de aprofundamento. Inserir definições curtas para os onze estilos/conceitos do teste; separar explicitamente os quatro estilos aprofundados nesta unidade dos temas que reaparecem depois.

Em `padroes-e-decisoes.md`, expandir Camadas, Pipes and Filters, Microkernel e Monólito Modular com responsabilidade, conectores, forças, anti-padrões, quando usar e quando evitar. Incorporar Camadas abertas/fechadas, sumidouro, filtro com estado e core creep como riscos explicados no caso hospitalar.

- [ ] **Step 3: Recuperar diagramas e exemplos sem colagem**

Recriar em Mermaid: dependências de camadas, pipeline de transformação e núcleo/plugins. Em `exemplo-arquitetural.md`, conectar cada diagrama a triagem, agenda, faturamento e auditoria; para cada diagrama incluir texto alternativo, legenda e leitura textual adjacente.

- [ ] **Step 4: Reescrever oficina e exercícios**

Apresentar no topo da oficina o artefato `laboratorios/plataforma-hospitalar/src/hospital/estilos.py`, sua função e a condição inicial do ambiente. Transformar Recordar e Compreender em perguntas individuais com `<details>`. Nas atividades avançadas, incluir os nove rótulos do contrato; antes de `python -m pytest tests/test_estilos.py -q`, explicar que o teste executa o comparador de estilos do caso hospitalar e qual saída deve ser guardada.

- [ ] **Step 5: Verificar**

Run:

```bash
python -m unittest tests.test_module_one tests.test_editorial_recovery -v
python scripts/validate_content.py --module modulo-1-visao-geral
python -m mkdocs build --strict
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add docs/modulo-1-visao-geral tests/test_module_one.py tests/test_editorial_recovery.py
git commit -m "docs: recover architectural styles foundations"
```

### Task 4: Recuperar a Unidade 2 — APIs, protocolos e plataforma

**Files:**
- Modify: `docs/modulo-2-apis/index.md`
- Modify: `docs/modulo-2-apis/conceitos.md`
- Modify: `docs/modulo-2-apis/padroes-e-decisoes.md`
- Modify: `docs/modulo-2-apis/exemplo-arquitetural.md`
- Modify: `docs/modulo-2-apis/estudo-de-caso.md`
- Modify: `docs/modulo-2-apis/oficina-de-ferramentas.md`
- Modify: `docs/modulo-2-apis/exercicios.md`
- Modify: `tests/test_module_two.py`

**Interfaces:**
- Consumes: capítulos 2.1–2.9 e seus exercícios; API em `laboratorios/plataforma-hospitalar/src/hospital/api/main.py`; OpenAPI em `laboratorios/plataforma-hospitalar/contratos/openapi.yaml`.
- Produces: visão arquitetural de APIs, protocolos e gateway, e oficina explicada por artefato e evidência.

- [ ] **Step 1: Escrever testes vermelhos de cobertura e auto-contenção**

```python
def test_unit_two_compares_api_styles_and_protocols_architecturally(self):
    text = read_module_page("modulo-2-apis", "conceitos.md")
    for term in ("REST", "GraphQL", "gRPC", "WebSocket", "contrato", "consumidor"):
        self.assertIn(term, text)

def test_api_workshop_names_the_local_application_before_commands(self):
    text = read_module_page("modulo-2-apis", "oficina-de-ferramentas.md")
    self.assertIn("API de elegibilidades da plataforma hospitalar", text)
    self.assertIn("src/hospital/api/main.py", text)
    self.assertIn("http://127.0.0.1:8000", text)
```

Run: `python -m unittest tests.test_module_two -v`

Expected: FAIL antes da integração dos conceitos e do contexto do artefato.

- [ ] **Step 2: Integrar conceitos e decisões**

Reescrever `conceitos.md` e `padroes-e-decisoes.md` para cobrir estilo API, REST, GraphQL, gRPC, WebSocket, contrato, compatibilidade, descoberta, plataforma de APIs, gateway mínimo, roteamento, agregação e políticas. Comparar por necessidade do consumidor, sem apresentar protocolo ou produto como escolha padrão.

- [ ] **Step 3: Reescrever caso, exemplo e oficina**

Usar o caso de elegibilidade hospitalar para explicar consumidor, contrato, status, `Location`, validação e evolução. A oficina deve introduzir a API FastAPI, seus caminhos `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`, o armazenamento efêmero e o OpenAPI antes de comandos. Para cada trilha Windows/macOS/Linux, conservar preparação, resultado esperado e contingência.

- [ ] **Step 4: Reescrever exercícios**

Criar perguntas expansíveis de Recordar/Compreender e, nas atividades avançadas, apresentar a API, o contrato, o terminal necessário, o estado inicial e as evidências `202`, `422`, protocolo e `Location` antes da execução. Não usar frases como “você recebeu o laboratório” ou “rode isto” sem nome e caminho do artefato.

- [ ] **Step 5: Verificar e commit**

Run:

```bash
python -m unittest tests.test_module_two tests.test_editorial_recovery -v
python scripts/validate_content.py --module modulo-2-apis
python -m mkdocs build --strict
```

```bash
git add docs/modulo-2-apis tests/test_module_two.py tests/test_editorial_recovery.py
git commit -m "docs: recover API architecture foundations"
```

### Task 5: Recuperar a Unidade 3 — serviços e sistemas distribuídos

**Files:**
- Modify: `docs/modulo-3-servicos/index.md`
- Modify: `docs/modulo-3-servicos/conceitos.md`
- Modify: `docs/modulo-3-servicos/padroes-e-decisoes.md`
- Modify: `docs/modulo-3-servicos/exemplo-arquitetural.md`
- Modify: `docs/modulo-3-servicos/estudo-de-caso.md`
- Modify: `docs/modulo-3-servicos/oficina-de-ferramentas.md`
- Modify: `docs/modulo-3-servicos/exercicios.md`
- Modify: `tests/test_module_three.py`

**Interfaces:**
- Consumes: capítulos 3.1–3.12 e exercícios; Compose e serviços em `laboratorios/plataforma-hospitalar/infra/compose.servicos.yml`.
- Produces: explicação progressiva de fronteiras, dados, consistência e evolução de serviços.

- [ ] **Step 1: Escrever teste vermelho de repertório distribuído**

```python
def test_unit_three_covers_distributed_service_consequences(self):
    text = read_module_page("modulo-3-servicos", "conceitos.md") + read_module_page("modulo-3-servicos", "padroes-e-decisoes.md")
    for term in ("persistência", "consistência eventual", "CAP", "SAGA", "CQRS", "event sourcing", "estrangulador", "chassi"):
        self.assertIn(term, text)
```

Run: `python -m unittest tests.test_module_three -v`

Expected: FAIL para repertório ainda ausente.

- [ ] **Step 2: Integrar os conceitos sem virar catálogo**

Explicar limites de microsserviços, decomposição, dados por serviço, persistência poliglota, CAP, consistência eventual, SAGA, CQRS, event sourcing, chassi e estrangulador como respostas condicionais a forças. Usar Netflix e Uber como estudos de consequência, escala e reversibilidade; registrar limites de contexto e evitar copiar narrativas de fornecedor.

- [ ] **Step 3: Tornar oficina e exercícios auto-contidos**

Apresentar `compose.servicos.yml`, os serviços de elegibilidade e exames, as duas bases e os testes antes de qualquer `docker compose`. Explicar que o Compose inicia uma demonstração local descartável, qual porta/health check observar e como encerrar. Usar perguntas expansíveis nos níveis iniciais; nas demais atividades declarar a situação, artefatos, preparação e evidência de falha parcial.

- [ ] **Step 4: Verificar e commit**

Run:

```bash
python -m unittest tests.test_module_three tests.test_editorial_recovery -v
python scripts/validate_content.py --module modulo-3-servicos
docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml config --quiet
```

```bash
git add docs/modulo-3-servicos tests/test_module_three.py tests/test_editorial_recovery.py
git commit -m "docs: recover service architecture foundations"
```

### Task 6: Recuperar a Unidade 4 — governança de serviços

**Files:**
- Modify: `docs/modulo-4-governanca/index.md`
- Modify: `docs/modulo-4-governanca/conceitos.md`
- Modify: `docs/modulo-4-governanca/padroes-e-decisoes.md`
- Modify: `docs/modulo-4-governanca/exemplo-arquitetural.md`
- Modify: `docs/modulo-4-governanca/estudo-de-caso.md`
- Modify: `docs/modulo-4-governanca/oficina-de-ferramentas.md`
- Modify: `docs/modulo-4-governanca/exercicios.md`
- Modify: `tests/test_module_four.py`

**Interfaces:**
- Consumes: capítulos 2.4–2.7, 4.2 e 4.3 como fonte de políticas, gateway, broker e mediator; stack `compose.governanca.yml`.
- Produces: governança vinculada a contratos, políticas, fronteiras, rastreabilidade e operação.

- [ ] **Step 1: Escrever teste vermelho de conceitos de governança**

```python
def test_unit_four_explains_governance_as_contract_policy_and_evidence(self):
    text = read_module_page("modulo-4-governanca", "conceitos.md") + read_module_page("modulo-4-governanca", "padroes-e-decisoes.md")
    for term in ("política", "versionamento", "gateway", "mediação", "rastreabilidade"):
        self.assertIn(term, text)
```

Run: `python -m unittest tests.test_module_four -v`

Expected: FAIL antes da ampliação.

- [ ] **Step 2: Integrar conceitos, exemplo e oficina**

Ampliar a unidade para diferenciar governança por contrato, roteamento, política, versionamento, correlação, logs e traces. Apresentar Kong, OpenTelemetry e Jaeger como implementação local do caso, não como sinônimos da arquitetura. Nomear os arquivos `compose.governanca.yml`, `infra/kong/kong.yml` e `infra/observabilidade/otel-collector.yml` antes dos comandos e indicar sinais esperados: rota, `429`, `correlation_id` e trace.

- [ ] **Step 3: Reescrever exercícios e verificar**

Transformar Recordar/Compreender em detalhes individuais. Nas atividades avançadas, declarar qual política será observada, em qual arquivo ela existe, qual serviço a recebe e qual saída comprova o comportamento. Preservar critérios percentuais, evidência e insuficiência.

Run:

```bash
python -m unittest tests.test_module_four tests.test_editorial_recovery -v
python scripts/validate_content.py --module modulo-4-governanca
docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml config --quiet
```

- [ ] **Step 4: Commit**

```bash
git add docs/modulo-4-governanca tests/test_module_four.py tests/test_editorial_recovery.py
git commit -m "docs: recover service governance foundations"
```

### Task 7: Recuperar a Unidade 5 — eventos, topologias e processamento

**Files:**
- Modify: `docs/modulo-5-eventos/index.md`
- Modify: `docs/modulo-5-eventos/conceitos.md`
- Modify: `docs/modulo-5-eventos/padroes-e-decisoes.md`
- Modify: `docs/modulo-5-eventos/exemplo-arquitetural.md`
- Modify: `docs/modulo-5-eventos/estudo-de-caso.md`
- Modify: `docs/modulo-5-eventos/oficina-de-ferramentas.md`
- Modify: `docs/modulo-5-eventos/exercicios.md`
- Modify: `tests/test_module_five.py`

**Interfaces:**
- Consumes: capítulos 4.1–4.4, comparação Kafka/ActiveMQ/RabbitMQ e `compose.eventos.yml`.
- Produces: EDA explicada por contratos, topologia, falhas e operação.

- [ ] **Step 1: Escrever teste vermelho de arquitetura orientada a eventos**

```python
def test_unit_five_covers_event_architecture_beyond_broker_terms(self):
    text = read_module_page("modulo-5-eventos", "conceitos.md") + read_module_page("modulo-5-eventos", "padroes-e-decisoes.md")
    for term in ("produtor", "consumidor", "broker", "mediator", "topologia", "payload", "idempotência", "DLQ"):
        self.assertIn(term, text)
```

Run: `python -m unittest tests.test_module_five -v`

Expected: FAIL se a unidade apenas citar o fluxo atual.

- [ ] **Step 2: Integrar conceitos e diagramas**

Cobrir eventos, produtores, consumidores, broker, mediator, topologias, payload, processamento, ordem, duplicidade, DLQ, observabilidade, limitações e custo operacional. Usar Kafka, ActiveMQ e RabbitMQ como comparação de necessidades, não ranking absoluto. Recriar os fluxos estruturais em Mermaid com leitura textual.

- [ ] **Step 3: Tornar oficina e exercícios auto-contidos**

Antes de iniciar RabbitMQ ou consumidor, explicar exchange, fila, consumidor de faturamento, armazenamento de idempotência e DLQ, com caminhos de arquivo. Cada experimento nomeia a variável alterada, o evento publicado, a evidência de processamento e o comportamento de erro esperado.

- [ ] **Step 4: Verificar e commit**

Run:

```bash
python -m unittest tests.test_module_five tests.test_editorial_recovery -v
python scripts/validate_content.py --module modulo-5-eventos
docker compose -f laboratorios/plataforma-hospitalar/infra/compose.eventos.yml config --quiet
```

```bash
git add docs/modulo-5-eventos tests/test_module_five.py tests/test_editorial_recovery.py
git commit -m "docs: recover event architecture foundations"
```

### Task 8: Recuperar a Unidade 6 — nuvem, serviços e operação

**Files:**
- Modify: `docs/modulo-6-nuvem/index.md`
- Modify: `docs/modulo-6-nuvem/conceitos.md`
- Modify: `docs/modulo-6-nuvem/padroes-e-decisoes.md`
- Modify: `docs/modulo-6-nuvem/exemplo-arquitetural.md`
- Modify: `docs/modulo-6-nuvem/estudo-de-caso.md`
- Modify: `docs/modulo-6-nuvem/oficina-de-ferramentas.md`
- Modify: `docs/modulo-6-nuvem/exercicios.md`
- Modify: `tests/test_module_six.py`

**Interfaces:**
- Consumes: capítulos 5.1–5.6, manifestos em `laboratorios/plataforma-hospitalar/infra/k8s/` e cluster kind em `infra/kind/cluster.yaml`.
- Produces: fundamentos de serviço em nuvem, contêiner e orquestração conectados à resiliência do caso hospitalar.

- [ ] **Step 1: Escrever teste vermelho de modelos e operação em nuvem**

```python
def test_unit_six_distinguishes_service_models_and_runtime_mechanisms(self):
    text = read_module_page("modulo-6-nuvem", "conceitos.md") + read_module_page("modulo-6-nuvem", "padroes-e-decisoes.md")
    for term in ("IaaS", "PaaS", "SaaS", "on-premise", "contêiner", "orquestração", "readiness", "liveness"):
        self.assertIn(term, text)
```

Run: `python -m unittest tests.test_module_six -v`

Expected: FAIL para distinções ausentes.

- [ ] **Step 2: Integrar conceitos e estudos de caso**

Explicar IaaS/PaaS/SaaS, on-premise, serviços gerenciados, contêineres, imagens, orquestração, escalabilidade, configuração e rollback. Usar AWS, iFood e Taco Bell como contextos de decisão e limites; separar claramente exemplo de fornecedor, modelo de serviço e princípio arquitetural.

- [ ] **Step 3: Reescrever oficina e exercícios**

Apresentar antes dos comandos o Dockerfile, a imagem `hospital-api:1.0.0`, o arquivo kind, os manifestos de namespace/ConfigMap/Deployment/Service/HPA e o que cada probe demonstra. A oficina informa que `kind` cria um cluster Kubernetes local descartável e que nenhum comando deve ser usado contra um cluster compartilhado. Exercícios iniciais usam detalhes expansíveis; os demais declaram artefatos, preparação, execução, sinais de rollout e rollback.

- [ ] **Step 4: Verificar e commit**

Run:

```bash
python -m unittest tests.test_module_six tests.test_editorial_recovery -v
python scripts/validate_content.py --module modulo-6-nuvem
python -m pytest laboratorios/plataforma-hospitalar/tests/test_k8s_manifests.py -q
```

```bash
git add docs/modulo-6-nuvem tests/test_module_six.py tests/test_editorial_recovery.py
git commit -m "docs: recover cloud architecture foundations"
```

### Task 9: Fechar contrato em todos os exercícios e revisar figuras

**Files:**
- Modify: `docs/modulo-{1-visao-geral,2-apis,3-servicos,4-governanca,5-eventos,6-nuvem}/exercicios.md`
- Modify: `docs/modulo-{1-visao-geral,2-apis,3-servicos,4-governanca,5-eventos,6-nuvem}/oficina-de-ferramentas.md`
- Modify as needed: `docs/assets/images/*`, `docs/assets/images/prompts.md`
- Modify: `tests/test_editorial_recovery.py`

**Interfaces:**
- Consumes: contrato da Task 2 e conceitos recuperados nas Tasks 3–8.
- Produces: seis módulos com exercícios formatados de modo uniforme e figuras acessíveis.

- [ ] **Step 1: Escrever teste vermelho transversal**

```python
def test_every_module_exercise_page_uses_expandable_feedback_and_self_contained_labels(self):
    for slug in MODULE_SLUGS:
        text = read_module_page(slug, "exercicios.md")
        self.assertGreaterEqual(text.count("<summary>Ver resposta</summary>"), 6, slug)
        for label in ADVANCED_LABELS:
            self.assertIn(f"**{label}**", text, slug)
```

Run: `python -m unittest tests.test_editorial_recovery.EditorialRecoveryTest.test_every_module_exercise_page_uses_expandable_feedback_and_self_contained_labels -v`

Expected: FAIL até os seis módulos atenderem ao padrão.

- [ ] **Step 2: Revisar todos os exercícios e oficinas como aluno iniciante**

Para cada instrução operacional, verificar explicitamente: qual é o artefato, onde ele está, por que será usado, em qual estado precisa estar, qual comando/manipulação ocorre, qual saída procurar e que ação tomar em caso de desvio. Substituir referências vagas como “laboratório”, “API”, “acrescente”, “compare” e “rode isto” por nomes próprios, caminhos, objetos de domínio e resultado verificável.

- [ ] **Step 3: Revisar cada figura da matriz**

Aplicar a decisão registrada na Task 1. Para cada figura pública mantida ou criada, confirmar texto alternativo, legenda, leitura textual, largura responsiva e fonte. Não manter uma imagem antiga apenas por estar no acervo.

- [ ] **Step 4: Verificar e commit**

Run:

```bash
python -m unittest tests.test_editorial_recovery tests.test_content_contract -v
python scripts/validate_content.py --all
python -m mkdocs build --strict
```

```bash
git add docs tests scripts
git commit -m "docs: complete self-contained learning activities"
```

### Task 10: Auditoria editorial, técnica e visual

**Files:**
- Modify as needed: arquivos identificados pelos testes e pela revisão visual.
- Modify: `docs/sobre/qualidade-do-material.md`

**Interfaces:**
- Consumes: todos os módulos, matriz interna, imagens e laboratórios.
- Produces: site pronto para publicação, com documento de qualidade atualizado.

- [ ] **Step 1: Executar a barreira completa**

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_content.py --all
python -m mkdocs build --strict
python -m pytest laboratorios/plataforma-hospitalar/tests -q
docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml config --quiet
docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml config --quiet
docker compose -f laboratorios/plataforma-hospitalar/infra/compose.eventos.yml config --quiet
git diff --check
```

Expected: todos os testes passam; build estrito termina com código 0; os Compose são válidos; não há whitespace inválido.

- [ ] **Step 2: Revisar páginas representativas em desktop e móvel**

Usar `mkdocs serve` e revisar: mapa de estilos e diagrama de camadas da Unidade 1; oficina e exercício da Unidade 2; conceitos de serviços; oficina de governança; diagrama e oficina de eventos; oficina de nuvem; projeto integrador. Confirmar que `details` expande, foco de teclado é visível, Mermaid renderiza, figuras têm leitura útil e tabelas permanecem legíveis em largura móvel.

- [ ] **Step 3: Atualizar política de qualidade**

Em `docs/sobre/qualidade-do-material.md`, acrescentar que a revisão editorial cobre rastreabilidade de fontes, resposta expansível para níveis iniciais, contexto completo para atividades avançadas e acessibilidade de figuras.

- [ ] **Step 4: Commit**

```bash
git add docs tests scripts mkdocs.yml laboratorios .github requirements.txt
git commit -m "docs: finalize editorial course recovery"
```

---

## Self-review

- A recuperação de conceitos e exemplos de cada unidade é coberta pelas Tasks 3–8.
- A rastreabilidade de todos os capítulos numerados é coberta pela Task 1 e não aparece ao aluno.
- O padrão de perguntas expansíveis e atividades auto-contidas é definido e validado na Task 2, aplicado nas Tasks 3–9 e auditado na Task 10.
- Figuras são tratadas como conteúdo acessível nas Tasks 1, 3–8 e 9.
- Nenhuma tarefa pede cópia literal de documentos, gabarito avançado ou publicação de material interno.
- A barreira final combina testes, conteúdo, build, laboratórios, Compose e revisão visual.
