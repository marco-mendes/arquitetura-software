# Site da Disciplina de Arquitetura de Software — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir e publicar um site MkDocs completo para seis encontros de Arquitetura de Software, preservando o acervo legado e conduzindo arquitetos iniciantes por conceitos, práticas locais e um projeto hospitalar progressivo.

**Architecture:** O conteúdo canônico viverá em `docs/`, dividido em oito páginas previsíveis por módulo e apoiado por um laboratório Python progressivo em `laboratorios/plataforma-hospitalar/`. Um validador editorial, testes `unittest`, o build estrito do MkDocs e o workflow do GitHub Pages formarão a barreira de qualidade; o material do professor permanecerá local e ignorado pelo Git.

**Tech Stack:** Python 3.11+, MkDocs Material 9.7.6, Markdown, Mermaid 11, FastAPI, pytest, Docker Compose, PostgreSQL, Kong, OpenTelemetry, Jaeger, RabbitMQ, kind e Kubernetes.

## Global Constraints

- A disciplina tem 24 horas em seis encontros de quatro horas.
- O público é de pós-graduação, com experiência em .NET, Java ou Python e sem formação arquitetural sistemática.
- Conceitos são ensinados antes do caso e definidos antes de aparecerem em exercícios.
- Python é a implementação executável de referência; Java e .NET aparecem em quadros de equivalência.
- Toda oficina essencial é local, open source e documentada para Windows, macOS e Linux.
- Enunciados de Aplicar, Analisar e Avaliar incluem situação, papel, insumos, condução, entrega e critérios de avaliação.
- A expressão pública é “critérios de avaliação”; “rubrica”, pontos e pontuação não aparecem nas páginas do aluno.
- O material não menciona cartão, crédito ou cobrança para classificar formas de acesso a ferramentas; ferramentas obrigatórias são descritas como open source.
- Percentuais de cada instrumento somam exatamente 100%.
- O caso integrador é uma plataforma hospitalar conectada a planos de saúde e laboratórios.
- Os arquivos Markdown legados da raiz permanecem acessíveis durante toda a primeira versão.
- `material-professor/` permanece local, ignorado pelo Git e ausente do site público.
- Imagens têm texto alternativo e explicação textual equivalente; Mermaid permanece legível como código no GitHub.
- A implementação deve acontecer em uma worktree isolada criada com `superpowers:using-git-worktrees`.
- Cada tarefa termina com testes verdes e um commit focado.

---

## Mapa de arquivos

### Fundação e publicação

- `mkdocs.yml`: configuração, navegação e extensões Markdown.
- `requirements.txt`: dependência fixada do gerador do site.
- `course_semantics.py`: classes semânticas do tema Academia sem contaminar o Markdown.
- `docs/assets/stylesheets/extra.css`: tokens, tipografia e componentes visuais.
- `docs/assets/javascripts/mermaid.mjs`: inicialização do Mermaid.
- `.github/workflows/publicar-site.yml`: teste, validação, build e deploy.
- `scripts/validate_content.py`: regras editoriais e estruturais.
- `tests/course_assertions.py`: funções de asserção compartilhadas pelos testes de módulos.

### Conteúdo público

- `docs/comecar/`: orientação, mapa, Bloom e preparação.
- `docs/modulo-{1..6}-*/`: oito páginas por encontro.
- `docs/projeto-integrador/`: contexto, incrementos, templates e avaliação.
- `docs/referencia/`: glossário, atributos, padrões, ferramentas, ADRs e bibliografia.
- `docs/sobre/`: plano da disciplina e créditos.
- `docs/assets/images/`: capa e infográficos em português.

### Prática executável

- `laboratorios/plataforma-hospitalar/pyproject.toml`: ambiente Python único.
- `laboratorios/plataforma-hospitalar/src/hospital/`: código cumulativo do caso.
- `laboratorios/plataforma-hospitalar/tests/`: testes executáveis por encontro.
- `laboratorios/plataforma-hospitalar/infra/`: Compose, Kong, telemetria, RabbitMQ e Kubernetes.

### Material local do professor

- `material-professor/README.md`: como usar o acervo docente.
- `material-professor/aula-{1..6}.md`: roteiro, escolhas e contingências.
- `material-professor/respostas/`: respostas comentadas.
- `material-professor/projeto-referencia/`: solução arquitetural docente.

---

### Task 1: Fundação MkDocs e pipeline de publicação

**Files:**
- Create: `requirements.txt`
- Create: `mkdocs.yml`
- Create: `.github/workflows/publicar-site.yml`
- Create: `docs/index.md`
- Create: `docs/modulo-1-visao-geral/index.md`
- Create: `docs/modulo-2-apis/index.md`
- Create: `docs/modulo-3-servicos/index.md`
- Create: `docs/modulo-4-governanca/index.md`
- Create: `docs/modulo-5-eventos/index.md`
- Create: `docs/modulo-6-nuvem/index.md`
- Create: `docs/assets/javascripts/mermaid.mjs`
- Create: `tests/test_site_foundation.py`

**Interfaces:**
- Produces: site MkDocs invocável com `python -m mkdocs build --strict`.
- Produces: workflow que chama `python -m unittest discover -s tests -v`, `python scripts/validate_content.py --all` e `mkdocs build --strict`, nessa ordem.

- [ ] **Step 1: Escrever o teste de fundação que falha**

```python
# tests/test_site_foundation.py
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

class SiteFoundationTest(unittest.TestCase):
    def test_required_foundation_files_exist(self):
        for relative in (
            "mkdocs.yml", "requirements.txt",
            ".github/workflows/publicar-site.yml",
            "docs/index.md", "docs/assets/javascripts/mermaid.mjs",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_six_modules_are_in_navigation(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        rendered = str(config["nav"])
        for label in ("Estilos", "APIs", "Serviços", "Governança", "Eventos", "Nuvem"):
            self.assertIn(label, rendered)

    def test_publication_gate_order(self):
        text = (ROOT / ".github/workflows/publicar-site.yml").read_text(encoding="utf-8")
        commands = (
            "python -m unittest discover -s tests -v",
            "python scripts/validate_content.py --all",
            "mkdocs build --strict",
        )
        self.assertEqual(sorted(map(text.index, commands)), list(map(text.index, commands)))
```

- [ ] **Step 2: Executar e confirmar a falha**

Run: `python -m unittest tests.test_site_foundation -v`

Expected: `FAIL` porque `mkdocs.yml` e os demais arquivos ainda não existem.

- [ ] **Step 3: Criar a fundação mínima**

Use `mkdocs-material==9.7.6` em `requirements.txt`. Configure `site_name: Arquitetura de Software`, `language: pt-BR`, `primary: custom`, `use_directory_urls: true`, Mermaid com `pymdownx.superfences`, o hook `course_semantics.py`, CSS/JS em `docs/assets/` e a navegação dos seis módulos. A página inicial deve apresentar os seis encontros. Crie também os seis `index.md` de módulo com título, encontro, resultado principal e aviso de que a navegação detalhada será acrescentada com as páginas do encontro; esse texto é uma introdução válida, não um marcador editorial.

O JavaScript deve fixar Mermaid 11 e reinicializar após navegação instantânea:

```javascript
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.12.2/+esm";
mermaid.initialize({ startOnLoad: false, securityLevel: "loose", theme: "neutral" });
document$.subscribe(() => mermaid.run({ querySelector: ".mermaid" }));
```

O workflow deve usar `actions/checkout@v4`, `actions/setup-python@v5`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3` e `actions/deploy-pages@v4`, com permissões `contents: read`, `pages: write` e `id-token: write`.

- [ ] **Step 4: Instalar dependências e executar o teste**

Run: `python -m pip install -r requirements.txt && python -m unittest tests.test_site_foundation -v`

Expected: `3 tests ... OK`.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt mkdocs.yml .github/workflows/publicar-site.yml docs/index.md docs/modulo-*/index.md docs/assets/javascripts/mermaid.mjs tests/test_site_foundation.py
git commit -m "feat: scaffold architecture course site"
```

### Task 2: Sistema visual Academia e semântica acessível

**Files:**
- Create: `course_semantics.py`
- Create: `docs/assets/stylesheets/extra.css`
- Create: `tests/test_visual_system.py`

**Interfaces:**
- Consumes: headings e blockquotes Markdown definidos pelos módulos.
- Produces: `on_page_content(html: str, **kwargs) -> str`.
- Produces: classes `.module-opening`, `.objective-card`, `.decision-callout`, `.risk-callout`, `.bloom-label`, `.architecture-figure`, `.comparison-table`, `.adr-block` e `.criteria`.

- [ ] **Step 1: Escrever testes visuais que falham**

```python
# tests/test_visual_system.py
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AcademiaVisualSystemTest(unittest.TestCase):
    def test_tokens_typography_and_components(self):
        css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")
        for value in ("#16243A", "#254DB8", "#5FC0D1", "#F2F6FB", "#FFFFFF", "#F2B84B"):
            self.assertIn(value, css)
        for value in ("Charter", "Georgia", "Inter", "Segoe UI", "IBM Plex Mono", "Consolas"):
            self.assertIn(value, css)
        for selector in (".module-opening", ".objective-card", ".decision-callout", ".risk-callout", ".bloom-label", ".architecture-figure", ".comparison-table", ".adr-block", ".criteria"):
            self.assertIn(selector, css)

    def test_accessibility_rules(self):
        css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")
        for marker in (":focus-visible", "prefers-reduced-motion", "overflow-x: auto", "max-width: 100%"):
            self.assertIn(marker, css)
        self.assertNotIn("outline: none", css)

    def test_semantic_hook_exposes_expected_interface(self):
        from course_semantics import on_page_content
        html = on_page_content('<h1>Título</h1><table><tr><td>x</td></tr></table>')
        self.assertIn("module-opening", html)
        self.assertIn("comparison-table", html)
```

- [ ] **Step 2: Executar e confirmar a falha**

Run: `python -m unittest tests.test_visual_system -v`

Expected: `ERROR` por arquivos ainda ausentes.

- [ ] **Step 3: Implementar hook e CSS**

Implemente `on_page_content` com substituições semânticas por expressões regulares, sem seletores posicionais amplos. O CSS deve declarar tokens de cor, espaçamento, largura de leitura, raio e sombra; tipografia editorial para títulos; sans-serif para corpo; mono para código; foco cobalto com contraste mínimo 3:1; rótulos textuais `DECISÃO`, `RISCO` e `CRITÉRIOS`; ajustes para telas abaixo de 768 px.

```python
def on_page_content(html: str, **_kwargs) -> str:
    html = _class_tags(html, r"<h1(?:\s[^>]*)?>", "module-opening")
    html = _class_tags(html, r"<table(?:\s[^>]*)?>", "comparison-table")
    html = _class_tags(html, r'<h2\b[^>]*\bid="(?:recordar|compreender|aplicar|analisar|avaliar|criar)"[^>]*>', "bloom-label")
    html = _class_tags(html, r"<p(?:\s[^>]*)?>(?=<strong>Critérios de avaliação)", "criteria")
    return html
```

- [ ] **Step 4: Verificar testes e build**

Run: `python -m unittest tests.test_visual_system -v && python -m mkdocs build --strict`

Expected: testes `OK`; build concluído sem erros.

- [ ] **Step 5: Commit**

```bash
git add course_semantics.py docs/assets/stylesheets/extra.css tests/test_visual_system.py
git commit -m "feat: add accessible Academia visual system"
```

### Task 3: Contrato editorial, páginas compartilhadas e validador

**Files:**
- Create: `scripts/validate_content.py`
- Create: `tests/course_assertions.py`
- Create: `tests/test_content_contract.py`
- Create: `docs/comecar/sobre-a-disciplina.md`
- Create: `docs/comecar/como-usar.md`
- Create: `docs/comecar/mapa-de-aprendizagem.md`
- Create: `docs/comecar/taxonomia-de-bloom.md`
- Create: `docs/referencia/glossario.md`
- Create: `docs/referencia/atributos-de-qualidade.md`
- Create: `docs/referencia/catalogo-de-padroes.md`
- Create: `docs/referencia/guia-de-ferramentas.md`
- Create: `docs/referencia/template-adr.md`
- Create: `docs/referencia/bibliografia.md`
- Create: `docs/sobre/plano-da-disciplina.md`
- Modify: `mkdocs.yml`

**Interfaces:**
- Produces: `MODULES: dict[str, str]`, `PAGES: tuple[str, ...]`, `BLOOM: tuple[str, ...]`.
- Produces: `bloom_sections(text: str) -> dict[str, str]` e CLI `validate_content.py --module SLUG|--all`.
- Produces: `assert_module_contract(testcase, slug, required_terms)` para testes específicos.

- [ ] **Step 1: Escrever testes do contrato**

```python
# tests/test_content_contract.py
from pathlib import Path
import unittest
from scripts.validate_content import MODULES, PAGES

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

class ContentContractTest(unittest.TestCase):
    def test_course_has_six_modules_and_eight_page_contract(self):
        self.assertEqual(6, len(MODULES))
        self.assertEqual(8, len(PAGES))
        self.assertEqual("index.md", PAGES[0])
        self.assertEqual("sintese-e-referencias.md", PAGES[-1])

    def test_public_pages_use_assessment_criteria_vocabulary(self):
        for path in DOCS.rglob("*.md"):
            if "superpowers" in path.parts:
                continue
            text = path.read_text(encoding="utf-8").casefold()
            self.assertNotRegex(text, r"\brubricas?\b|\bpontua(?:ção|cao)\b|\b\d+\s+pontos?\b")
```

- [ ] **Step 2: Executar e observar falha do validador ausente**

Run: `python -m unittest tests.test_content_contract -v`

Expected: `ERROR` porque `scripts.validate_content` ainda não existe.

- [ ] **Step 3: Implementar o validador e o helper**

Defina exatamente:

```python
MODULES = {
    "modulo-1-visao-geral": "Visão geral de estilos",
    "modulo-2-apis": "Arquitetura de APIs",
    "modulo-3-servicos": "Arquitetura de Serviços",
    "modulo-4-governanca": "Governança de Serviços",
    "modulo-5-eventos": "Arquiteturas de Eventos",
    "modulo-6-nuvem": "Arquiteturas de Nuvens",
}
PAGES = ("index.md", "conceitos.md", "padroes-e-decisoes.md", "exemplo-arquitetural.md", "estudo-de-caso.md", "oficina-de-ferramentas.md", "exercicios.md", "sintese-e-referencias.md")
BLOOM = ("Recordar", "Compreender", "Aplicar", "Analisar", "Avaliar", "Criar")
```

O validador deve verificar arquivos, links e âncoras locais, texto alternativo, equivalência textual após figuras, marcadores `TODO|TBD|PLACEHOLDER|PREENCHER`, seis seções Bloom, blocos de resposta apenas em Recordar/Compreender, critérios em níveis avançados, percentuais somando 100% por instrumento, 5.000–8.500 palavras por módulo e 32.000–51.000 no total. Deve reprovar páginas públicas que usem “rubrica”, pontos, pontuação, cartão, crédito ou cobrança para classificar acesso a ferramentas. Nos laboratórios e exercícios, rótulos procedimentais em negrito devem terminar o parágrafo e ser seguidos por linha em branco, evitando blocos visualmente aglutinados.

Implemente o helper compartilhado integralmente:

```python
# tests/course_assertions.py
from pathlib import Path
import re
from scripts.validate_content import PAGES, bloom_sections

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

def assert_module_contract(testcase, slug: str, required_terms: tuple[str, ...]) -> None:
    module = DOCS / slug
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for page in PAGES:
        testcase.assertTrue((module / page).is_file(), f"{slug}/{page}")
        testcase.assertIn(f"{slug}/{page}", navigation)
    corpus = "\n".join((module / page).read_text(encoding="utf-8") for page in PAGES)
    testcase.assertIn("## Equivalências em Java e .NET", corpus)
    for term in required_terms:
        testcase.assertIn(term.casefold(), corpus.casefold(), term)
    workshop = (module / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
    for heading in ("## Ferramenta", "## Pré-requisitos", "## Instalação", "## Preparação do laboratório", "## Execução", "## Resultado esperado", "## Interpretação", "## Limpeza e contingência", "## Evidência a entregar"):
        testcase.assertIn(heading, workshop)
    for platform in ("### Windows", "### macOS", "### Linux"):
        testcase.assertIn(platform, workshop)
    for label in ("Essencial em aula", "Exploração em dupla", "Extensão"):
        testcase.assertIn(label, workshop)
    for prompt in ("**Objetivo**", "**Pré-requisito**", "**Execute**", "**Observe**", "**Compare**", "Questões exploratórias"):
        testcase.assertIn(prompt, workshop)
    exercises = (module / "exercicios.md").read_text(encoding="utf-8")
    sections = bloom_sections(exercises)
    testcase.assertEqual({"Recordar", "Compreender", "Aplicar", "Analisar", "Avaliar", "Criar"}, set(sections))
    for level in ("Aplicar", "Analisar", "Avaliar"):
        for marker in ("**Situação**", "**Seu papel**", "**Insumos disponíveis**", "**Como conduzir**", "**Entrega esperada**", "**Critérios de avaliação**"):
            testcase.assertIn(marker, sections[level])
        testcase.assertRegex(sections[level], r"\|[^\n]*\|\s*\d+%\s*\|")
```

- [ ] **Step 4: Criar as páginas compartilhadas com conteúdo final**

Use os seguintes núcleos, sem texto provisório:

- `sobre-a-disciplina.md`: público, pré-requisitos, seis encontros e método;
- `como-usar.md`: sequência conceito → exemplo → oficina → evidência → projeto;
- `mapa-de-aprendizagem.md`: progressão dos seis encontros;
- `taxonomia-de-bloom.md`: níveis, verbos, exemplos e controle do professor;
- `glossario.md`: estilo, componente, conector, fronteira, contrato, atributo de qualidade, acoplamento, coesão, idempotência, consistência eventual, telemetria, plano de dados e plano de controle;
- `atributos-de-qualidade.md`: desempenho, disponibilidade, segurança, modificabilidade, testabilidade, interoperabilidade e operabilidade;
- `catalogo-de-padroes.md`: padrões ensinados e módulo de referência;
- `guia-de-ferramentas.md`: finalidade, licença aberta, módulo, instalação e equivalentes;
- `template-adr.md`: contexto, forças, alternativas, decisão, consequências e evidências;
- `bibliografia.md`: fontes primárias e livros-base;
- `plano-da-disciplina.md`: 24 horas e objetivos por encontro.

Acrescente `Começar`, `Projeto integrador`, `Referência` e `Sobre` à navegação do `mkdocs.yml`, apontando somente para arquivos criados nesta tarefa.

Crie arquivos vazios apenas pelo tempo necessário para observar a primeira falha; antes do commit, cada página compartilhada deve conter todos os núcleos acima e cada página de módulo será criada em sua tarefa correspondente.

- [ ] **Step 5: Executar testes unitários do validador**

Run: `python -m unittest tests.test_content_contract -v && python -m mkdocs build --strict`

Expected: `2 tests ... OK` e build estrito concluído. A existência das oito páginas será exigida módulo a módulo por `assert_module_contract` nas Tasks 5–10.

- [ ] **Step 6: Commit**

```bash
git add scripts tests/course_assertions.py tests/test_content_contract.py docs/comecar docs/referencia docs/sobre mkdocs.yml
git commit -m "feat: define course editorial contract"
```

### Task 4: Caso hospitalar e projeto integrador progressivo

**Files:**
- Create: `docs/projeto-integrador/index.md`
- Create: `docs/projeto-integrador/contexto-hospitalar.md`
- Create: `docs/projeto-integrador/incrementos.md`
- Create: `docs/projeto-integrador/modelos-de-entrega.md`
- Create: `docs/projeto-integrador/criterios-de-avaliacao.md`
- Create: `tests/test_integrative_project.py`
- Create: `laboratorios/plataforma-hospitalar/README.md`
- Create: `laboratorios/plataforma-hospitalar/pyproject.toml`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/__init__.py`

**Interfaces:**
- Produces: contexto comum consumido pelos seis módulos.
- Produces: pacote Python `hospital` e comando de teste `python -m pytest laboratorios/plataforma-hospitalar/tests`.

- [ ] **Step 1: Escrever teste do projeto**

```python
# tests/test_integrative_project.py
from pathlib import Path
import re, unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "docs/projeto-integrador"

class IntegrativeProjectTest(unittest.TestCase):
    def test_six_increments_and_external_integrations(self):
        text = (PROJECT / "incrementos.md").read_text(encoding="utf-8")
        self.assertEqual(6, len(re.findall(r"(?m)^## Incremento \d", text)))
        context = (PROJECT / "contexto-hospitalar.md").read_text(encoding="utf-8")
        for term in ("plano de saúde", "laboratório", "paciente", "faturamento", "auditoria"):
            self.assertIn(term, context.casefold())

    def test_assessment_percentages_sum_to_100(self):
        text = (PROJECT / "criterios-de-avaliacao.md").read_text(encoding="utf-8")
        values = [int(value) for value in re.findall(r"\|\s*(\d+)%\s*\|", text)]
        self.assertEqual(100, sum(values))
```

- [ ] **Step 2: Executar e confirmar a falha**

Run: `python -m unittest tests.test_integrative_project -v`

Expected: `ERROR` por páginas ausentes.

- [ ] **Step 3: Escrever o contexto e os seis incrementos**

Defina pacientes, profissionais, operadoras e laboratórios; capacidades de cadastro, agenda, elegibilidade, autorização, exames, resultados, faturamento, notificações e auditoria; restrições de privacidade, rastreabilidade, interoperabilidade e disponibilidade. Cada incremento deve listar `Objetivo`, `Insumos`, `Passos`, `Artefato`, `Evidência` e `Conexão com o próximo encontro`.

Use seis critérios somando 100%: coerência 20%, decisões e trade-offs 20%, contratos e integrações 15%, dados/eventos 15%, governança/operação 15% e clareza/evidências 15%.

- [ ] **Step 4: Criar o esqueleto executável**

Configure `pyproject.toml` com Python `>=3.11`, pacote em `src`, dependências `fastapi`, `uvicorn`, `pydantic`, `httpx`, `psycopg[binary]`, `aio-pika`, `opentelemetry-sdk` e dependências de desenvolvimento `pytest`, `pytest-asyncio`. O README deve conter preparação equivalente para PowerShell e shells POSIX.

Instale o workspace antes dos testes posteriores:

Run: `python -m pip install -e "laboratorios/plataforma-hospitalar[dev]"`

Expected: pacote `hospital` instalado em modo editável sem erros.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_integrative_project -v`

Expected: `2 tests ... OK`.

```bash
git add docs/projeto-integrador tests/test_integrative_project.py laboratorios/plataforma-hospitalar
git commit -m "feat: establish hospital integrative project"
```

### Task 5: Módulo 1 — Visão Geral de Estilos Arquiteturais

**Files:**
- Modify: `docs/modulo-1-visao-geral/index.md`
- Create: `docs/modulo-1-visao-geral/{conceitos,padroes-e-decisoes,exemplo-arquitetural,estudo-de-caso,oficina-de-ferramentas,exercicios,sintese-e-referencias}.md`
- Create: `tests/test_module_one.py`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/estilos.py`
- Create: `laboratorios/plataforma-hospitalar/tests/test_estilos.py`
- Modify: `mkdocs.yml`

**Interfaces:**
- Produces: `comparar_estilos(cenario: dict) -> list[dict]` com campos `estilo`, `forcas`, `limites` e `evidencias`.
- Consumes: contexto e template ADR da Task 4.

- [ ] **Step 1: Testar contrato e prática do módulo**

```python
# tests/test_module_one.py
from tests.course_assertions import assert_module_contract
import unittest

class ModuleOneTest(unittest.TestCase):
    def test_content(self):
        assert_module_contract(self, "modulo-1-visao-geral", (
            "componente", "conector", "atributo de qualidade", "camadas",
            "pipes and filters", "microkernel", "monólito modular", "ADR",
            "Structurizr Lite", "Python", ".NET", "Java",
        ))
```

No teste de laboratório, forneça um cenário com alta modificabilidade e confira que cada alternativa retorna forças, limites e evidências não vazias.

- [ ] **Step 2: Executar e confirmar falha**

Run: `python -m unittest tests.test_module_one -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_estilos.py -q`

Expected: falha por módulo e função ausentes.

- [ ] **Step 3: Escrever as oito páginas**

Cubra: o que é arquitetura; estrutura, decisões e atributos; estilos em camadas, pipes and filters, microkernel e monólito modular; diferenças entre estilo, padrão e tecnologia; ADR; comparação aplicada à triagem, faturamento e agenda hospitalar. A oficina deve instalar Python, pytest e Structurizr Lite em Windows/macOS/Linux, executar `test_estilos.py`, alterar uma força arquitetural, comparar resultados e registrar um mini-ADR. Inclua trilhas `Essencial em aula`, `Exploração em dupla` e `Extensão`. Expanda a entrada do módulo no `mkdocs.yml` com as oito páginas na ordem do contrato editorial.

- [ ] **Step 4: Implementar `comparar_estilos` e os testes**

Use uma tabela explícita de estilos e filtre/ordene pelas forças solicitadas; não crie um motor genérico de regras. O teste deve demonstrar que mudar a prioridade de modificabilidade para throughput altera a justificativa observada.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_module_one -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_estilos.py -q && python scripts/validate_content.py --module modulo-1-visao-geral`

Expected: testes `OK`, pytest `passed`, módulo dentro do orçamento.

```bash
git add docs/modulo-1-visao-geral tests/test_module_one.py laboratorios/plataforma-hospitalar mkdocs.yml
git commit -m "feat: add architectural styles module"
```

### Task 6: Módulo 2 — Arquitetura de APIs

**Files:**
- Modify: `docs/modulo-2-apis/index.md`
- Create: `docs/modulo-2-apis/{conceitos,padroes-e-decisoes,exemplo-arquitetural,estudo-de-caso,oficina-de-ferramentas,exercicios,sintese-e-referencias}.md`
- Create: `tests/test_module_two.py`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/api/main.py`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/api/models.py`
- Create: `laboratorios/plataforma-hospitalar/tests/test_api_contract.py`
- Create: `laboratorios/plataforma-hospitalar/contratos/openapi.yaml`
- Create: `laboratorios/plataforma-hospitalar/contratos/.spectral.yaml`
- Modify: `mkdocs.yml`

**Interfaces:**
- Produces: `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`.
- Produces: schemas `PedidoElegibilidade`, `ElegibilidadeAceita` e `ErroAPI`.

- [ ] **Step 1: Criar testes vermelhos de conteúdo e contrato**

O teste editorial exige `REST`, `HTTP`, `OpenAPI`, `idempotência`, `versionamento`, `paginação`, `FastAPI`, `Bruno`, `Spectral`, `ASP.NET Core` e `Spring Boot`. O teste FastAPI envia um pedido válido, espera `202`, cabeçalho `Location`, protocolo e recuperação posterior; envia CPF ausente e espera erro `422` estruturado.

- [ ] **Step 2: Executar e confirmar falhas**

Run: `python -m unittest tests.test_module_two -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_api_contract.py -q`

Expected: falhas por páginas e aplicação ausentes.

- [ ] **Step 3: Escrever conteúdo e oficina instrumental**

Ensine contrato, recurso, método, status, cabeçalhos, idempotência, evolução compatível, REST versus RPC/GraphQL/gRPC e gateway. A oficina conduz: instalar Python/Bruno/Node; subir FastAPI; abrir `/docs`; importar `openapi.yaml` no Bruno; criar elegibilidade; consultar protocolo; provocar erro; validar com `npx @stoplight/spectral-cli lint`; alterar uma regra; comparar contrato e execução. Cada comando deve ter resultado esperado e contingência. Expanda a entrada do módulo no `mkdocs.yml` com as oito páginas.

- [ ] **Step 4: Implementar API e contrato versionado**

Use armazenamento em memória apenas neste módulo. Mantenha `openapi.yaml` como contrato explícito e teste os exemplos nele. Não introduza autenticação real ainda.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_module_two -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_api_contract.py -q && npx @stoplight/spectral-cli lint laboratorios/plataforma-hospitalar/contratos/openapi.yaml && python scripts/validate_content.py --module modulo-2-apis`

Expected: todos os comandos terminam com código 0.

```bash
git add docs/modulo-2-apis tests/test_module_two.py laboratorios/plataforma-hospitalar mkdocs.yml
git commit -m "feat: add API architecture module"
```

### Task 7: Módulo 3 — Arquitetura de Serviços

**Files:**
- Modify: `docs/modulo-3-servicos/index.md`
- Create: `docs/modulo-3-servicos/{conceitos,padroes-e-decisoes,exemplo-arquitetural,estudo-de-caso,oficina-de-ferramentas,exercicios,sintese-e-referencias}.md`
- Create: `tests/test_module_three.py`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/servicos/elegibilidade.py`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/servicos/exames.py`
- Create: `laboratorios/plataforma-hospitalar/tests/test_service_boundaries.py`
- Create: `laboratorios/plataforma-hospitalar/Dockerfile`
- Create: `laboratorios/plataforma-hospitalar/infra/compose.servicos.yml`
- Create: `laboratorios/plataforma-hospitalar/infra/postgres/init.sql`
- Modify: `mkdocs.yml`

**Interfaces:**
- Produces: serviços `elegibilidade` e `exames` com bancos logicamente separados.
- Produces: teste de contrato HTTP que não importa internals do outro serviço.

- [ ] **Step 1: Testar conceitos e fronteiras**

Exija `capacidade de negócio`, `bounded context`, `coesão`, `acoplamento`, `monólito modular`, `microsserviço`, `banco por serviço`, `consistência`, `SAGA`, `CQRS`, `Docker Compose` e `PostgreSQL`. O teste executável deve falhar se o serviço de exames acessar diretamente a tabela de elegibilidade.

- [ ] **Step 2: Executar e confirmar falhas**

Run: `python -m unittest tests.test_module_three -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_service_boundaries.py -q`

Expected: falhas por conteúdo e serviços ausentes.

- [ ] **Step 3: Escrever módulo e oficina**

Conduza o estudante da decomposição lógica à distribuição física; explique por que microsserviços não são objetivo em si; compare monólito modular, macrosserviços e microsserviços; introduza propriedade dos dados, chamadas síncronas, falhas parciais, SAGA e CQRS sem exigir implementação completa dos dois últimos. A oficina sobe Compose, inspeciona health checks, chama os dois serviços, interrompe um contêiner, observa falha parcial e executa o teste de contrato. Expanda a entrada do módulo no `mkdocs.yml` com as oito páginas.

- [ ] **Step 4: Implementar serviços mínimos e Compose**

Use dois processos FastAPI e dois schemas PostgreSQL. Exponha `/health`; configure dependências e health checks; mantenha todas as credenciais apenas como valores locais didáticos no Compose.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_module_three -v && docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml config --quiet`

Expected: testes editoriais e validação do Compose passam.

Run: `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml up -d --build --wait`

Expected: serviços e bancos ficam `healthy`.

Run: `python -m pytest laboratorios/plataforma-hospitalar/tests/test_service_boundaries.py -q && python scripts/validate_content.py --module modulo-3-servicos`

Expected: testes e validador passam.

Run: `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml down -v`

Expected: contêineres, rede e volumes didáticos removidos.

```bash
git add docs/modulo-3-servicos tests/test_module_three.py laboratorios/plataforma-hospitalar mkdocs.yml
git commit -m "feat: add service architecture module"
```

### Task 8: Módulo 4 — Governança de Serviços

**Files:**
- Modify: `docs/modulo-4-governanca/index.md`
- Create: `docs/modulo-4-governanca/{conceitos,padroes-e-decisoes,exemplo-arquitetural,estudo-de-caso,oficina-de-ferramentas,exercicios,sintese-e-referencias}.md`
- Create: `tests/test_module_four.py`
- Create: `laboratorios/plataforma-hospitalar/infra/kong/kong.yml`
- Create: `laboratorios/plataforma-hospitalar/infra/observabilidade/otel-collector.yml`
- Create: `laboratorios/plataforma-hospitalar/infra/compose.governanca.yml`
- Create: `laboratorios/plataforma-hospitalar/tests/test_gateway_policy.py`
- Modify: `mkdocs.yml`

**Interfaces:**
- Produces: rota Kong `/hospital/elegibilidades` com correlation ID e rate limiting.
- Produces: trace ponta a ponta visível no Jaeger.

- [ ] **Step 1: Testar políticas observáveis**

Exija `governança`, `política`, `gateway`, `rate limiting`, `correlation ID`, `logs`, `métricas`, `traces`, `SLO`, `OpenTelemetry`, `Jaeger` e `Kong`. O teste envia requisições pelo gateway, confirma cabeçalho de correlação e observa `429` após o limite declarado.

- [ ] **Step 2: Executar e confirmar falhas**

Run: `python -m unittest tests.test_module_four -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_gateway_policy.py -q`

Expected: falhas por configuração ausente.

- [ ] **Step 3: Escrever módulo e oficina**

Defina governança como decisões e políticas verificáveis, separando design-time e runtime; ensine catálogo, ownership, versionamento, segurança, limites, logs, métricas, traces e SLO. A oficina instala Docker, sobe Kong/Collector/Jaeger, chama direto e via gateway, localiza o trace por correlation ID, excede o limite e compara os efeitos. Explique onde editar `kong.yml` e como confirmar o reload. Expanda a entrada do módulo no `mkdocs.yml` com as oito páginas.

- [ ] **Step 4: Implementar configuração declarativa**

Fixe imagens de contêiner por versão, configure Kong DB-less, OpenTelemetry Collector e Jaeger all-in-one. A política precisa ser reproduzível sem painel web proprietário.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_module_four -v && docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml config --quiet`

Expected: testes editoriais e validação do Compose passam.

Run: `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml up -d --build --wait`

Expected: API, Kong, Collector e Jaeger ficam disponíveis.

Run: `python -m pytest laboratorios/plataforma-hospitalar/tests/test_gateway_policy.py -q && python scripts/validate_content.py --module modulo-4-governanca`

Expected: política e conteúdo passam.

Run: `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml down -v`

Expected: ambiente removido.

```bash
git add docs/modulo-4-governanca tests/test_module_four.py laboratorios/plataforma-hospitalar mkdocs.yml
git commit -m "feat: add service governance module"
```

### Task 9: Módulo 5 — Arquiteturas de Eventos

**Files:**
- Modify: `docs/modulo-5-eventos/index.md`
- Create: `docs/modulo-5-eventos/{conceitos,padroes-e-decisoes,exemplo-arquitetural,estudo-de-caso,oficina-de-ferramentas,exercicios,sintese-e-referencias}.md`
- Create: `tests/test_module_five.py`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/eventos/publicador.py`
- Create: `laboratorios/plataforma-hospitalar/src/hospital/eventos/consumidor.py`
- Create: `laboratorios/plataforma-hospitalar/tests/test_event_idempotency.py`
- Create: `laboratorios/plataforma-hospitalar/infra/compose.eventos.yml`
- Modify: `mkdocs.yml`

**Interfaces:**
- Produces: evento `ResultadoLaboratorialDisponibilizado.v1` com `event_id`, `occurred_at`, `exam_id`, `patient_id` e `result_reference`.
- Produces: consumidor idempotente que registra `event_id` processado.

- [ ] **Step 1: Testar semântica e repetição**

Exija `evento`, `comando`, `mensagem`, `broker`, `fila`, `tópico`, `entrega pelo menos uma vez`, `idempotência`, `ordenação`, `dead-letter queue`, `RabbitMQ`, `Kafka` e `consistência eventual`. Publique o mesmo evento duas vezes e confirme um único efeito de negócio e duas tentativas registradas.

- [ ] **Step 2: Executar e confirmar falhas**

Run: `python -m unittest tests.test_module_five -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_event_idempotency.py -q`

Expected: falhas por publicador/consumidor ausentes.

- [ ] **Step 3: Escrever módulo e oficina**

Ensine eventos como fatos passados, compare broker e mediator, filas e logs distribuídos, RabbitMQ e Kafka, entrega, repetição, ordem, schema e evolução. A oficina sobe RabbitMQ, publica um resultado, executa consumidor, repete a mensagem, inspeciona evidências de idempotência, provoca erro e observa a dead-letter queue. Expanda a entrada do módulo no `mkdocs.yml` com as oito páginas.

- [ ] **Step 4: Implementar fluxo local**

Use `aio-pika`, exchange `hospital.events`, fila `billing.resultados.v1`, dead-letter exchange e SQLite/local memory somente para a tabela didática de mensagens processadas. Valide o schema Pydantic antes de confirmar a mensagem.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_module_five -v && docker compose -f laboratorios/plataforma-hospitalar/infra/compose.eventos.yml config --quiet`

Expected: testes editoriais e validação do Compose passam.

Run: `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.eventos.yml up -d --build --wait`

Expected: RabbitMQ e componentes do laboratório ficam disponíveis.

Run: `python -m pytest laboratorios/plataforma-hospitalar/tests/test_event_idempotency.py -q && python scripts/validate_content.py --module modulo-5-eventos`

Expected: repetição idempotente e conteúdo passam.

Run: `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.eventos.yml down -v`

Expected: ambiente removido.

```bash
git add docs/modulo-5-eventos tests/test_module_five.py laboratorios/plataforma-hospitalar mkdocs.yml
git commit -m "feat: add event architecture module"
```

### Task 10: Módulo 6 — Arquiteturas de Nuvens

**Files:**
- Modify: `docs/modulo-6-nuvem/index.md`
- Create: `docs/modulo-6-nuvem/{conceitos,padroes-e-decisoes,exemplo-arquitetural,estudo-de-caso,oficina-de-ferramentas,exercicios,sintese-e-referencias}.md`
- Create: `tests/test_module_six.py`
- Create: `laboratorios/plataforma-hospitalar/infra/k8s/namespace.yaml`
- Create: `laboratorios/plataforma-hospitalar/infra/k8s/deployment.yaml`
- Create: `laboratorios/plataforma-hospitalar/infra/k8s/service.yaml`
- Create: `laboratorios/plataforma-hospitalar/infra/k8s/configmap.yaml`
- Create: `laboratorios/plataforma-hospitalar/infra/k8s/hpa.yaml`
- Create: `laboratorios/plataforma-hospitalar/infra/kind/cluster.yaml`
- Create: `laboratorios/plataforma-hospitalar/tests/test_k8s_manifests.py`
- Modify: `mkdocs.yml`

**Interfaces:**
- Produces: implantação `hospital-api` com readiness, liveness, recursos, duas réplicas, rolling update e rollback.

- [ ] **Step 1: Testar propriedades dos manifests**

Exija `IaaS`, `PaaS`, `SaaS`, `região`, `zona`, `elasticidade`, `resiliência`, `contêiner`, `orquestração`, `readiness`, `liveness`, `rollback`, `Docker`, `kind` e `Kubernetes`. Carregue YAML e confirme probes distintas, requests/limits e estratégia `RollingUpdate`.

- [ ] **Step 2: Executar e confirmar falhas**

Run: `python -m unittest tests.test_module_six -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_k8s_manifests.py -q`

Expected: falhas por manifests ausentes.

- [ ] **Step 3: Escrever módulo e oficina**

Relacione nuvem a atributos e operação; explique modelos de serviço, responsabilidade compartilhada, regiões/zonas, stateless/stateful, doze fatores, escalabilidade, resiliência, custo e lock-in. A oficina instala Docker, kubectl e kind nos três sistemas; cria cluster; carrega imagem; aplica manifests; observa rollout; provoca uma versão com probe inválida; vê a indisponibilidade; desfaz com `kubectl rollout undo`; coleta evidências; remove cluster. Expanda a entrada do módulo no `mkdocs.yml` com as oito páginas.

- [ ] **Step 4: Criar manifests mínimos e testes**

Fixe apiVersion estável, namespace `hospital`, labels uniformes `app: hospital-api`, porta 8000, requests/limits explícitos e probes nos endpoints `/health/live` e `/health/ready`.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_module_six -v && python -m pytest laboratorios/plataforma-hospitalar/tests/test_k8s_manifests.py -q && kubectl apply --dry-run=client -f laboratorios/plataforma-hospitalar/infra/k8s && python scripts/validate_content.py --module modulo-6-nuvem`

Expected: todos passam.

```bash
git add docs/modulo-6-nuvem tests/test_module_six.py laboratorios/plataforma-hospitalar mkdocs.yml
git commit -m "feat: add cloud architecture module"
```

### Task 11: Infográficos, diagramas e equivalentes textuais

**Files:**
- Create: `docs/assets/images/capa-arquitetura-software.png`
- Create: `docs/assets/images/m01-mapa-estilos.png`
- Create: `docs/assets/images/m02-anatomia-api.png`
- Create: `docs/assets/images/m03-fronteiras-servicos.png`
- Create: `docs/assets/images/m04-governanca-observavel.png`
- Create: `docs/assets/images/m05-fluxo-eventos.png`
- Create: `docs/assets/images/m06-resiliencia-nuvem.png`
- Create: `docs/assets/images/prompts.md`
- Create: `tests/test_concept_infographics.py`
- Modify: `docs/index.md`
- Modify: `docs/modulo-{1..6}-*/conceitos.md`

**Interfaces:**
- Produces: sete PNGs 16:9, em português, com identidade Academia.
- Produces: uma única referência Markdown por imagem e parágrafo `**Leitura textual da figura:**` imediatamente posterior.

- [ ] **Step 1: Escrever teste de imagens**

```python
# tests/test_concept_infographics.py
from pathlib import Path
import re, unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
IMAGES = DOCS / "assets/images"

class ConceptInfographicsTest(unittest.TestCase):
    def test_required_images_are_referenced_once_with_text_equivalent(self):
        names = ("capa-arquitetura-software.png", "m01-mapa-estilos.png", "m02-anatomia-api.png", "m03-fronteiras-servicos.png", "m04-governanca-observavel.png", "m05-fluxo-eventos.png", "m06-resiliencia-nuvem.png")
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in DOCS.rglob("*.md")
            if "superpowers" not in path.parts and path.name != "prompts.md"
        )
        for name in names:
            self.assertTrue((IMAGES / name).is_file(), name)
            self.assertEqual(1, corpus.count(name), name)
        self.assertGreaterEqual(corpus.count("**Leitura textual da figura:**"), 7)
```

- [ ] **Step 2: Executar e confirmar falha**

Run: `python -m unittest tests.test_concept_infographics -v`

Expected: falha pelas sete imagens ausentes.

- [ ] **Step 3: Gerar as imagens com o skill `imagegen`**

Use um prompt-base registrado em `prompts.md`: “Infográfico acadêmico editorial, proporção 16:9, fundo claro, azul-marinho #16243A, cobalto #254DB8, ciano #5FC0D1 e âmbar #F2B84B, texto curto em português brasileiro, hierarquia legível, sem logotipos comerciais, sem aparência fotográfica”. Acrescente a cada arquivo: mapa comparativo de estilos; anatomia de contrato API; limites e dados de serviços; gateway/políticas/telemetria; publicação/broker/consumidores/idempotência; regiões/cluster/probes/rollback; e uma capa que sintetize a progressão dos seis encontros.

- [ ] **Step 4: Indexar e explicar cada imagem**

Inclua alt text que descreva a relação, legenda `*Figura N — ...*` e um parágrafo textual que percorra os elementos e setas. Use Mermaid, não imagem gerada, para diagramas de sequência das páginas `exemplo-arquitetural.md`.

- [ ] **Step 5: Verificar e commit**

Run: `python -m unittest tests.test_concept_infographics -v && python scripts/validate_content.py --all && python -m mkdocs build --strict`

Expected: todos passam.

```bash
git add docs/assets/images docs/index.md docs/modulo-* tests/test_concept_infographics.py
git commit -m "feat: add Portuguese architecture infographics"
```

### Task 12: Material local do professor

**Files:**
- Modify: `.gitignore`
- Create locally, ignored: `material-professor/README.md`
- Create locally, ignored: `material-professor/aula-{1..6}.md`
- Create locally, ignored: `material-professor/respostas/modulo-{1..6}.md`
- Create locally, ignored: `material-professor/projeto-referencia/solucao.md`
- Create: `tests/test_private_material_policy.py`

**Interfaces:**
- Produces localmente: roteiros de 240 minutos por encontro, gabaritos e solução de referência.
- Public boundary: nenhum arquivo sob `material-professor/` entra no índice Git ou no build MkDocs.

- [ ] **Step 1: Escrever teste da política pública**

```python
# tests/test_private_material_policy.py
from pathlib import Path
import subprocess, unittest

ROOT = Path(__file__).resolve().parents[1]

class PrivateMaterialPolicyTest(unittest.TestCase):
    def test_teacher_material_is_ignored_and_not_in_nav(self):
        ignored = subprocess.run(["git", "check-ignore", "material-professor/README.md"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, ignored.returncode)
        self.assertNotIn("material-professor", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
```

- [ ] **Step 2: Executar e confirmar falha**

Run: `python -m unittest tests.test_private_material_policy -v`

Expected: `FAIL` porque o caminho ainda não está ignorado.

- [ ] **Step 3: Ignorar e criar o conteúdo docente local**

Adicione `/material-professor/` a `.gitignore`. Em cada aula, distribua exatamente 240 minutos entre abertura, conceitos, exemplo, oficina, discussão, projeto e fechamento; marque essencial/extensão; inclua preparação Windows/macOS/Linux, erros esperados, respostas, critérios, pontos de parada e contingência sem Docker. A solução de referência deve conter os seis incrementos e justificar alternativas, sem ser copiada para `docs/`.

- [ ] **Step 4: Verificar isolamento e completude local**

Run: `python -m unittest tests.test_private_material_policy -v && git status --short --ignored material-professor`

Expected: teste `OK`; saída mostra somente `!! material-professor/`.

- [ ] **Step 5: Commit apenas da política**

```bash
git add .gitignore tests/test_private_material_policy.py
git commit -m "chore: keep teacher material private"
```

### Task 13: Compatibilidade do acervo legado e README de transição

**Files:**
- Modify: `README.md`
- Modify: todos os Markdown legados na raiz apenas para acrescentar uma nota canônica, sem remover conteúdo.
- Create: `docs/referencia/mapa-do-acervo-legado.md`
- Create: `tests/test_legacy_compatibility.py`

**Interfaces:**
- Produces: mapa `arquivo legado → módulo/página canônica`.
- Preserves: todos os caminhos Markdown existentes no commit-base `e223a79`.

- [ ] **Step 1: Escrever teste de preservação**

```python
# tests/test_legacy_compatibility.py
from pathlib import Path
import subprocess, unittest

ROOT = Path(__file__).resolve().parents[1]

class LegacyCompatibilityTest(unittest.TestCase):
    def test_baseline_root_markdown_files_still_exist(self):
        names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "e223a79"], cwd=ROOT, text=True).splitlines()
        legacy = [name for name in names if "/" not in name and name.endswith(".md")]
        self.assertTrue(legacy)
        for name in legacy:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_readme_documents_preview_validation_and_pages(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for marker in ("python3 -m venv .venv", "pip install -r requirements.txt", "mkdocs serve", "python scripts/validate_content.py --all", "mkdocs build --strict", "GitHub Actions"):
            self.assertIn(marker, text)
```

- [ ] **Step 2: Executar e confirmar a falha documental**

Run: `python -m unittest tests.test_legacy_compatibility -v`

Expected: preservação passa; README falha por instruções ausentes.

- [ ] **Step 3: Atualizar README e mapa**

Apresente propósito, público, seis encontros, site, prévia local, validação, laboratórios, material privado e publicação. Conserve uma seção “Acervo legado” com os links antigos. Em cada documento legado, acrescente ao início uma nota curta com link relativo para a página canônica correspondente; não reescreva nem exclua o corpo nesta etapa.

- [ ] **Step 4: Verificar links e commit**

Run: `python -m unittest tests.test_legacy_compatibility -v && python scripts/validate_content.py --all`

Expected: todos passam.

```bash
git add README.md ./*.md docs/referencia/mapa-do-acervo-legado.md tests/test_legacy_compatibility.py
git commit -m "docs: preserve legacy paths during site transition"
```

### Task 14: Auditoria integral, revisão visual e preparação da publicação

**Files:**
- Modify as needed: `docs/**/*.md`, `tests/**/*.py`, `scripts/validate_content.py`, `mkdocs.yml`
- Create: `docs/sobre/qualidade-do-material.md`

**Interfaces:**
- Consumes: todos os módulos, laboratórios, imagens e testes.
- Produces: uma `main` candidata à publicação sem falhas conhecidas.

- [ ] **Step 1: Executar a barreira integral e registrar qualquer falha**

Run: `python -m unittest discover -s tests -v`

Expected: todos os testes passam; se um falhar, corrija somente a causa demonstrada e repita o comando.

- [ ] **Step 2: Validar conteúdo e build**

Run: `python scripts/validate_content.py --all && python -m mkdocs build --strict`

Expected: “Validação concluída sem erros” e build com código 0.

- [ ] **Step 3: Validar laboratório Python e configurações**

Run: `python -m pytest laboratorios/plataforma-hospitalar/tests -q`

Expected: todos os testes passam.

Run: `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml config --quiet && docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml config --quiet && docker compose -f laboratorios/plataforma-hospitalar/infra/compose.eventos.yml config --quiet`

Expected: código 0 nos três arquivos.

- [ ] **Step 4: Revisar visualmente páginas representativas**

Run: `mkdocs serve`

Confira em desktop e largura móvel: início; conceitos e exemplo do módulo 1; oficina do módulo 2; exercício do módulo 3; oficina do módulo 4; diagrama do módulo 5; oficina do módulo 6; projeto integrador. Verifique que figuras não cortam texto, tabelas rolam horizontalmente, linhas e parágrafos quebram corretamente, Mermaid renderiza e o foco de teclado permanece visível.

- [ ] **Step 5: Registrar a política de qualidade**

Em `qualidade-do-material.md`, documente os quatro comandos de verificação, sistemas suportados, política de imagens, política de respostas e processo para reportar correções. Não inclua resultados efêmeros nem afirmações de cobertura sem teste.

- [ ] **Step 6: Executar verificação final de diff**

Run: `git diff --check && git status --short`

Expected: nenhuma falha de whitespace; apenas `qualidade-do-material.md` e correções intencionais ainda não commitadas.

- [ ] **Step 7: Commit da candidata à publicação**

```bash
git add docs tests scripts mkdocs.yml laboratorios README.md .github requirements.txt course_semantics.py .gitignore
git commit -m "docs: finalize architecture software course site"
```

- [ ] **Step 8: Finalizar a branch**

Use `superpowers:verification-before-completion`, depois `superpowers:requesting-code-review` e `superpowers:finishing-a-development-branch`. Somente após aprovação, mescle na `main`, envie ao GitHub e acompanhe o workflow do Pages até a URL responder com o novo site.

---

## Checkpoints de revisão

1. **Após Task 3:** fundação, tema e contrato editorial.
2. **Após Task 7:** caso integrador e módulos 1–3 com oficinas executáveis.
3. **Após Task 10:** módulos 4–6 e cadeia prática completa.
4. **Após Task 12:** recursos visuais e material docente local.
5. **Após Task 14:** auditoria, integração e publicação.
