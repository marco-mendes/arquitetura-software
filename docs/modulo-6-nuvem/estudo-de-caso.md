# Estudo de caso: a janela de agendamento e o pico previsível

## Situação

Toda segunda-feira, às 7h, parceiros consultam elegibilidade antes de liberar agendas de exame. O volume normal é baixo, mas a janela de vinte minutos produz picos. Na última ocorrência, usuários receberam respostas lentas; a equipe concluiu que “precisa de nuvem”. Essa frase ainda não distingue fatos de hipóteses. Os sinais disponíveis são: latência p95 da API, taxa de respostas 5xx, uso de CPU, memória, conexões do serviço de elegibilidade e idade das requisições pendentes. Não há dado clínico no exercício.

O primeiro diagnóstico separa camadas. Se CPU da API fica baixa e o tempo da dependência externa aumenta, aumentar Pods não resolve a causa. Se os Pods atingem request de CPU, têm filas de entrada e a dependência preserva folga, uma escala horizontal pode ajudar. Se uma única instância perde sessão em memória, o problema é stateful e precisa de um estado compartilhado antes de escalar. A decisão é uma hipótese testável: gerar carga sintética, observar limites e registrar a mudança.

## Alternativas

| Alternativa | Quando faz sentido | Benefício | Risco ou custo |
| --- | --- | --- | --- |
| VMs em IaaS com autoscaling | equipe opera SO e rede | controle de runtime e rede | patches, imagens de VM e operação própria |
| runtime PaaS para API stateless | contrato de deploy atende à plataforma | reduz trabalho de host e escala | limites de runtime e integração específicos |
| Kubernetes gerenciado | múltiplas cargas exigem políticas comuns | declarações portáveis e controles de rollout | curva operacional, custo de cluster e add-ons |
| SaaS de agenda integrado | processo não é diferencial e contrato é suficiente | entrega funcional rápida | residência, integração, exportação e lock-in |

Não há vencedora genérica. Para uma capacidade simples com poucos serviços, PaaS pode diminuir risco mais que operar Kubernetes. Para várias cargas que já precisam de isolamento, observabilidade e deploy consistentes, um cluster pode justificar sua operação. A plataforma hospitalar usa kind no ensino para tornar Deployment e rollback visíveis; isso não é recomendação automática de Kubernetes em produção.

## Contextos de mercado, não receitas

**AWS** é um vocabulário concreto para discutir ofertas: uma máquina virtual como EC2 se aproxima do consumo de IaaS; um runtime ou banco gerenciado desloca mais responsabilidade para o provedor; um produto de agenda configurado pode ser SaaS. Esses nomes não classificam automaticamente uma solução nem respondem por residência de dados, custo de saída ou continuidade. A decisão do hospital começa pelos atributos e pelo contrato, e só depois pergunta qual serviço os satisfaz.

Os casos públicos de **iFood** e **Taco Bell** servem como contexto para formular perguntas, não como propaganda nem como arquitetura copiável. Uma plataforma com picos de pedidos pode discutir elasticidade, telemetria e autonomia de times; uma operação de restaurantes pode discutir integração, sazonalidade e uma experiência de canal digital. Nenhum desses relatos prova que o hospital deve adotar AWS, serverless ou Kubernetes. Escala, dados regulados, capacidade da equipe, dependências existentes e evidências próprias determinam a escolha.

Uma comparação responsável registra o princípio antes da marca: “reduzir operação de runtime” pode apontar para PaaS; “manter controle de rede e sistema” pode apontar para IaaS ou on-premise; “comprar uma capacidade não diferenciadora” pode apontar para SaaS. Para cada hipótese, a equipe declara o que fica sob sua responsabilidade, como exportará dados, que sinal confirmará o benefício e quando revisará a decisão.

## Proposta inicial verificável

A equipe mantém a API stateless, move estado durável para serviço apropriado e define um SLO de disponibilidade e latência durante a janela. Ela começa com duas réplicas em domínios de falha distintos quando a infraestrutura suportar, request/limit medidos e HPA apenas depois de verificar a métrica. Uma fila ou rate limit pode proteger a dependência se a demanda exceder capacidade. A resposta ao usuário deve indicar “em processamento” quando o contrato permitir, em vez de manter conexões até falharem.

O orçamento inclui tempo de cluster, banco, logs, traces, transferência e trabalho de plantão. Uma etiqueta relaciona recursos ao produto e ambiente; uma política reduz ambiente de teste fora do horário. Para lock-in, a equipe documenta o serviço específico escolhido, formato de exportação, identidade usada, custo de saída e teste periódico de restauração. Não é necessário criar uma camada de abstração que esconda tudo; é necessário saber o que seria difícil mudar e por quê.

## Incidente de atualização

Na sexta-feira, a versão nova da API aponta para uma tag que não existe no registry. O rollout não completa porque as novas réplicas não iniciam. As antigas continuam atendendo graças a `maxUnavailable: 0`, mas o rollout fica bloqueado. O operador confirma revisão, eventos e status dos Pods. Depois executa rollback para a revisão anterior, confirma duas réplicas prontas e abre investigação sobre o pipeline de publicação. Não apaga Pods manualmente nem altera produção para “testar”.

O caso mostra que resiliência começa por reduzir alcance da mudança e aumentar observabilidade. A melhoria posterior pode ser publicar por digest, validar existência da imagem antes do rollout e exigir evidência de health endpoints. O rollback é contenção; o aprendizado é corrigir a barreira que permitiu a tag inválida.
