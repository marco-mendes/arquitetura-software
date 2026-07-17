# Critérios de avaliação

A entrega é avaliada como uma arquitetura acumulada, não como seis pastas independentes. Os critérios abaixo somam 100% e orientam tanto a revisão entre encontros quanto a apresentação final.

| Critério | Peso |
| --- | ---: |
| Coerência | 20% |
| Decisões e trade-offs | 20% |
| Contratos e integrações | 15% |
| Dados e eventos | 15% |
| Governança e operação | 15% |
| Clareza e evidências | 15% |

## Como interpretar

### Coerência

Contexto, capacidades, limites, diagramas, contratos e implantação contam a mesma história. Mudanças entre incrementos são refletidas nos artefatos relacionados e não deixam versões incompatíveis sem explicação.

### Decisões e trade-offs

As escolhas partem de forças e cenários de qualidade, com alternativas reais e consequências favoráveis e desfavoráveis. ADRs registram suposições, riscos aceitos e gatilhos de revisão.

### Contratos e integrações

APIs e integrações com plano de saúde, operadora e laboratório preservam significado, identidade, erros, idempotência, correlação e evolução. Exemplos e testes sustentam o comportamento declarado.

### Dados e eventos

Propriedade, acesso, consistência, retenção e reconciliação são explícitos. Eventos representam fatos, têm produtores e consumidores conhecidos e tratam repetição, ordenação e falha.

### Governança e operação

Políticas podem ser aplicadas e verificadas. Logs, métricas, rastros, alertas, modos degradados e procedimentos de recuperação respondem aos cenários priorizados.

### Clareza e evidências

A entrega pode ser compreendida por alguém que não participou do grupo. Evidências são reproduzíveis, ligadas a decisões e honestas sobre limitações.

## Escala comum de julgamento

- **Atende plenamente:** a relação entre contexto, decisão, consequência e evidência está explícita e consistente.
- **Atende parcialmente:** a decisão aparece, mas faltam conexão, consequência ou verificação suficiente.
- **Ainda não atende:** há afirmação ou artefato isolado sem justificativa verificável, ou existem contradições relevantes.

Use essa escala em cada critério e registre a evidência que sustenta o julgamento. A qualidade visual ajuda a leitura, mas não substitui conteúdo arquitetural coerente.
