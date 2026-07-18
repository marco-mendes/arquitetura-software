# Oficina do Módulo 1 com códigos existentes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar a oficina da Unidade 1 em três experimentos executáveis com os exemplos reais de Camadas, Pipes and Filters e Microkernel.

**Architecture:** A página de oficina passa a ser o roteiro de entrada para os diretórios `codigos/cap01-estilos-fundamentais`, sem depender do laboratório hospitalar. Cada experimento identifica arquivos, caminhos locais, links GitHub, comando por plataforma, evidência, perguntas e extensão reversível.

**Tech Stack:** Markdown, Python 3.10+, MkDocs, unittest, validador editorial.

## Global Constraints

- Usar exclusivamente os três exemplos existentes sob `<raiz-do-clone>/codigos/cap01-estilos-fundamentais/`.
- Não usar `laboratorios/plataforma-hospitalar`, pytest, Podman, Docker ou Structurizr como prática principal da oficina.
- Declarar Python 3.10+ e comandos equivalentes para Windows, macOS e Linux.
- Cada experimento precisa de artefato, caminho, arquivos a abrir, pré-condição, comando, saída, observação e contingência.
- Links de código devem apontar para `https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/...`.
- Extensões ocorrem em cópias locais e são revertidas ao final; não há resposta canônica.

---

### Task 1: Reescrever a oficina pelos três exemplos reais

**Files:**
- Modify: `docs/modulo-1-visao-geral/oficina-de-ferramentas.md`
- Modify: `tests/test_module_one.py`

**Interfaces:**
- Consumes: `codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas`, `1.3-pipes-and-filters` e `1.4-microkernel`.
- Produces: uma prática de aproximadamente 120 minutos que executa `main.py` nos três diretórios e aponta para arquivos concretos.

- [ ] **Step 1: Escrever testes vermelhos de referências e exclusões**

```python
def test_workshop_uses_the_three_existing_chapter_one_examples(self):
    workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
    for path in (
        "codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas",
        "codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters",
        "codigos/cap01-estilos-fundamentais/1.4-microkernel",
    ):
        self.assertIn(path, workshop)
    self.assertNotIn("laboratorios/plataforma-hospitalar", workshop)
    self.assertNotIn("Structurizr", workshop)
    self.assertNotIn("Podman", workshop)

def test_workshop_links_each_style_to_real_chapter_one_source_files(self):
    workshop = (MODULE / "oficina-de-ferramentas.md").read_text(encoding="utf-8")
    for filename in (
        "apresentacao.py", "servicos.py", "dominio.py", "repositorios.py",
        "framework.py", "filtros/testers.py", "filtros/transformers.py",
        "nucleo.py", "plugins/impostos_sp.py", "plugins/frete.py",
    ):
        self.assertIn(filename, workshop)
    self.assertGreaterEqual(workshop.count("github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais"), 10)
```

Run: `python -m unittest tests.test_module_one -v`

Expected: FAIL porque a oficina ainda usa o laboratório hospitalar e não liga os arquivos do capítulo.

- [ ] **Step 2: Reescrever preparação e orientação de ambiente**

Substituir o material de instalação por uma preparação curta: o aluno abre a raiz `arquitetura-software`, confirma Python 3.10+ e não cria ambiente virtual. Incluir comandos:

```powershell
py --version
Set-Location codigos\cap01-estilos-fundamentais\1.2-estilo-em-camadas
py main.py
```

```bash
python3 --version
cd codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas
python3 main.py
```

Explicar que, se `py` ou `python3` não existir, o aluno instala Python 3.10+ pelo canal do sistema e repete a verificação; não incluir Podman, pacotes ou comandos de instalação de dependências.

- [ ] **Step 3: Criar os três experimentos essenciais**

Para Camadas, apresentar o diretório, os quatro links de arquivo e o comando `main.py`; orientar observação de agendamento e conflito. Para Pipes and Filters, apresentar `framework.py` e os quatro tipos de filtro; orientar observação de descarte, transformação e ranking. Para Microkernel, apresentar núcleo e plugins; orientar observação de ordem por categoria e contribuição de regras.

Cada experimento contém uma tabela com `O que abrir`, `O que executar`, `O que observar` e `Se algo sair diferente`, seguida de perguntas de exploração. Os links usam a URL exata do repositório e os caminhos locais usam `<raiz-do-clone>/codigos/...`.

- [ ] **Step 4: Acrescentar extensões reversíveis**

Em cada experimento, orientar o aluno a copiar o diretório para `<raiz-do-clone>/entregas/unidade-1/` antes de alterar uma condição, executar novamente, guardar saída antes/depois e excluir a cópia ou desfazer a mudança. As extensões pedem observação, não prescrevem uma alteração de código específica.

- [ ] **Step 5: Verificar e commitar**

Run:

```bash
python -m unittest tests.test_module_one -v
python scripts/validate_content.py --module modulo-1-visao-geral
python -m mkdocs build --strict
git diff --check
```

Expected: testes, validador, build e whitespace passam.

```bash
git add docs/modulo-1-visao-geral/oficina-de-ferramentas.md tests/test_module_one.py
git commit -m "docs: use chapter one examples in workshop"
```

### Task 2: Auditar a execução real dos exemplos e a clareza da oficina

**Files:**
- Modify as needed: `docs/modulo-1-visao-geral/oficina-de-ferramentas.md`, `tests/test_module_one.py`

**Interfaces:**
- Consumes: oficina reescrita e os três `main.py` sob `codigos/cap01-estilos-fundamentais`.
- Produces: roteiro que aponta apenas para comandos e saídas reais.

- [ ] **Step 1: Executar os três exemplos na raiz correta**

Run:

```bash
python3 codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/main.py
python3 codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/main.py
python3 codigos/cap01-estilos-fundamentais/1.4-microkernel/main.py
```

Expected: cada comando termina com código 0 e imprime evidência de agendamento/conflito, triagem/ranking e faturamento/plugins, respectivamente.

- [ ] **Step 2: Corrigir apenas divergências observadas**

Se um comando, arquivo ou saída citada pela oficina divergir da execução, atualizar a oficina com o nome e comportamento reais. Se os três comandos corresponderem ao roteiro, não alterar texto apenas por estilo.

- [ ] **Step 3: Executar a barreira do módulo e commitar apenas se necessário**

Run:

```bash
python -m unittest tests.test_module_one tests.test_content_contract -v
python scripts/validate_content.py --module modulo-1-visao-geral
python -m mkdocs build --strict
git diff --check
```

Expected: todos passam.

Se a auditoria corrigir uma divergência factual:

```bash
git add docs/modulo-1-visao-geral/oficina-de-ferramentas.md tests/test_module_one.py
git commit -m "docs: verify chapter one workshop execution"
```

Não criar commit vazio quando os comandos e o roteiro já estiverem alinhados.

## Self-review

- A Task 1 substitui toda a prática antiga pelos três diretórios e protege referências/links.
- A Task 2 confirma que o aluno pode executar cada `main.py` real e que as observações do texto correspondem à saída.
- O plano não modifica o código didático existente, apenas o utiliza e o referencia.
