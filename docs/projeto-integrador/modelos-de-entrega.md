# Modelos de entrega

Use estes modelos para manter rastreabilidade entre encontros. Cada item novo deve apontar para o contexto que o motivou e para a evidência que permite revisá-lo. Diagramas sem explicação e escolhas sem alternativas não formam uma decisão arquitetural completa.

## Cabeçalho da baseline

```text
Versão da baseline:
Incremento:
Data:
Responsáveis:
Mudanças desde a versão anterior:
Artefatos substituídos:
Riscos e suposições em aberto:
```

## Registro de decisão

Adote o [template de ADR](../referencia/template-adr.md) e mantenha um índice com estado, decisão, artefatos afetados e ADR substituto, quando houver. Uma decisão deve comparar alternativas pelas mesmas forças e declarar consequências favoráveis e desfavoráveis.

```text
Identificador e título:
Contexto e forças:
Alternativas comparadas:
Decisão e justificativa:
Consequências:
Evidências:
Gatilho de revisão:
```

Consulte o [catálogo de padrões](../referencia/catalogo-de-padroes.md) para reconhecer opções, sem usar o nome de um padrão como justificativa suficiente.

## Cenário de atributo de qualidade

A estrutura detalhada aparece em [atributos de qualidade](../referencia/atributos-de-qualidade.md).

```text
Atributo:
Fonte do estímulo:
Estímulo:
Ambiente:
Elemento afetado:
Resposta esperada:
Medida da resposta:
Evidência que será coletada:
```

Prefira medidas observáveis. “A solução deve ser rápida” não informa carga, ambiente, resposta nem limite aceitável.

## Contrato de integração

```text
Participantes e responsabilidade:
Capacidade atendida:
Operação, comando ou evento:
Dados obrigatórios e significado:
Identidade e autorização:
Resultado e estados de erro:
Limites de tempo e repetição:
Idempotência e correlação:
Compatibilidade e evolução:
Exemplos e teste de contrato:
```

O contrato deve distinguir erro de negócio, indisponibilidade temporária e mensagem inválida. Não inclua dados protegidos apenas por conveniência.

## Quadro de dados e eventos

| Informação ou evento | Responsável | Quem pode usar | Consistência necessária | Retenção ou descarte | Recuperação e reconciliação |
| --- | --- | --- | --- | --- | --- |
| Exemplo preenchido pela equipe | Capacidade responsável | Participantes autorizados | Justificativa do nível escolhido | Regra adotada | Processo observável |

## Evidência reproduzível

Use as ferramentas apropriadas listadas no [guia de ferramentas](../referencia/guia-de-ferramentas.md), sempre relacionando execução e decisão.

```text
Decisão ou cenário verificado:
Ambiente e pré-requisitos:
Comando ou procedimento:
Entrada controlada:
Resultado esperado:
Resultado observado:
Local dos registros, métricas ou rastros:
Limitações da evidência:
```

Uma captura isolada pode ilustrar o resultado, mas a entrega precisa permitir que outra pessoa repita a verificação.

## Lista de consistência antes da entrega

- Os nomes de capacidades, atores e estados são iguais entre texto, contrato e diagrama.
- Cada ADR aponta para forças do contexto e para artefatos afetados.
- Dados e eventos têm responsável e regras de acesso explícitos.
- Falhas externas têm estado observável, recuperação e correlação.
- Evidências indicam procedimento, resultado esperado e limitação.
- Mudanças em decisões anteriores aparecem no histórico da baseline.
