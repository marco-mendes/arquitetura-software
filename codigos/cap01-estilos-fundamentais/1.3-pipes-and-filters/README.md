# 1.3 — Pipes and Filters: Pipeline de Triagem de Currículos

Demonstração completa do estilo Pipes and Filters aplicado a um pipeline
de triagem de candidatos para vaga de Engenheiro Backend.

## Conceitos demonstrados

- **Framework reutilizável:** classes abstratas `Filtro` e `Pipeline`
- **Os 4 tipos de filtro** (Richards & Ford): Producer, Tester, Transformer, Consumer
- **Statelessness:** cada filtro é independente e não compartilha estado
- **Composição:** o pipeline é montado em `main.py` sem alterar os filtros

## Execução

```bash
python main.py
```

Sem dependências externas — apenas Python 3.10+.

## Estrutura

```
framework.py          ← Filtro (ABC) + Pipeline
dominio.py            ← Curriculo, Vaga, ResultadoTriagem
filtros/
  producer.py         ← LeitorDeCurriculos (Producer)
  testers.py          ← Validador, FiltroPorExperiencia, FiltroPorPretensao (Testers)
  transformers.py     ← Normalizador, CalculadorDeScore (Transformers)
  consumer.py         ← RelatorioDeTriagem (Consumer)
main.py               ← Composição do pipeline + dados de entrada
```

## Saída esperada

6 currículos processados → 3 descartados (dados inválidos, experiência insuficiente,
pretensão acima do orçamento) → 3 aprovados ordenados por score de aderência.
