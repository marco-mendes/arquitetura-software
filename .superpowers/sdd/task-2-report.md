# Relatório — Task 2

## Resultado

- Substituído o mindmap Mermaid da Figura 1 por `docs/assets/images/m01-familias-arquiteturais.svg`, um ativo SVG local com `viewBox`, título, descrição e quatro cartões estáveis na paleta Academia.
- A imagem apresenta as famílias Organização interna, Decomposição por domínio, Integração e comunicação e Execução e operação, cada uma com pergunta orientadora e estilos principais, sem conectores sobre o texto.
- `conceitos.md` agora fornece texto alternativo na imagem, legenda, fonte e leitura textual imediatamente após a figura.
- Foram restaurados quatro blocos didáticos com problema, ideia de organização, estilos abrangidos, quando ajuda e limite, ligados às unidades futuras e às decisões desta unidade.
- A numeração global do Módulo 1 continua em leitura crescente de Figura 1 a Figura 9; a cobertura que considera apenas Mermaid foi atualizada de quatro para três figuras.

## TDD

- RED: `python -m unittest tests.test_module_one.ModuleOneTest.test_module_one_uses_accessible_static_family_map_not_mermaid_mindmap -v` falhou porque o material ainda referenciava o mindmap e não tinha o SVG.
- GREEN: o teste passou após a criação do ativo, a substituição da figura e a cobertura de acessibilidade do SVG.

## Verificação

- `python -m unittest tests.test_module_one -v` — 23 testes aprovados.
- `python scripts/validate_content.py --module modulo-1-visao-geral` — validação concluída sem erros.
- `python -m mkdocs build --strict` — build concluído; apenas os avisos preexistentes do Material for MkDocs e do arquivo `assets/images/prompts.md` fora da navegação.
- `git diff --check` — sem erros de whitespace.

## Commit

- `b3a9014 docs: restore the architectural style family map`

## Apêndice — correções P1/P2

- A família **Decomposição por domínio** agora inclui macrosserviços, e **Execução e operação** inclui orquestração e serverless no SVG, no texto alternativo, na leitura textual, na tabela e nas narrativas correspondentes. Os rótulos do SVG foram distribuídos em linhas curtas para manter os cartões legíveis.
- A narrativa de Integração e comunicação agora aponta para [Pipes and Filters](../../docs/modulo-1-visao-geral/padroes-e-decisoes.md#pipes-and-filters), cuja seção possui a âncora explícita `{#pipes-and-filters}`. Os links existentes de Camadas e Microkernel foram preservados.
- A regressão em `tests/test_module_one.py` cobre os três termos em todas as representações do mapa e confirma o link local e sua âncora.

### Verificação da correção

- `python -m unittest tests.test_module_one -v` — 24 testes aprovados.
- `python scripts/validate_content.py --module modulo-1-visao-geral` — validação concluída sem erros.
- `mkdocs build --strict` — build concluído; apenas os avisos preexistentes do Material for MkDocs e do arquivo `assets/images/prompts.md` fora da navegação.
- `git diff --check` — sem erros de whitespace.
