# Estudo de caso: a janela de agendamento e o pico previsível

## Situação

Toda segunda-feira, às 7h, parceiros consultam elegibilidade antes de liberar agendas de exame. O volume normal é baixo, mas a janela de vinte minutos produz picos. Na última ocorrência, usuários receberam respostas lentas, e a equipe concluiu que “precisa de nuvem”. Essa frase ainda não distingue fatos de hipóteses. Os sinais disponíveis são: latência p95 da API, taxa de respostas 5xx, uso de CPU, memória, conexões do serviço de elegibilidade e idade das requisições pendentes. Não há dado clínico no exercício.

O primeiro diagnóstico separa camadas. Se CPU da API fica baixa e o tempo da dependência externa aumenta, aumentar Pods não resolve a causa. Se os Pods atingem request de CPU, têm filas de entrada e a dependência preserva folga, uma escala horizontal pode ajudar. Se uma única instância perde sessão em memória, o problema é stateful e precisa de um estado compartilhado antes de escalar. A decisão é uma hipótese testável: gerar carga sintética, observar limites e registrar a mudança.

## Alternativas

| Alternativa | Quando faz sentido | Benefício | Risco ou custo |
| --- | --- | --- | --- |
| VMs em IaaS com autoscaling | equipe opera SO e rede | controle de runtime e rede | patches, imagens de VM e operação própria |
| runtime PaaS para API stateless | contrato de deploy atende à plataforma | reduz trabalho de host e escala | limites de runtime e integração específicos |
| Kubernetes gerenciado | múltiplas cargas exigem políticas comuns | declarações portáveis e controles de rollout | curva operacional, custo de cluster e add-ons |
| SaaS de agenda integrado | processo não é diferencial e contrato é suficiente | entrega funcional rápida | residência, integração, exportação e lock-in |

Não há vencedora genérica. Para uma capacidade simples com poucos serviços, PaaS pode diminuir risco mais que operar Kubernetes. Para várias cargas que já precisam de isolamento, observabilidade e deploy consistentes, um cluster pode justificar sua operação. A plataforma hospitalar usa kind no ensino para tornar Deployment e rollback visíveis. Esse uso didático não recomenda Kubernetes em produção.

## Contextos de mercado como fonte de perguntas

**AWS** é um vocabulário concreto para discutir ofertas: uma máquina virtual como EC2 se aproxima do consumo de IaaS. Um runtime ou banco gerenciado desloca mais responsabilidade para o provedor. Um produto de agenda configurado pode ser SaaS. Esses nomes não classificam automaticamente uma solução nem respondem por residência de dados, custo de saída ou continuidade. A decisão do hospital começa pelos atributos e pelo contrato, e só depois pergunta qual serviço os satisfaz.

Os casos públicos de **iFood** e **Taco Bell** servem como contexto para formular perguntas, não como propaganda nem como arquitetura copiável. Uma plataforma com picos de pedidos pode discutir elasticidade, telemetria e autonomia de times. Uma operação de restaurantes pode discutir integração, sazonalidade e uma experiência de canal digital. Nenhum desses relatos prova que o hospital deve adotar AWS, serverless ou Kubernetes. Escala, dados regulados, capacidade da equipe, dependências existentes e evidências próprias determinam a escolha.

Uma comparação responsável registra o princípio antes da marca: “reduzir operação de runtime” pode apontar para PaaS. “Manter controle de rede e sistema” pode apontar para IaaS ou on-premise. “Comprar uma capacidade não diferenciadora” pode apontar para SaaS. Para cada hipótese, a equipe declara o que fica sob sua responsabilidade, como exportará dados, que sinal confirmará o benefício e quando revisará a decisão.

## Representar a arquitetura de referência na AWS

Traduzir o modelo de referência do módulo para um provedor concreto é um exercício útil, desde que a tradução venha depois do princípio. O portfólio abaixo reúne os serviços básicos da AWS por categoria e serve como vocabulário para essa tradução. A tabela de referência original vem da ByteByteGo.

| Computação | Para que serve |
| --- | --- |
| Amazon EC2 | servidores virtuais na nuvem |
| AWS Lambda | funções *serverless* para cargas orientadas a eventos |
| Amazon ECS | orquestração gerenciada de contêineres |
| Amazon EKS | gerenciamento de clusters Kubernetes |
| AWS Fargate | computação *serverless* para contêineres |

| Armazenamento | Para que serve |
| --- | --- |
| Amazon S3 | armazenamento de objetos escalável |
| Amazon EBS | armazenamento em bloco para instâncias EC2 |
| Amazon FSx | armazenamento de arquivos gerenciado |
| AWS Backup | automação centralizada de cópias de segurança |
| Amazon Glacier | armazenamento frio para arquivamento |

| Banco de dados | Para que serve |
| --- | --- |
| Amazon RDS | banco relacional gerenciado |
| Amazon DynamoDB | banco NoSQL de baixa latência |
| Amazon Aurora | banco nativo de nuvem de alto desempenho |
| Amazon Redshift | *data warehousing* escalável |
| Amazon ElastiCache | cache em memória com Redis ou Memcached |
| Amazon DocumentDB | banco de documentos compatível com MongoDB |
| Amazon Keyspaces | serviço gerenciado compatível com Cassandra |

| Rede e segurança | Para que serve |
| --- | --- |
| Amazon VPC | rede isolada na nuvem |
| AWS CloudFront | rede de entrega de conteúdo |
| AWS Route 53 | serviço de nomes de domínio escalável |
| AWS WAF | proteção contra ataques a aplicações web |
| AWS Shield | proteção contra negação de serviço distribuída |

| IA e aprendizado de máquina | Para que serve |
| --- | --- |
| Amazon SageMaker | criar, treinar e implantar modelos |
| AWS Rekognition | análise de imagem e vídeo |
| AWS Textract | extração de texto de documentos digitalizados |
| Amazon Comprehend | processamento de linguagem natural |

| Monitoramento e DevOps | Para que serve |
| --- | --- |
| Amazon CloudWatch | métricas, logs e alertas |
| AWS X-Ray | rastreamento distribuído de aplicações |
| AWS CodePipeline | automação de esteira de CI e entrega |
| AWS CloudFormation | infraestrutura como código |

Um desenho pronto ajuda a calibrar o nível de detalhe esperado.

![Diagrama isométrico de uma arquitetura AWS com Route 53, CloudFront, S3 para recursos estáticos, balanceadores em duas zonas de disponibilidade, instâncias EC2 sob auto scaling e um par RDS primário e réplica com replicação entre zonas.](https://github.com/user-attachments/assets/7f2fb3aa-d983-4b7b-aff4-dcd7dcd39c56)

*Figura 16 — Nível de detalhe esperado num diagrama de arquitetura de nuvem. Fonte: Cloudcraft.*

**Leitura textual da figura:** um usuário chega por duas vias, o Amazon Route 53 para resolução de nome e o CloudFront como rede de entrega de conteúdo, que busca recursos estáticos no S3. Do CloudFront o tráfego segue para um balanceador Elastic Load Balancing e daí para instâncias EC2 distribuídas em duas zonas de disponibilidade, marcadas como AZ A e AZ B. Faixas alaranjadas atravessam os grupos de instâncias indicando auto scaling. Um segundo balanceador aparece adiante, encaminhando para outra camada de instâncias. À direita, um banco RDS primário replica para uma réplica RDS em outra zona, com a ligação rotulada como replicação entre zonas. Um cadeado à esquerda representa o controle de segurança na borda.

A tradução responsável mantém a ordem. O atributo vem primeiro, depois o princípio, e só então o serviço. “Reduzir operação de runtime” pode chegar a Fargate ou a um runtime gerenciado. “Manter controle de rede e sistema” pode chegar a EC2 dentro de uma VPC. “Comprar capacidade não diferenciadora” pode chegar a um SaaS de agenda. O caminho inverso, que parte do serviço e depois procura a justificativa, produz o desenho bonito que ninguém consegue defender numa revisão.

## Proposta inicial verificável

A equipe mantém a API stateless, move estado durável para serviço apropriado e define um SLO de disponibilidade e latência durante a janela. Ela começa com duas réplicas em domínios de falha distintos quando a infraestrutura suportar, request/limit medidos e HPA apenas depois de verificar a métrica. Uma fila ou rate limit pode proteger a dependência se a demanda exceder capacidade. A resposta ao usuário deve indicar “em processamento” quando o contrato permitir, em vez de manter conexões até falharem.

O orçamento inclui tempo de cluster, banco, logs, traces, transferência e trabalho de plantão. Uma etiqueta relaciona recursos ao produto e ambiente. Uma política reduz ambiente de teste fora do horário. Para lock-in, a equipe documenta o serviço específico escolhido, formato de exportação, identidade usada, custo de saída e teste periódico de restauração. Saber o que seria difícil mudar, e por quê, basta. Criar uma camada de abstração que esconda tudo é desnecessário.

## Incidente de atualização

Na sexta-feira, a versão nova da API aponta para uma tag que não existe no registry. O rollout não completa porque as novas réplicas não iniciam. As antigas continuam atendendo graças a `maxUnavailable: 0`, mas o rollout fica bloqueado. O operador confirma revisão, eventos e status dos Pods. Depois executa rollback para a revisão anterior, confirma duas réplicas prontas e abre investigação sobre o pipeline de publicação. Não apaga Pods manualmente nem altera produção para “testar”.

O caso mostra que resiliência começa por reduzir alcance da mudança e aumentar observabilidade. A melhoria posterior pode ser publicar por digest, validar existência da imagem antes do rollout e exigir evidência de health endpoints. O rollback é contenção. O aprendizado está em corrigir a barreira que permitiu a tag inválida.
