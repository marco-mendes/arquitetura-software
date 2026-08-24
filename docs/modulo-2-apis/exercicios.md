# Exercícios por Taxonomia de Bloom

Responda primeiro e abra “Ver resposta” somente depois da tentativa. Nas atividades de Aplicar, Analisar, Avaliar e Criar, siga o roteiro completo: ele apresenta o artefato, a condição de início, a evidência e os limites da prática antes de pedir uma decisão.

## Recordar

1\. Toda API tem três camadas fáceis de confundir: a **interface** (a porta oferecida), o **contrato** (as promessas observáveis) e a **implementação** (como elas são cumpridas). O que diferencia essas três?

<details markdown="1">
<summary>Ver resposta</summary>

Interface é a fronteira oferecida; contrato torna explícitas as promessas observáveis; implementação é o mecanismo que as cumpre. Um consumidor deveria depender do contrato, e não do framework ou banco usados internamente.
</details>

2\. Os métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`...) têm papéis diferentes por convenção. Qual é a diferença fundamental de propósito entre `GET` e `POST`?

<details markdown="1">
<summary>Ver resposta</summary>

`GET` solicita a representação atual de um recurso, sem a intenção de alterar estado no servidor. `POST` normalmente cria algo novo ou dispara um processamento, alterando o estado do servidor.
</details>

3\. Por que uma API REST evita colocar o nome da ação na própria URL — como `/criarPedido` ou `/listarPedidos` — e prefere algo como `POST /pedidos` e `GET /pedidos`?

<details markdown="1">
<summary>Ver resposta</summary>

Porque REST organiza a API em torno de **recursos** (substantivos) e deixa a ação a cargo do **verbo HTTP**. Repetir a ação na URL duplica a semântica e quebra a uniformidade que permite tratamento genérico por ferramentas, cache e roteamento.
</details>

4\. Em integrações, a mesma chamada às vezes chega repetida. O que significa dizer que uma operação é **idempotente**?

<details markdown="1">
<summary>Ver resposta</summary>

Repetir a mesma intenção produz o mesmo efeito pretendido no servidor. Isso não exige que cada resposta seja idêntica nem cria deduplicação automática em uma integração distribuída.
</details>

5\. Existe um formato padrão para descrever por escrito os paths, operações, schemas, exemplos e respostas de uma API HTTP. Que artefato é esse?

<details markdown="1">
<summary>Ver resposta</summary>

Um documento OpenAPI. No laboratório, o contrato explícito está em `laboratorios/plataforma-hospitalar/contratos/openapi.yaml`.
</details>

6\. Um **API gateway** fica na borda, entre os consumidores e as APIs internas. Cite duas responsabilidades técnicas adequadas a ele — e uma que **não** deveria ficar nele.

<details markdown="1">
<summary>Ver resposta</summary>

Roteamento, terminação TLS, autenticação técnica, limite de tráfego, correlação e telemetria são responsabilidades possíveis. Tradução de vocabulário do laboratório e regras de elegibilidade não devem ser despejadas no gateway.
</details>

## Compreender

1\. Uma operação `POST /aprovarAutomaticamente` usa JSON e HTTP. Por que ela pode ser um RPC coerente, mas não deve ser chamada de REST só por causa disso?

<details markdown="1">
<summary>Ver resposta</summary>

RPC organiza a colaboração por operações nomeadas. REST requer restrições e semântica de recursos, representações e mensagens HTTP; uma URL com HTTP não comprova essas propriedades.
</details>

2\. Comparado a uma API de leitura com campos fixos, quando o GraphQL tende a ajudar mais?

<details markdown="1">
<summary>Ver resposta</summary>

Quando consumidores precisam de combinações de campos e relações muito variáveis. Ainda é necessário controlar custo das consultas, autorização por campo e cache; não é a escolha automática para qualquer tela móvel.
</details>

3\. O **WebSocket** mantém um canal aberto entre cliente e servidor. O que ele resolve, e o que ele não resolve sozinho?

<details markdown="1">
<summary>Ver resposta</summary>

Ele mantém um canal bidirecional persistente para atualização em tempo real. Não garante entrega durável, reprocessamento, ordenação de negócio ou recuperação após desconexão; essas políticas precisam ser projetadas.
</details>

4\. O laboratório fala **SOAP/TISS** (o padrão de troca das operadoras) e a plataforma usa o próprio vocabulário. Por que traduzir entre os dois é mais apropriado num **adaptador** do que no **gateway**?

<details markdown="1">
<summary>Ver resposta</summary>

Porque a tradução contém conhecimento da dependência e de seus significados. O gateway pode aplicar políticas técnicas; o adaptador isola mudanças externas e protege o domínio interno da plataforma.
</details>

## Aplicar

### Recomendar o estilo de entrega do resultado ao parceiro

**Objetivo**

Recomendar um entre quatro estilos de interação para entregar resultados de exame a uma operadora parceira, declarando ganho, custo e o fato que decide.

**Situação**

O hospital precisa entregar o resultado de exames a uma operadora de saúde parceira. O resultado nasce no laboratório e fica pronto muito depois do pedido. A operadora usa esse resultado para liberar procedimentos seguintes, então o atraso tem consequência para o paciente.

Hoje não existe integração. Alguém exporta uma planilha no fim do dia e envia por correio eletrônico. A operadora reclama do atraso e o hospital reclama do retrabalho.

A área de integração pediu uma recomendação de contrato antes de abrir o projeto.

**Seu papel**

Você é a pessoa arquiteta responsável pela recomendação de contrato. A implementação fica com outra equipe, que espera de você a escolha e os riscos declarados.

**Artefato que você irá usar**

Crie `entregas/unidade-2/aplicar-entrega-resultado.md`, a partir da raiz do repositório `arquitetura-software`, e use as comparações de estilos de interação em `docs/modulo-2-apis/conceitos.md`.

**Antes de executar**

Crie o diretório `entregas/unidade-2/`; o estado inicial é sem serviço iniciado e sem alteração do laboratório.

Seis fatos foram apurados nas duas empresas:

1. O resultado fica pronto entre vinte minutos e seis horas depois do pedido, sem previsibilidade.
2. A operadora processa no máximo quatrocentos resultados por dia.
3. O contrato entre as empresas exige comprovar a entrega de cada resultado, com identificador e carimbo de tempo.
4. A operadora não mantém endereço público para receber chamadas de entrada, e a área de segurança dela não pretende abrir um.
5. O hospital não opera fila nem *broker* hoje, e a infraestrutura tem uma pessoa.
6. Um atraso de até quinze minutos entre o resultado ficar pronto e chegar à operadora é aceitável.

As quatro alternativas em avaliação:

| Alternativa | O que muda no contrato |
| --- | --- |
| **A. Consulta periódica** | O hospital expõe um recurso REST com os resultados prontos. A operadora consulta de tempos em tempos e marca o que já leu. |
| **B. Aceitação assíncrona** | A operadora registra o interesse num pedido e recebe `202` com `Location`. Consulta aquele protocolo depois, até o resultado aparecer. |
| **C. Chamada de retorno** | Quando o resultado fica pronto, o hospital chama um endereço da operadora e entrega o conteúdo. |
| **D. Mensageria** | O hospital publica cada resultado num tópico. A operadora consome no próprio ritmo, com reprocessamento possível. |

**O que fazer**

1. Recomende **uma** das quatro alternativas, em uma frase.
2. Preencha o quadro comparativo, uma linha por alternativa. A primeira vem resolvida como modelo.

    | Alternativa | O que resolve | O que cobra | Fato decisivo |
    | --- | --- | --- | --- |
    | A. Consulta periódica | funciona sem exigir nada da infraestrutura da operadora | gasta chamadas em vão quase o dia inteiro e o atraso depende do intervalo escolhido | fato 4, que mantém a alternativa viva |
    | B. Aceitação assíncrona | | | |
    | C. Chamada de retorno | | | |
    | D. Mensageria | | | |

3. Escreva o contrato de erro da alternativa recomendada: que resposta o consumidor recebe quando o resultado ainda não existe e quando o identificador é desconhecido.
4. Diga como a sua recomendação atende ao fato 3, isto é, onde fica a comprovação de entrega.
5. Aponte a alternativa que você descartaria de imediato e nomeie o fato apurado que a derruba.
6. Declare o risco que a sua recomendação aceita e escreva o sinal observável que levaria a trocar de alternativa.

**Evidência esperada**

O artefato traz o quadro comparativo completo, a recomendação em uma frase, o contrato de erro escrito com código de status e identificador, a resposta sobre comprovação de entrega, a alternativa descartada com o fato que a derruba, o risco aceito e o sinal de revisão observável.

**Entrega esperada**

Envie `entregas/unidade-2/aplicar-entrega-resultado.md` com no máximo uma página, contendo o quadro comparativo, a recomendação, o contrato de erro, o risco aceito e o sinal de revisão.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Comparação com ganho e custo nas quatro alternativas | 30% | Evidência: as duas colunas preenchidas para as quatro; insuficiente: alternativa listada sem custo. |
| Recomendação sustentada por fato apurado | 25% | Evidência: fato citado pelo número; insuficiente: escolha por moda tecnológica. |
| Contrato de erro explícito | 20% | Evidência: código de status e identificador; insuficiente: "retorna erro". |
| Alternativa descartada com motivo | 15% | Evidência: fato que a derruba; insuficiente: descarte sem base. |
| Risco aceito e sinal de revisão | 10% | Evidência: consequência e condição observável; insuficiente: prazo no calendário. |

## Analisar

**Objetivo**

Comparar contratos de consulta de agenda e identificar como paginação, estilo de API e adaptadores respondem a mudanças concorrentes sem apresentar uma escolha como automática.

**Situação**

Oito unidades consultam três parceiros, com até 40 mil horários futuros. Há inserção, cancelamento e navegação móvel em lotes de vinte. A ordena por data; B não ordena; C usa cursor próprio. A meta é p95 de 800 ms, sem medição atual.

**Seu papel**

Você analisa o contrato de leitura e a fronteira de adaptação. Sua entrega deve separar o que o enunciado afirma, o que você supõe e o que precisa ser medido.

**Artefato que você irá usar**

Use o enunciado, [conceitos](conceitos.md), [padrões e decisões](padroes-e-decisoes.md), Mermaid e Markdown. Não há API de agenda: executar significa construir e revisar a análise.

**Insumos disponíveis**

Compare paginação por `offset/limit` e cursor opaco; REST, GraphQL e RPC como formas de interação; e um adaptador por parceiro. Considere limite máximo de cem itens, inserção, cancelamento e itens com mesma data. Não invente medições de latência.

**Antes de executar**

Na raiz do clone `arquitetura-software`, crie `entregas/unidade-2/analise-agenda/` com `forcas.md`, `contratos.md`, `simulacao.md` e `sequencia.md`. A condição inicial verificável é: os quatro arquivos existem, `sequencia.md` pode receber Mermaid e nenhum deles contém uma recomendação pronta.

**Como conduzir**

Comece por forças e incertezas. Os dois contratos e o diagrama devem decorrer dessa análise, não servir para defender antecipadamente uma tecnologia.

**O que fazer**

1. Separe volume, navegação, mudança, interoperabilidade, latência e incerteza.
2. Modele `offset/limit` e cursor com parâmetros, ordenação, continuação e erro.
3. Simule cinco páginas; insira e cancele entre elas; marque repetição ou omissão.
4. Compare REST, GraphQL e RPC por colaboração, descoberta, cache, evolução, risco e evidência.
5. Desenhe sequência Mermaid com móvel, API, adaptador e parceiro; inclua leitura textual.
6. Proponha duas medições com amostra, medida e limiar.

**Evidência esperada**

Os arquivos mostram duas propostas comparáveis, efeitos concretos de inserção/cancelamento, um diagrama legível e hipóteses marcadas como hipóteses.

**Entrega esperada**

Entregue `entregas/unidade-2/analise-agenda/` com os quatro arquivos e até 900 palavras. Inclua uma lacuna que impede recomendação definitiva.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Forças e incertezas separadas | 20% | Evidência: hipótese marcada; insuficiência: suposição apresentada como fato. |
| Contratos completos e comparáveis | 25% | Evidência: campos, semântica e erros; insuficiência: fragmentos sem continuação ou ordenação. |
| Simulação de mudança concorrente | 20% | Evidência: repetição/omissão localizada; insuficiência: mudança citada sem efeito mostrado. |
| Comparação simétrica de estilos | 20% | Evidência: mesmos critérios; insuficiência: preferência sem contraste. |
| Modelo e experimento coerentes | 15% | Evidência: diagrama, leitura e medida se correspondem; insuficiência: seta ou métrica sem propósito. |

## Avaliar

**Objetivo**

Avaliar propostas de autorização com critérios mensuráveis, identificar compromissos ausentes e produzir uma recomendação condicionada à evidência disponível.

**Situação**

No pico há 12 mil autorizações/hora; 5% repetem após dois segundos. A operadora leva 200 ms–25 s e fica indisponível até dez minutos duas vezes ao mês. A mantém chamada aberta; B aceita e devolve protocolo; C usa RPC/gRPC interno e HTTP ao cliente. Nenhuma define idempotência, retenção ou resposta tardia.

**Seu papel**

Você participa de uma revisão arquitetural. Pode recomendar uma proposta, combinar elementos, pedir experimento limitado ou adiar a decisão. Você não precisa escolher a alternativa que parece mais moderna.

**Artefato que você irá usar**

Use o enunciado, [conceitos](conceitos.md), [padrões e decisões](padroes-e-decisoes.md) e o [template de ADR](../referencia/template-adr.md). Não há gRPC, broker ou operadora instalada: avalie o parecer, não ferramentas.

**Insumos disponíveis**

Considere amostra de dez mil requisições com 500 repetições, orçamento de resposta inicial de dois segundos e necessidade de rastrear cada pedido por 24 horas. Considere REST/HTTP, RPC/gRPC, chave de idempotência, `202`, `Location`, timeout e reconciliação. Não presuma infraestrutura adicional já disponível.

**Antes de executar**

Na raiz do clone, crie `entregas/unidade-2/avaliacao-autorizacao/parecer.md`. Comece com uma tabela vazia contendo “critério”, “medida”, “evidência disponível”, “lacuna” e “impacto”. A condição inicial verificável é a tabela existir antes de qualquer recomendação.

**Como conduzir**

Preencha critérios e evidências antes de comparar as propostas. Uma recomendação só é útil se sua objeção e seu gatilho de revisão puderem ser verificados depois.

**O que fazer**

1. Defina critérios de resposta, disponibilidade, repetição, rastreabilidade, evolução e operação.
2. Modele resposta rápida, lenta, indisponibilidade e repetição para A, B e C.
3. Liste compromissos ausentes: retenção, idempotência, falha temporária e resposta tardia.
4. Compare acoplamento temporal, duplicidade, operação e evolução.
5. Recomende sob condição; proponha dois testes com amostra, medida e limiar.
6. Registre objeção forte e gatilho de revisão.

**Evidência esperada**

O parecer mostra critérios anteriores à escolha, uma comparação completa, dois experimentos mensuráveis e uma recomendação que declara incertezas.

**Entrega esperada**

Entregue `entregas/unidade-2/avaliacao-autorizacao/parecer.md` com tabela, análise, recomendação, objeção e gatilho. Cada cálculo deve indicar os dados do enunciado usados.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Critérios antes da recomendação | 20% | Evidência: tabela inicial; insuficiência: critério posterior. |
| Falhas e repetições no contrato | 25% | Evidência: status e protocolo; insuficiência: “erro” genérico. |
| Consequências comparadas | 25% | Evidência: ganho e custo; insuficiência: opção sem limite. |
| Experimentos mensuráveis | 15% | Evidência: amostra e limiar; insuficiência: teste vago. |
| Recomendação revisável | 15% | Evidência: objeção/gatilho; insuficiência: conclusão absoluta. |

## Criar

**Objetivo**

Criar a baseline de contratos do incremento 2 para que outra equipe consiga revisar, executar e evoluir a fronteira hospitalar sem antecipar serviços, broker ou gateway que ainda não foram justificados.

**Situação**

Defina API inicial de agenda e elegibilidade, fronteira com operadora/laboratório e tratamento de resultados posteriores. A equipe ainda opera uma aplicação; parceiros têm contratos próprios, chamadas repetem e respostas podem levar horas.

**Seu papel**

Você coordena um pacote de contratos e evidências. Sua responsabilidade é manter coerência entre consumidor, operação, schema, erro, diagrama, decisão e limite declarado.

**Artefato que você irá usar**

Use [contexto hospitalar](../projeto-integrador/contexto-hospitalar.md), `laboratorios/plataforma-hospitalar/contratos/openapi.yaml` como referência, OpenAPI, Mermaid, Bruno, Spectral, [template de ADR](../referencia/template-adr.md) e dados sintéticos. O contrato existente é exemplo, não solução para agenda ou laboratório.

**Insumos disponíveis**

Inclua ao menos uma operação de agenda, uma de elegibilidade e uma fronteira de adaptação externa. Compare REST/HTTP, pelo menos mais duas formas de interação ou estratégias de integração, usando as mesmas forças. Considere paginação para coleções e repetição para comandos relevantes.

**Antes de executar**

Na raiz do clone, crie `entregas/unidade-2/baseline-contratos/` com `contratos/`, `diagramas/`, `evidencias/` e `decisoes/`. Crie também um `README.md` com o objetivo do pacote. A condição inicial verificável é: as quatro pastas e o índice existem; os dados de exemplo não identificam pessoas reais; e o grupo consegue localizar o OpenAPI de referência sem alterá-lo.

**Como conduzir**

Produza os artefatos em ordem de dependência: contexto e consumidores antes do contrato; contrato antes do diagrama; validação antes do ADR final. Ao terminar, procure nomes, estados e promessas que divergem entre arquivos.

**O que fazer**

1. No `README.md`, declare consumidor, capacidade, fronteira, resultado e fora de escopo.
2. Escreva OpenAPI com schemas, exemplos, estados, erros e cabeçalhos.
3. Declare ordenação/paginação de coleções e idempotência de comandos relevantes.
4. Modele caminho normal e falha externa em Mermaid, com leitura textual.
5. Registre alternativas, decisão, consequências, transição, evidências e gatilhos em `ADR-002.md`.
6. Valide com Spectral, execute exemplos no Bruno quando aplicável e guarde saídas.
7. Confira nomes, operações, status e responsabilidades em todos os artefatos.

**Evidência esperada**

O pacote mostra uma cadeia legível de consumidor → contrato → exemplo → diagrama → ADR → validação, além de lacunas honestas sobre integração externa, persistência e componentes não instalados.

**Entrega esperada**

Entregue `entregas/unidade-2/baseline-contratos/` com `README.md`, contratos, diagramas, evidências e `ADR-002.md`. Outra equipe deve conseguir identificar o que executar, o que revisar e o que ainda exige experimento.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Fronteiras, consumidores e responsabilidades rastreáveis | 15% | Evidência: ator e responsável explícitos; insuficiência: responsabilidade apenas implícita. |
| Contratos completos e semanticamente claros | 25% | Evidência: exemplos e erros válidos; insuficiência: campos ou estados sem significado. |
| Evolução, paginação e repetição contextualizadas | 20% | Evidência: política ligada à necessidade; insuficiência: mecanismo citado sem motivo. |
| Diagramas, exemplos e contratos coerentes | 15% | Evidência: mesmas operações e estados; insuficiência: diagrama contradiz contrato. |
| Evidências reproduzíveis e limites explícitos | 15% | Evidência: caminho, comando e condição; insuficiência: saída sem contexto. |
| ADR revisável | 10% | Evidência: alternativas, consequências e gatilho; insuficiência: decisão sem racional ou revisão. |
