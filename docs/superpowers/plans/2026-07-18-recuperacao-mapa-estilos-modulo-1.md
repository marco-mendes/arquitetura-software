# Recuperação do mapa e dos estilos do Módulo 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restaurar o mapa das quatro famílias e o aprofundamento de Camadas, Pipes and Filters e Microkernel sem ampliar a navegação do Módulo 1, deslocando o vocabulário preparatório para Referências.

**Architecture:** `conceitos.md` passa a começar pelos estilos e usa um SVG estático, responsivo e acessível para o mapa das famílias. `padroes-e-decisoes.md` torna-se a página de aprofundamento dos três estilos. Um glossário expandido e o apêndice `como-ler-uma-arquitetura.md` armazenam o vocabulário e as duas representações preparatórias fora do fluxo da aula.

**Tech Stack:** Markdown, SVG nativo, Material for MkDocs, CSS existente, unittest, validador editorial Python.

## Global Constraints

- Não criar páginas no Módulo 1; usar apenas as oito páginas já presentes na navegação.
- Criar o apêndice exclusivamente em Referência e acrescentá-lo à navegação dessa seção.
- O mapa das famílias não pode usar Mermaid `mindmap`; o SVG deve ser local, responsivo, ter `alt`, legenda, fonte e leitura textual.
- Manter números de figuras do Módulo 1 crescentes na ordem pública.
- Preservar os originais da raiz do repositório e não expor a matriz editorial interna.
- Reescrever o conteúdo para o curso; não copiar literalmente os arquivos `1.1` a `1.4`.

---

### Task 1: Mover o vocabulário preparatório para Referências

**Files:**
- Create: `docs/referencia/como-ler-uma-arquitetura.md`
- Modify: `docs/referencia/glossario.md`
- Modify: `docs/modulo-1-visao-geral/conceitos.md`
- Modify: `mkdocs.yml`
- Modify: `tests/test_module_one.py`
- Modify: `tests/test_content_contract.py`

**Interfaces:**
- Consumes: os conceitos iniciais e as Figuras 1 e 2 de `docs/modulo-1-visao-geral/conceitos.md`.
- Produces: uma página em Referência, linkada como `referencia/como-ler-uma-arquitetura.md`, e um `conceitos.md` que inicia em `## Estilos arquiteturais`.

- [ ] **Step 1: Escrever testes vermelhos para a separação de fluxo**

```python
def test_module_one_begins_with_architectural_styles(self):
    text = (MODULE / "conceitos.md").read_text(encoding="utf-8")
    self.assertEqual("# Conceitos: estilos arquiteturais", text.splitlines()[0])
    self.assertNotIn("## O que torna uma decisão arquitetural", text)

def test_reference_appendix_preserves_how_to_read_architecture(self):
    appendix = ROOT / "docs/referencia/como-ler-uma-arquitetura.md"
    text = appendix.read_text(encoding="utf-8")
    for term in ("Componente", "Conector", "Configuração", "Estrutura", "comportamento"):
        self.assertIn(term, text)
    self.assertEqual(2, text.count("```mermaid"))
```

Run: `python -m unittest tests.test_module_one -v`

Expected: FAIL porque o apêndice ainda não existe e a página de conceitos começa por decisões.

- [ ] **Step 2: Criar o apêndice e expandir o glossário**

Em `docs/referencia/como-ler-uma-arquitetura.md`, migrar e reescrever as duas figuras existentes: componentes/conectores/configuração e sequência de comportamento. Cada Mermaid deve ficar imediatamente seguido de `**Texto alternativo:**`, legenda `*Figura N — ... Fonte: curso.*` e `**Leitura textual da figura:**`.

Em `docs/referencia/glossario.md`, acrescentar verbetes curtos para `Decisão arquitetural`, `Restrição`, `Premissa`, `Configuração` e `Visão arquitetural`. Refinar os verbetes existentes apenas para manter terminologia consistente.

Remover de `conceitos.md` os blocos introdutórios que migrarem e alterar o título para `# Conceitos: estilos arquiteturais`.

- [ ] **Step 3: Conectar a página à Referência e proteger contratos**

Adicionar ao bloco `Referência` em `mkdocs.yml`:

```yaml
      - Como ler uma arquitetura: referencia/como-ler-uma-arquitetura.md
```

Adicionar um teste de navegação em `tests/test_content_contract.py` que assegure a presença de `referencia/como-ler-uma-arquitetura.md` no `nav` e mantenha o contrato de oito páginas de cada módulo.

- [ ] **Step 4: Executar a verificação focal e commitar**

Run:

```bash
python -m unittest tests.test_module_one tests.test_content_contract -v
python scripts/validate_content.py --module modulo-1-visao-geral
```

Expected: todos os testes passam e o validador não reporta links ou figuras inválidos.

```bash
git add docs/referencia docs/modulo-1-visao-geral/conceitos.md mkdocs.yml tests/test_module_one.py tests/test_content_contract.py
git commit -m "docs: move architecture reading concepts to references"
```

### Task 2: Restaurar o mapa das quatro famílias sem Mermaid mindmap

**Files:**
- Create: `docs/assets/images/m01-familias-arquiteturais.svg`
- Modify: `docs/modulo-1-visao-geral/conceitos.md`
- Modify: `tests/test_module_one.py`

**Interfaces:**
- Consumes: a lista de famílias e estilos definida em `1.1 Mapa e Estilos de Backend.md`.
- Produces: Figura 1 do Módulo 1 como SVG local e um texto de famílias que antecede a comparação de estilos.

- [ ] **Step 1: Escrever teste vermelho para o novo mapa**

```python
def test_module_one_uses_accessible_static_family_map_not_mermaid_mindmap(self):
    text = (MODULE / "conceitos.md").read_text(encoding="utf-8")
    self.assertIn("m01-familias-arquiteturais.svg", text)
    self.assertNotIn("mindmap", text)
    for family in (
        "Organização interna",
        "Decomposição por domínio",
        "Integração e comunicação",
        "Execução e operação",
    ):
        self.assertIn(family, text)
```

Run: `python -m unittest tests.test_module_one.ModuleOneTest.test_module_one_uses_accessible_static_family_map_not_mermaid_mindmap -v`

Expected: FAIL porque o mindmap ainda é usado.

- [ ] **Step 2: Criar o SVG estático e substituir o mindmap**

Criar `m01-familias-arquiteturais.svg` com um título central curto e quatro cartões, sem conectores passando por texto. Cada cartão deve listar uma pergunta orientadora e seus estilos principais. Usar a paleta Academia e `viewBox` para resposta em telas pequenas.

Substituir o bloco Mermaid em `conceitos.md` pela imagem, com texto alternativo, legenda, fonte e leitura textual. Reordenar as figuras seguintes do módulo para preservar numeração crescente.

Restaurar os quatro blocos narrativos de família, cada um contendo problema, ideia de organização, estilos abrangidos, quando ajuda e limite; inserir links para as unidades futuras ou para as âncoras de `padroes-e-decisoes.md`.

- [ ] **Step 3: Proteger a figura e a ordem de leitura**

Estender `tests/test_module_one.py` para conferir que o SVG existe, possui `viewBox`, não usa script externo e que `conceitos.md` contém texto alternativo, legenda e leitura textual para ele. Atualizar o teste de números de figuras para a nova sequência.

- [ ] **Step 4: Verificar e commitar**

Run:

```bash
python -m unittest tests.test_module_one -v
python scripts/validate_content.py --module modulo-1-visao-geral
python -m mkdocs build --strict
```

Expected: testes e build passam sem mindmap no material publicado.

```bash
git add docs/assets/images/m01-familias-arquiteturais.svg docs/modulo-1-visao-geral/conceitos.md tests/test_module_one.py
git commit -m "docs: restore the architectural style family map"
```

### Task 3: Ampliar as seções de estilos na página de decisões

**Files:**
- Modify: `docs/modulo-1-visao-geral/padroes-e-decisoes.md`
- Modify: `docs/modulo-1-visao-geral/conceitos.md`
- Modify: `docs/modulo-1-visao-geral/exemplo-arquitetural.md`
- Modify: `tests/test_module_one.py`

**Interfaces:**
- Consumes: os materiais `1.2 Estilo em Camadas.md`, `1.3 Pipes-filters.md` e `1.4 Micro-kernel.md`.
- Produces: âncoras públicas `#camadas`, `#pipes-and-filters` e `#microkernel`, conectadas a conceitos e exemplo arquitetural.

- [ ] **Step 1: Escrever teste vermelho de aprofundamento por estilo**

```python
def test_decision_page_restores_the_three_style_deep_dives(self):
    text = (MODULE / "padroes-e-decisoes.md").read_text(encoding="utf-8")
    expected = {
        "Camadas": ("camada fechada", "camada aberta", "sumidouro", "OCP", "MVC"),
        "Pipes and Filters": ("filtro sem estado", "filtro com estado", "rejeição", "ordenação", "throughput"),
        "Microkernel": ("registro", "contrato de extensão", "compatibilidade", "core creep", "plugin"),
    }
    for heading, terms in expected.items():
        section = text.split(f"## {heading}", 1)[1]
        for term in terms:
            self.assertIn(term, section)
```

Run: `python -m unittest tests.test_module_one.ModuleOneTest.test_decision_page_restores_the_three_style_deep_dives -v`

Expected: FAIL porque os termos e a estrutura aprofundada ainda não coexistem nas seções.

- [ ] **Step 2: Reescrever as três seções como aprofundamentos autônomos**

Usar títulos `## Camadas {#camadas}`, `## Pipes and Filters {#pipes-and-filters}` e `## Microkernel {#microkernel}`. Em cada seção, apresentar mecanismo, regras ou contrato, variações, forças, limites, critérios de uso e uma ligação direta com o caso hospitalar. Manter ou ampliar os Mermaid apenas quando ajudarem a explicar dependências, pipeline ou plugins; cada um deve seguir o contrato editorial de acessibilidade.

- [ ] **Step 3: Criar ligações de retorno a partir de conceitos e exemplo**

Em `conceitos.md`, ligar cada um dos três estilos à sua âncora. Em `exemplo-arquitetural.md`, acrescentar links de “aprofundar a decisão” nas subseções de Agenda, Faturamento e Triagem. Usar caminhos relativos válidos:

```markdown
[Aprofundar Camadas](padroes-e-decisoes.md#camadas)
[Aprofundar Pipes and Filters](padroes-e-decisoes.md#pipes-and-filters)
[Aprofundar Microkernel](padroes-e-decisoes.md#microkernel)
```

- [ ] **Step 4: Executar verificações completas e commitar**

Run:

```bash
python -m unittest tests.test_module_one tests.test_content_contract -v
python scripts/validate_content.py --module modulo-1-visao-geral
python -m mkdocs build --strict
git diff --check
```

Expected: testes, validador, build e verificação de espaços passam.

```bash
git add docs/modulo-1-visao-geral tests/test_module_one.py
git commit -m "docs: restore module one style deep dives"
```

### Task 4: Auditoria editorial final da recuperação

**Files:**
- Modify as needed: arquivos identificados pela auditoria.

**Interfaces:**
- Consumes: material recuperado nas Tasks 1 a 3.
- Produces: página de conceitos conectada, referências disponíveis e figuras sem o mindmap instável.

- [ ] **Step 1: Executar a barreira de regressão**

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_content.py --all
python -m mkdocs build --strict
git diff --check
```

Expected: todos os testes passam; nenhuma página pública expõe rótulos internos; não há links ou âncoras inválidos.

- [ ] **Step 2: Fazer inspeção editorial dirigida**

Verificar em sequência que: a primeira seção de `conceitos.md` é o mapa de estilos; as quatro famílias possuem problema, usos e limites; a Figura do mapa não é Mermaid; Camadas, Pipes and Filters e Microkernel possuem conteúdo aprofundado e links a partir do exemplo; o apêndice contém as duas representações removidas do módulo; e o glossário contém os cinco novos verbetes.

- [ ] **Step 3: Commit de qualquer correção factual encontrada**

```bash
git add docs tests mkdocs.yml
git commit -m "docs: finalize module one style map recovery"
```

Somente criar esse commit se a auditoria encontrar e corrigir uma divergência; caso contrário, não criar commit vazio.

## Self-review

- A separação de vocabulário está coberta pela Task 1.
- O SVG e as quatro famílias estão cobertos pela Task 2.
- Os três aprofundamentos, âncoras e ligações do exemplo estão cobertos pela Task 3.
- Navegação, contratos, build e links são cobertos em todas as tarefas e repetidos na Task 4.
- Não há `TODO`, conteúdo implícito ou criação de páginas adicionais no Módulo 1.
