# Task 9 — Correção da revisão editorial

## Correções

- `self_contained_activity_errors()` agora exige conteúdo em cada um dos nove
  campos e verifica caminho de artefato, estado inicial, ação enumerada,
  evidência observável e contingência. Os testes cobrem campo vazio, roteiro
  insuficiente, ordem inválida e roteiro válido.
- As quatro atividades avançadas dos módulos 5 e 6 agora identificam os
  artefatos locais, caminhos relativos à raiz, estado inicial, manipulação,
  saída a guardar e desvio seguro.
- Mermaid público recebe regras efetivas para `.md-typeset .mermaid` e seu
  SVG, com largura máxima, altura proporcional e rolagem horizontal.
- A oficina do módulo 3 substitui as repetições de “Antes deste Compose” por
  uma tabela de transição que preserva estado, evidência e contingência.

## Verificação

Executados após as alterações:

| Comando | Resultado |
| --- | --- |
| `python -m unittest tests.test_editorial_recovery tests.test_content_contract -v` | aprovado |
| `python scripts/validate_content.py --all` | sem erros |
| `python -m mkdocs build --strict` | aprovado |
| `git diff --check` | sem erros |
