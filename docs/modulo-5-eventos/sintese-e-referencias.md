# Síntese e referências

## Síntese para revisão

Eventos conectam capacidades por fatos em vez de chamadas em cadeia. Um evento bem nomeado afirma passado; um comando pede ação; mensagem é o envelope técnico. Broker distribui e retém conforme sua tecnologia; mediator coordena uma conversa e assume decisão explícita. Fila serve bem para trabalho pendente; tópico distribui para interesses independentes; log distribuído adiciona retenção e posições de leitura. Nenhum desses conceitos torna as regras de domínio responsabilidade da infraestrutura.

Uma integração robusta declara entrega pelo menos uma vez e responde com idempotência. A identidade da ocorrência, a transação local do consumidor e uma chave única para o efeito são mais úteis que uma promessa ampla de ausência de repetição. Ordem precisa de escopo e chave; consistência eventual precisa de uma experiência e um tempo de convergência aceitáveis. Schema e evolução tornam o contrato verificável; DLQ conserva uma falha para análise sem resolvê-la automaticamente.

RabbitMQ e Kafka não são degraus de maturidade. RabbitMQ oferece exchanges, filas e confirmações que atendem bem ao laboratório de Faturamento. Kafka organiza logs particionados, retenção e offsets, úteis quando replay e múltiplas leituras independentes são requisitos reais. Ambos pedem operação, segurança, observabilidade e testes. A decisão começa pelo problema e pelas evidências; taxa genérica e promessa de exactly-once não bastam.

## Fontes públicas para aprofundar

- [RabbitMQ Tutorials e documentação de consumidores](https://www.rabbitmq.com/tutorials) explicam confirmações, filas e padrões AMQP.
- [RabbitMQ: dead lettering](https://www.rabbitmq.com/docs/dlx) detalha causas e configuração de dead-letter exchange.
- [Apache Kafka: introdução](https://kafka.apache.org/intro) apresenta tópicos, partições, retenção e grupos de consumidores.
- [Apache Kafka: semântica de entrega](https://kafka.apache.org/documentation/#semantics) descreve limites e mecanismos de processamento.
- [CloudEvents specification](https://github.com/cloudevents/spec) oferece uma referência aberta para metadados de eventos; adotar o formato ainda exige uma decisão de contrato.
- [Martin Kleppmann, *Designing Data-Intensive Applications*](https://dataintensive.net/) aprofunda logs, replicação, ordenação e sistemas distribuídos.

## Perguntas de saída

Antes de encerrar uma decisão, responda: o evento descreve fato ou esconde um comando? Qual é a unidade de ordem que importa? Qual identidade impede um segundo efeito? Onde uma mensagem inválida fica visível? O que pode convergir depois e como o usuário sabe disso? Qual mudança de contrato é compatível? Se a resposta não aparecer no desenho, código, configuração ou evidência operacional, a integração ainda depende de suposições frágeis.
