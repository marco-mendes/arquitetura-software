# Exercícios: tornar políticas governáveis

As atividades percorrem a Taxonomia de Bloom e exigem premissas explícitas. Não existe desenho único: use os fatos do caso, declare incertezas e mostre como a proposta seria verificada. Todas as atividades pedem uma entrega autocontida, sem depender de console manual.

## Recordar

### Inventariar a linguagem de governança

**Situação**

Uma equipe recebeu o repositório da plataforma hospitalar e encontrou rota pública, serviço, Collector e Jaeger, mas não sabe nomear o papel de cada elemento.

**Seu papel**

Você organiza um glossário inicial para a nova equipe.

**Insumos disponíveis**

Os arquivos `kong.yml`, `otel-collector.yml`, Compose e este módulo; nenhuma informação adicional de produção.

**Como conduzir**

1. Defina governança, política, ownership, catálogo e versionamento.
2. Diferencie logs, métricas e traces por pergunta respondida.
3. Defina SLO, correlation ID, trace ID e rate limiting.
4. Relacione cada termo a um artefato do laboratório.

**Entrega esperada**

Um glossário de uma página com uma definição, um exemplo e uma evidência para cada termo.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Definições precisas | 35% |
| Relação com artefatos | 35% |
| Distinção entre sinais | 30% |

## Compreender

### Explicar a fronteira de responsabilidade

**Situação**

Uma pessoa propõe implementar no gateway a regra “beneficiário com plano vencido não pode solicitar exame”, porque a entrada já conhece a rota.

**Seu papel**

Você explica a fronteira sem rejeitar a preocupação com segurança.

**Insumos disponíveis**

A rota pública, o serviço Elegibilidade, banco próprio e a política de correlação e limite da oficina.

**Como conduzir**

1. Descreva o objetivo técnico do gateway.
2. Localize a regra de plano vencido e justifique.
3. Identifique duas políticas adequadas à borda.
4. Explique como os sinais operacionais ajudam a investigar a decisão.

**Entrega esperada**

Uma nota para a equipe, com diagrama simples de responsabilidade e consequências da escolha.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Separação entre borda e domínio | 40% |
| Justificativa contextual | 30% |
| Uso correto de telemetria | 30% |

## Aplicar

### Publicar uma rota de resultado de exame

**Situação**

O serviço Resultados deve ganhar entrada pública. Ele contém dado de saúde, tem consumidor móvel autenticado e precisa de proteção contra picos. A regra de quem pode ler cada resultado depende de vínculo clínico e permanece no serviço.

**Seu papel**

Você prepara uma política inicial, declarada e testável.

**Insumos disponíveis**

Kong DB-less, Collector, Jaeger, um catálogo em Markdown e a convenção de correlation ID da oficina. O time ainda opera uma única réplica de gateway no ambiente de estudo.

**Como conduzir**

1. Escreva a entrada de catálogo com owner, contrato, consumidores e dados.
2. Proponha rota, chave de limite, janela e consequência de `429`.
3. Declare o que gateway faz e o que o serviço faz.
4. Desenhe um trace com gateway, serviço e dependência.
5. Descreva chamada e consulta de trace automatizáveis.
6. Registre uma condição que exigiria rever limite local.

**Entrega esperada**

Um arquivo de política, mapa de fluxo e roteiro de verificação com entradas e efeitos esperados.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Catálogo e ownership explícitos | 20% |
| Política de borda coerente | 25% |
| Regra de domínio preservada | 25% |
| Evidência de correlação e trace | 20% |
| Condição de revisão | 10% |

## Analisar

### Diagnosticar uma cadeia sem correlação

**Situação**

Atendimento relata que algumas consultas falham. Gateway registra `502`, Elegibilidade registra erro de banco e Jaeger contém traces sem nome consistente de serviço. Cada registro usa identificador diferente; a média de latência está estável.

**Seu papel**

Você analisa o incidente sem concluir causalidade além das evidências.

**Insumos disponíveis**

Três amostras de logs anonimizados, taxa de `5xx` por minuto, traces parciais e o arquivo de política atual.

**Como conduzir**

1. Separe fato, inferência e hipótese.
2. Mapeie lacunas de correlation ID e traceparent.
3. Explique por que média pode ocultar uma falha relevante.
4. Compare ao menos duas causas plausíveis.
5. Proponha alteração mínima em política, sinal e teste.
6. Indique qual dado adicional confirmaria ou enfraqueceria a hipótese.

**Entrega esperada**

Um diagnóstico com linha do tempo, mapa de evidências e plano de investigação seguro.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Separação de fato e hipótese | 25% |
| Leitura integrada dos sinais | 25% |
| Hipóteses alternativas | 20% |
| Mudança verificável proposta | 20% |
| Limites da conclusão | 10% |

## Avaliar

### Escolher uma política de limite

**Situação**

Um portal parceiro dispara lotes de consultas toda manhã. Limite por IP protege a infraestrutura, mas hospitais diferentes saem pelo mesmo proxy. Limite por credencial permite justiça maior, porém as credenciais ainda estão em transição. Recusar solicitações pode atrasar atendimento; aceitar tudo pode degradar todos os consumidores.

**Seu papel**

Você recomenda uma política temporária e condições de evolução.

**Insumos disponíveis**

Picos de 20 chamadas por segundo durante cinco minutos, capacidade atual de oito por segundo, consumidores identificados parcialmente, suporte em horário comercial e meta de latência para consultas aceitas.

**Como conduzir**

1. Compare IP, credencial e fila como chaves ou estratégias.
2. Avalie proteção, justiça, operação e risco de atraso.
3. Declare resposta para `429` e orientação a clientes.
4. Escolha indicador, SLO e sinal de revisão.
5. Registre impactos para owner, consumidores e plataforma.
6. Descreva experimento reversível antes de uso amplo.

**Entrega esperada**

Um registro de decisão com alternativas, decisão, consequências, evidências e plano de retorno.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Comparação equilibrada | 25% |
| Vínculo com capacidade e risco | 25% |
| SLO e sinais operacionais | 20% |
| Reversibilidade | 15% |
| Comunicação a consumidores | 15% |

## Criar

### Desenhar o mínimo de governança para agenda

**Situação**

Agenda será adicionada à plataforma. Ela consulta Elegibilidade, reserva horário e informa preparo de sala. O novo serviço terá owner próprio, uma API pública e integração com duas equipes. A primeira versão precisa começar localmente, mas sua governança não pode depender de memória informal.

**Seu papel**

Você cria um pacote de decisão para iniciar e evoluir o serviço.

**Insumos disponíveis**

Contrato de Elegibilidade, Compose da oficina, limite de três novas unidades implantáveis no semestre, dados sintéticos e objetivo de confirmação inicial em três segundos.

**Como conduzir**

1. Crie entrada de catálogo, ownership e classificação de dados.
2. Defina contrato e estratégia de versão.
3. Separe políticas de gateway, serviço e domínio.
4. Modele logs, métricas, traces e correlation ID.
5. Defina um SLO e seu orçamento de erro.
6. Descreva teste de rota, limite e propagação.
7. Inclua dois gatilhos que exigiriam revisão arquitetural.

**Entrega esperada**

Um pacote com ADR, diagrama, configuração declarativa ilustrativa, plano de sinais e roteiro de teste reproduzível.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Coerência entre ownership e contrato | 20% |
| Separação de políticas | 20% |
| Observabilidade verificável | 20% |
| SLO contextualizado | 15% |
| Testes reproduzíveis | 15% |
| Gatilhos de evolução | 10% |
