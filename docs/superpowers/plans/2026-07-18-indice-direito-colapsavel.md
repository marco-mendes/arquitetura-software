# Índice direito colapsável — plano de implementação

> **Para agentes:** HABILIDADE OBRIGATÓRIA: use `superpowers:subagent-driven-development` (recomendado) ou `superpowers:executing-plans` para implementar este plano tarefa a tarefa. Os passos usam checkboxes (`- [ ]`) para acompanhamento.

**Objetivo:** permitir que o índice à direita seja recolhido em desktop, mantendo-o aberto por padrão e preservando a escolha da pessoa estudante entre páginas.

**Arquitetura:** um módulo JavaScript próprio do portal será carregado pelo MKDocs depois da inicialização do Material. Ele observará `document$`, que também é emitido pela navegação instantânea, e inserirá um único botão em um contêiner próprio, fora do índice secundário. Uma classe na raiz do documento representa o estado; CSS no breakpoint desktop recolhe a coluna secundária e mantém uma alça compacta para restaurá-la. O estado será salvo em `localStorage`.

**Tecnologias:** Material for MkDocs, CSS, JavaScript ES modules, `localStorage`, Python `unittest` e MkDocs.

## Restrições globais

- O índice abre visível quando não houver preferência salva.
- O controle só aparece no breakpoint desktop de `76.25em` ou superior, onde o tema exibe o índice direito como coluna lateral.
- O botão deve usar texto em português, teclado nativo e `aria-expanded` correto.
- A preferência deve sobreviver à navegação instantânea e ao recarregamento.
- Não alterar conteúdo didático, navegação à esquerda, paleta, tipografia ou comportamento móvel.

---

### Task 1: Cobrir a extensão visual com testes editoriais

**Arquivos:**

- Modificar: `tests/test_visual_system.py`
- Consumido: `mkdocs.yml`, `docs/assets/stylesheets/extra.css` e o novo módulo de interface.
- Produz: testes que definem o contrato estático da integração com o tema.

- [ ] **Passo 1: escrever o teste que falha**

Acrescentar ao `VisualSystemTest` uma verificação que leia configuração, CSS e JavaScript e exija os marcadores públicos abaixo:

```python
def test_right_toc_can_be_collapsed_accessibly_on_desktop(self):
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")
    script = (ROOT / "docs/assets/javascripts/toc-toggle.mjs").read_text(
        encoding="utf-8"
    )

    self.assertIn("assets/javascripts/toc-toggle.mjs", navigation)
    self.assertIn("html.toc-collapsed .md-sidebar--secondary", css)
    self.assertIn("@media (min-width: 76.25em)", css)
    self.assertIn("academia-toc-toggle", script)
    self.assertIn("aria-expanded", script)
    self.assertIn("localStorage", script)
    self.assertIn("document$.subscribe", script)
```

- [ ] **Passo 2: executar o teste e confirmar a falha**

Executar:

```bash
python -m unittest tests.test_visual_system.VisualSystemTest.test_right_toc_can_be_collapsed_accessibly_on_desktop -v
```

Resultado esperado: falha porque `toc-toggle.mjs` ainda não existe e a configuração não o referencia.

- [ ] **Passo 3: confirmar a intenção do teste**

O teste não simula um navegador. Ele impede regressões nos quatro contratos que o build pode verificar: carregamento do módulo, seletor desktop, acessibilidade declarada e reinicialização após a navegação instantânea.

- [ ] **Passo 4: registrar o teste**

```bash
git add tests/test_visual_system.py
git commit -m "test: cobre índice direito colapsável"
```

### Task 2: Implementar controle acessível e layout recolhido

**Arquivos:**

- Criar: `docs/assets/javascripts/toc-toggle.mjs`
- Modificar: `docs/assets/stylesheets/extra.css`
- Modificar: `mkdocs.yml`
- Teste: `tests/test_visual_system.py`
- Consome: o elemento `.md-sidebar--secondary` do Material e o observável global `document$` já usado por `mermaid.mjs`.
- Produz: botão `#academia-toc-toggle`, classe `toc-collapsed` em `document.documentElement` e a chave `academia-toc-collapsed` no armazenamento local.

- [ ] **Passo 1: criar o módulo de comportamento**

Criar `docs/assets/javascripts/toc-toggle.mjs` com uma implementação que monte o botão dentro de `.md-content`, e não dentro de `.md-sidebar--secondary`; isso permite que a alça continue disponível quando o painel for ocultado. Ela deve retornar silenciosamente abaixo de `76.25em` e em páginas sem índice secundário, evitar duplicação após transição instantânea, restaurar a preferência e atualizar texto e atributo ARIA a cada alternância.

```javascript
const storageKey = "academia-toc-collapsed";
const collapsedClass = "toc-collapsed";

function preferenceIsCollapsed() {
  return window.localStorage.getItem(storageKey) === "true";
}

function updateButton(button, collapsed) {
  button.setAttribute("aria-expanded", String(!collapsed));
  button.setAttribute(
    "aria-label",
    collapsed ? "Mostrar índice" : "Recolher índice",
  );
  button.textContent = collapsed ? "Mostrar índice" : "Recolher índice";
}

function mountTocToggle() {
  const sidebar = document.querySelector(".md-sidebar--secondary");
  const content = document.querySelector(".md-content");
  const desktop = window.matchMedia("(min-width: 76.25em)").matches;
  if (!desktop || !sidebar || !content || document.querySelector("#academia-toc-toggle")) return;

  const button = document.createElement("button");
  button.id = "academia-toc-toggle";
  button.className = "academia-toc-toggle";
  button.type = "button";

  const collapsed = preferenceIsCollapsed();
  document.documentElement.classList.toggle(collapsedClass, collapsed);
  updateButton(button, collapsed);

  button.addEventListener("click", () => {
    const nextCollapsed = !document.documentElement.classList.contains(collapsedClass);
    document.documentElement.classList.toggle(collapsedClass, nextCollapsed);
    window.localStorage.setItem(storageKey, String(nextCollapsed));
    updateButton(button, nextCollapsed);
  });

  content.append(button);
}

document$.subscribe(mountTocToggle);
```

- [ ] **Passo 2: carregar o módulo**

Em `mkdocs.yml`, adicionar a entrada abaixo depois de `mermaid.mjs`, preservando a lista existente:

```yaml
extra_javascript:
  - assets/javascripts/mermaid.mjs
  - assets/javascripts/toc-toggle.mjs
```

- [ ] **Passo 3: adicionar as regras de apresentação**

Em `docs/assets/stylesheets/extra.css`, acrescentar regras após os estilos de acessibilidade. O botão tem o mesmo azul do sistema visual. Só em desktop a classe recolhe a coluna, mantém uma alça fixa na borda direita do conteúdo e deixa o flex layout nativo do Material usar a largura liberada; não configurar `.md-grid`, que não é a grade de layout do tema.

```css
.academia-toc-toggle {
  background: var(--academia-white);
  border: 1px solid rgb(37 77 184 / 28%);
  border-radius: 999px;
  color: var(--academia-cobalt);
  cursor: pointer;
  font: inherit;
  font-size: 0.75rem;
  font-weight: 700;
  margin: 0 0 var(--academia-space-3);
  padding: var(--academia-space-2) var(--academia-space-3);
}

.academia-toc-toggle:hover {
  background: var(--academia-surface);
}

@media (min-width: 76.25em) {
  html.toc-collapsed .md-sidebar--secondary {
    display: none;
  }

  .md-content {
    position: relative;
  }

  html.toc-collapsed .academia-toc-toggle {
    position: fixed;
    right: var(--academia-space-4);
    top: 50%;
    transform: translateY(-50%);
  }
}
```

- [ ] **Passo 4: executar o teste focal e a suíte visual**

Executar:

```bash
python -m unittest tests.test_visual_system.VisualSystemTest.test_right_toc_can_be_collapsed_accessibly_on_desktop -v
python -m unittest tests.test_visual_system -v
```

Resultado esperado: ambos aprovados.

- [ ] **Passo 5: registrar a implementação**

```bash
git add mkdocs.yml docs/assets/stylesheets/extra.css docs/assets/javascripts/toc-toggle.mjs tests/test_visual_system.py
git commit -m "feat: permite recolher índice direito"
```

### Task 3: Validar o portal completo

**Arquivos:**

- Verificar: todos os arquivos modificados nas Tarefas 1 e 2.

- [ ] **Passo 1: executar as verificações automatizadas**

```bash
python -m unittest discover -s tests -q
python scripts/validate_content.py --all
python -m mkdocs build --strict
git diff --check
```

Resultado esperado: testes, validação de conteúdo, build e verificação de espaços aprovados. O aviso externo do Material sobre versões futuras do MkDocs não bloqueia o build.

- [ ] **Passo 2: verificar manualmente em uma página de conteúdo**

Abrir uma página com títulos, como `modulo-1-visao-geral/conceitos/`, em viewport desktop. Confirmar: o índice abre visível; o botão recolhe o painel e amplia o conteúdo; o botão restaura o painel; ao abrir outro conteúdo, a escolha permanece. Reduzir a largura para viewport móvel e confirmar que nenhum botão adicional aparece.

- [ ] **Passo 3: registrar a evidência de conclusão**

Anotar no relatório de execução os comandos aprovados e a página usada na inspeção manual. Nenhum arquivo didático precisa ser alterado nesta tarefa.
