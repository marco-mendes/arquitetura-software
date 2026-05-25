# 1.4 — MicroKernel: Sistema de Faturamento Multi-Estado

Demonstração completa do estilo MicroKernel aplicado a um sistema de
faturamento que emite notas com regras fiscais que variam por estado.

## Conceitos demonstrados

- **Os 3 componentes** (Richards & Ford): Core System, Plugin Registry, Plugin Contract
- **Contrato via Protocol:** `PluginFaturamento` define a interface; o núcleo não
  conhece as implementações concretas
- **Extensão sem modificação:** novo estado (MG) adicionado em `main.py` sem
  alterar `CoreFaturamento` ou qualquer plugin existente
- **Registro dinâmico:** plugins são registrados por categoria em tempo de execução

## Execução

```bash
python main.py
```

Sem dependências externas — apenas Python 3.10+.

## Estrutura

```
dominio.py             ← Fatura, Cliente, ItemFatura, ResultadoEmissao
nucleo.py              ← PluginFaturamento (Protocol), PluginRegistry, CoreFaturamento
plugins/
  impostos_sp.py       ← ImpostoSPPlugin (ICMS) + ISSSPPlugin
  impostos_rj.py       ← ImpostoRJPlugin (ICMS RJ)
  frete.py             ← FreteCorrespondenciaPlugin
  notificacao.py       ← NotificacaoEmailPlugin
main.py                ← Configuração + 4 cenários de emissão
```

## Saída esperada

4 faturas emitidas: SP (ICMS + ISS + frete), RJ (ICMS flat), SP grande (frete grátis),
MG (plugin adicionado em tempo de execução sem modificar o núcleo).
