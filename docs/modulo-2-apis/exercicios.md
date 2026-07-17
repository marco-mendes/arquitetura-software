# Exercícios por Taxonomia de Bloom

Os exercícios avançam de vocabulário para uma baseline de contratos. Recordar e Compreender oferecem retorno comentado para estudo autônomo. Aplicar, Analisar, Avaliar e Criar apresentam todos os dados necessários, um procedimento e critérios que somam 100%. As atividades avançadas admitem alternativas justificadas e não incluem resposta pronta.

## Recordar

1. O que diferencia interface, contrato e implementação?
2. Qual status comunica aceitação sem conclusão?
3. Qual cabeçalho pode indicar onde acompanhar um recurso aceito?
4. O que significa dizer que um método é idempotente?
5. Qual artefato descreve paths, operações, schemas e respostas de uma API HTTP?
6. Cite duas responsabilidades adequadas a um API gateway.

**Respostas comentadas**

1. Interface é a fronteira oferecida, contrato explicita promessas observáveis e implementação é o mecanismo que as cumpre.
2. `202 Accepted`. Ele não afirma que o processamento terminou.
3. `Location`. O valor deve identificar o recurso relevante ao acompanhamento.
4. Repetir a mesma intenção tem o mesmo efeito pretendido no servidor; respostas e metadados ainda podem variar.
5. Um documento OpenAPI.
6. Entre as possibilidades estão roteamento, terminação TLS, limites de uso e correlação. Regras centrais do domínio não são uma boa responsabilidade para o gateway.

## Compreender

Classifique cada afirmação como decisão de contrato, detalhe de implementação, evidência ou força do contexto e justifique.

1. “A resposta de aceitação usa `202` e inclui `Location`.”
2. “O servidor guarda protocolos em um dicionário Python.”
3. “O teste envia o exemplo OpenAPI e recebe `202`.”
4. “Uma operadora pode demorar até trinta segundos para responder.”
5. “O consumidor deve tolerar campos opcionais desconhecidos.”
6. “A aplicação usa FastAPI.”

**Respostas comentadas**

1. Decisão de contrato, pois consumidor observa status e cabeçalho.
2. Detalhe de implementação enquanto não altera comportamento prometido.
3. Evidência de concordância para uma amostra válida.
4. Força temporal que influencia interação síncrona ou acompanhada.
5. Regra de compatibilidade do contrato.
6. Tecnologia de implementação, não estilo arquitetural por si só.

Explique ainda por que `POST /aprovarAutomaticamente` pode ser uma operação RPC coerente, mas não deve ser chamada de REST apenas porque usa JSON e HTTP. Compare unidade principal, semântica e expectativa do consumidor.

## Aplicar

**Situação**

Você recebeu o laboratório local com `POST /elegibilidades`, `GET /elegibilidades/{protocolo}`, contrato OpenAPI e testes. Precisa comprovar o caminho feliz e um erro antes de compartilhar a baseline.

**Seu papel**

Você atua como consumidor do contrato e registra evidências reproduzíveis, sem alterar a implementação.

**Insumos disponíveis**

Use `contratos/openapi.yaml`, Bruno, Spectral, FastAPI em `src/hospital/api` e `tests/test_api_contract.py`. O pedido sintético válido é `cpf=12345678901`, `codigo_operadora=OPS-001` e `matricula_plano=MAT-2026-001`.

**Como conduzir**

1. Prepare o ambiente pela oficina e execute os testes de contrato.
2. Valide o OpenAPI com Spectral e guarde a saída.
3. Importe o contrato no Bruno e envie o pedido válido.
4. Registre status, `Location`, protocolo, situação e instante.
5. Consulte o protocolo pela operação `GET` e compare os corpos.
6. Remova `cpf`, envie novamente e registre o erro estruturado.
7. Escreva três frases separando o que foi demonstrado do que permanece fora do experimento.

**Entrega esperada**

Uma pasta `evidencias-aplicar` com saídas de Spectral e pytest, coleção Bruno, três respostas e uma nota de interpretação. Outra pessoa deve conseguir repetir os comandos.

**Critérios de avaliação**

| Critério observado | Percentual |
| --- | ---: |
| Comandos, versões e resultados reproduzíveis | 25% |
| Caminho `POST` e `GET` coerente com o contrato | 30% |
| Erro `422` registrado com código e detalhe | 25% |
| Limites da evidência declarados com precisão | 20% |

## Analisar

**Situação**

Uma rede de oito unidades consulta disponibilidade de agenda de três parceiros. Cada parceiro oferece até 40 mil horários futuros. Novos horários entram durante o dia, cancelamentos removem opções e o aplicativo móvel navega em lotes de vinte. O parceiro A ordena por data; B entrega sem ordem; C usa um cursor próprio. A rede quer uma linguagem única e tempo de resposta de até 800 ms no percentil 95. Um usuário pode avançar cinco páginas enquanto a coleção muda.

**Seu papel**

Você analisa o contrato de leitura e a fronteira de adaptação, sem escolher uma alternativa antes de comparar evidências.

**Insumos disponíveis**

Considere paginação por `offset/limit` e por cursor opaco; REST, GraphQL e RPC como estilos possíveis; um adaptador por parceiro; limite máximo de cem itens; e amostras sintéticas com inserção, cancelamento e item de mesma data. Não há medições de latência dos parceiros.

**Como conduzir**

1. Separe forças de volume, estabilidade de navegação, mudança concorrente, interoperabilidade e latência.
2. Defina ordenação e identidade necessárias para cada alternativa de paginação.
3. Modele dois contratos de leitura, incluindo parâmetros, resposta, continuação e erros.
4. Simule cinco páginas com inserções e cancelamentos e marque repetição ou omissão.
5. Compare REST, GraphQL e RPC pelas mesmas dimensões, sem inferir desempenho pelo nome.
6. Desenhe uma sequência Mermaid com consumidor, API, adaptador e parceiro.
7. Liste medições ausentes e uma experiência capaz de produzi-las.

**Entrega esperada**

Uma matriz de forças, dois fragmentos de contrato, tabela da simulação, diagrama com leitura textual e análise de até 900 palavras. Inclua hipóteses e não apresente estimativas como medições.

**Critérios de avaliação**

| Critério observado | Percentual |
| --- | ---: |
| Forças e incertezas de contexto corretamente separadas | 20% |
| Contratos completos e comparáveis | 25% |
| Simulação evidencia efeitos de mudança concorrente | 20% |
| Comparação simétrica de estilos e adaptações | 20% |
| Diagrama, texto e experiência proposta são coerentes | 15% |

## Avaliar

**Situação**

Uma plataforma administrativa recebe 12 mil pedidos de autorização por hora no pico. Cinco por cento dos clientes repetem a chamada quando não recebem resposta em dois segundos. A operadora leva de 200 ms a 25 s e fica indisponível por até dez minutos duas vezes ao mês. A proposta A mantém a chamada aberta e devolve decisão final. A proposta B aceita o pedido, devolve protocolo e permite consulta. A proposta C usa um método RPC síncrono interno via gRPC e expõe uma API HTTP separada aos clientes. Nenhuma proposta definiu idempotência, retenção ou tratamento de resposta tardia.

**Seu papel**

Você participa de uma revisão arquitetural e pode recomendar uma proposta, combinar elementos, pedir experimento ou adiar a decisão.

**Insumos disponíveis**

Use os fatos acima, uma amostra de dez mil requisições com 500 repetições, orçamento de resposta inicial de dois segundos e necessidade de rastrear cada pedido por 24 horas. Considere REST/HTTP, RPC/gRPC, chave de idempotência, `202`, `Location`, timeout e reconciliação. Não presuma infraestrutura adicional já instalada.

**Como conduzir**

1. Defina critérios mensuráveis antes de examinar as propostas.
2. Modele a experiência do cliente sob resposta rápida, lenta, indisponibilidade e repetição.
3. Identifique compromissos de contrato ausentes em cada proposta.
4. Compare acoplamento temporal, risco de duplicação, complexidade operacional e evolução.
5. Redija uma recomendação condicionada à evidência disponível.
6. Proponha dois testes com a amostra e limiares de aceitação.
7. Registre a objeção mais forte à recomendação e um gatilho que a mudaria.

**Entrega esperada**

Um parecer com critérios, matriz de propostas, recomendação condicionada, duas experiências, objeção e gatilho de revisão. Cada cálculo deve mostrar os dados usados.

**Critérios de avaliação**

| Critério observado | Percentual |
| --- | ---: |
| Critérios definidos antes da recomendação | 20% |
| Falhas e repetições analisadas pelo contrato | 25% |
| Consequências comparadas sem preferência implícita | 25% |
| Experiências têm amostra, medida e limiar | 15% |
| Recomendação, objeção e gatilho são rastreáveis | 15% |

## Criar

**Situação**

O grupo precisa entregar o incremento 2 da plataforma hospitalar. A baseline anterior delimitou agenda, elegibilidade, autorização e integração com laboratório. Operadora e laboratório mantêm contratos próprios; chamadas podem repetir; respostas externas variam de instantâneas a horas; a equipe ainda opera uma única aplicação. A entrega deve orientar implementação futura sem antecipar divisão em serviços, broker ou gateway.

**Seu papel**

Você coordena um pacote de contratos que outra equipe conseguirá revisar, executar e evoluir.

**Insumos disponíveis**

Use o [contexto hospitalar](../projeto-integrador/contexto-hospitalar.md), o contrato de elegibilidade do laboratório, OpenAPI 3.1, Mermaid, Bruno, Spectral, o [template de ADR](../referencia/template-adr.md) e dados exclusivamente sintéticos. Inclua pelo menos uma operação de agenda, uma de elegibilidade e uma fronteira de adaptação externa.

**Como conduzir**

1. Recupere atores, fronteiras e cenários de qualidade da baseline anterior.
2. Para cada interação, declare consumidor, resultado, necessidade temporal e responsável pelos dados.
3. Compare ao menos três estilos ou formas de interação pelas mesmas forças.
4. Escreva contratos com operações, schemas, estados, erros, correlação e exemplos.
5. Defina paginação onde houver coleção e idempotência onde houver repetição relevante.
6. Modele em Mermaid caminho normal e falha externa, com leitura textual.
7. Execute lint e exemplos e registre divergências entre contrato e implementação.
8. Produza `ADR-002` com consequência, transição compatível e gatilho de revisão.
9. Faça revisão cruzada entre ADR, contratos, diagramas e evidências.

**Entrega esperada**

Uma pasta versionável com índice, contratos OpenAPI, exemplos Bruno, mapa de erros, diagramas, evidências de validação e `ADR-002`. A entrega deve indicar lacunas e decisões adiadas, sem instalar componentes fora do incremento.

**Critérios de avaliação**

| Critério observado | Percentual |
| --- | ---: |
| Fronteiras, consumidores e responsabilidades rastreáveis | 15% |
| Contratos completos, coerentes e semanticamente claros | 25% |
| Evolução, paginação e repetição tratadas conforme o contexto | 20% |
| Diagramas e exemplos concordam com os contratos | 15% |
| Evidências são reproduzíveis e limites são explícitos | 15% |
| ADR preserva alternativas, consequências e revisão | 10% |
