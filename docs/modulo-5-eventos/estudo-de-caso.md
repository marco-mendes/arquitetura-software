# Estudo de caso: resultado, faturamento e tempo de convergência

## Situação

A plataforma hospitalar fictícia começou com uma chamada síncrona: quando o laboratório marcava um resultado como disponível, chamava Faturamento; depois Faturamento chamava Notificação. Em horário de pico, uma lentidão na cobrança fazia Resultados aguardar. Uma indisponibilidade transitória devolvia erro ao fluxo clínico apesar de o resultado estar pronto. Para evitar perda, uma pessoa passou a repetir manualmente chamadas e apareceu cobrança duplicada. O problema não era apenas a tecnologia da chamada: as responsabilidades e falhas estavam misturadas.

A primeira proposta foi “usar Kafka para tudo”. Ela trazia palavras atraentes — escala, replay, log — mas não respondia sobre dados, consumidores, ordem e operação. A segunda proposta foi um broker RabbitMQ local com uma única fila de Faturamento. Ela não resolveu o hospital inteiro, mas permitiu perguntar o necessário: o que ocorreu, quem reage, que atraso é aceitável e como uma repetição não cria duas cobranças? A escolha inicial foi RabbitMQ porque a necessidade imediata era roteamento de trabalho para um consumidor, demonstração de confirmações e DLQ, sem um requisito de replay de muitos fluxos.

## Decisão e consequências

Resultados publicou o fato `ResultadoLaboratorialDisponibilizado.v1` no tópico `hospital.events`. O fato levava referência, não laudo. Faturamento criou a fila `billing.resultados.v1` e assumiu ownership de sua política de retry, store idempotente e DLQ. Notificação não foi conectada no primeiro incremento, mas o tópico permitia adicionar uma fila própria sem editar Resultados. A disponibilidade do resultado passou a não depender da resposta de Faturamento; a cobrança passou a poder ficar pendente por um intervalo explícito.

Essa é consistência eventual. A interface que mostra o exame não pode afirmar “cobrado” imediatamente apenas porque o fato foi publicado. Ela pode informar que o resultado está disponível e que a atualização administrativa está em processamento, se essa informação for útil e autorizada. Operação acompanha idade da mensagem mais antiga, tamanho da fila, taxa de rejeição e quantidade na DLQ. Uma fila vazia não demonstra que todos os efeitos foram corretos; uma fila crescente é sinal para investigar capacidade, dependência ou contrato.

## Incidente: duplicidade de entrega

Em um teste de falha, Faturamento escreveu sua cobrança, mas caiu antes de confirmar a mensagem. RabbitMQ a entregou de novo após o consumidor retornar. Um handler que executava `INSERT` sem chave única faria duas cobranças. A correção não foi tentar desativar redelivery: isso aumentaria risco de perda. O consumidor passou a usar `event_id` como chave de deduplicação e a gravar, na mesma transação local, uma tentativa e o efeito.

Na repetição, a linha já existia. O handler registrou tentativa dois e confirmou a mensagem sem inserir novo efeito. A equipe passou a diferenciar “tentativas” de “cobranças”: duas tentativas podem ser evidência de disponibilidade parcial; uma cobrança é o efeito que não deve duplicar. Essa nomenclatura melhora a conversa com negócio e operação, porque não transforma uma propriedade de transporte em promessa de faturamento.

## Incidente: evolução incompatível

Mais tarde, uma integração enviou evento sem `result_reference`. O schema Pydantic recusou o corpo, o consumidor não deu ack e a mensagem chegou à DLQ. Uma resposta apressada seria mudar o consumidor para inventar uma referência. Isso ocultaria o contrato rompido e poderia associar cobrança ao recurso errado. A equipe identificou o producer, corrigiu a versão que gerava o evento e decidiu o destino das mensagens já paradas. As mensagens sintéticas foram removidas após registrar a causa; uma ocorrência real exigiria procedimento de reconciliação e proteção de dados.

Em seguida surgiu a necessidade de acrescentar uma referência administrativa. Antes de mudar, a equipe verificou consumidores e definiu campo opcional em uma evolução compatível, exemplo de payload e prazo para tornar a informação obrigatória. Se a semântica de referência mudasse, criaria `v2` e manteria publicação dupla por prazo curto e medido. Versionamento é um acordo social apoiado por ferramentas, não apenas um sufixo.

## Quando Kafka vira extensão plausível

Se o hospital precisar manter um fluxo de eventos por período definido para que Analytics, qualidade e um novo consumidor façam replay independente, Kafka pode se tornar uma alternativa a avaliar. O design começaria por tópicos, chaves de partição, retenção, grupos de consumidores e classificação de dados. Faturamento ainda precisaria deduplicar efeitos externos e escolher uma chave de ordenação por exame ou conta. A existência de replay não dá autorização para reter dados sem política, nem corrige payload mal versionado.

Uma alternativa híbrida também pode ser razoável: um log para eventos de integração e uma fila para unidades de trabalho internas. Mas cada ponte precisa de owner, observabilidade e recuperação. Não é uma evolução obrigatória do RabbitMQ; é uma decisão nova, motivada por requisitos de leitura e retenção que o caso demonstra ou mede.

## Perguntas para a decisão

Que diferença o usuário percebe entre “resultado disponível” e “cobrança concluída”? Qual atraso administrativo é aceitável e como ele aparece? Quais campos são estritamente necessários no evento? Qual efeito deve ser único e por qual identidade? O que fazer quando a mesma mensagem chega depois de uma atualização mais nova? Quem acompanha a DLQ e em quanto tempo? Ao responder, a equipe transforma uma escolha de broker em uma arquitetura com consequência verificável.
