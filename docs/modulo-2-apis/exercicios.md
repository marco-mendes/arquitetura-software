# Exercícios por Taxonomia de Bloom

Responda primeiro e abra “Ver resposta” somente depois da tentativa. Nas atividades de Aplicar, Analisar, Avaliar e Criar, siga o roteiro completo: ele apresenta o artefato, a condição de início, a evidência e os limites da prática antes de pedir uma decisão.

## Recordar

1. O que diferencia interface, contrato e implementação em uma API?

<details>
<summary>Ver resposta</summary>

Interface é a fronteira oferecida; contrato torna explícitas as promessas observáveis; implementação é o mecanismo que as cumpre. Um consumidor deveria depender do contrato, e não do framework ou banco usados internamente.
</details>

2. Qual status HTTP comunica que um pedido foi aceito, mas que o processamento ainda pode não ter terminado?

<details>
<summary>Ver resposta</summary>

`202 Accepted`. Ele comunica aceitação; não é uma confirmação de que uma operadora já decidiu a elegibilidade.
</details>

3. Qual cabeçalho pode indicar onde acompanhar um recurso aceito?

<details>
<summary>Ver resposta</summary>

`Location`. Seu valor deve indicar o recurso relevante para acompanhamento, por exemplo `/elegibilidades/{protocolo}`.
</details>

4. O que significa dizer que uma operação é idempotente?

<details>
<summary>Ver resposta</summary>

Repetir a mesma intenção produz o mesmo efeito pretendido no servidor. Isso não exige que cada resposta seja idêntica nem cria deduplicação automática em uma integração distribuída.
</details>

5. Que artefato descreve paths, operações, schemas, exemplos e respostas de uma API HTTP?

<details>
<summary>Ver resposta</summary>

Um documento OpenAPI. No laboratório, o contrato explícito está em `laboratorios/plataforma-hospitalar/contratos/openapi.yaml`.
</details>

6. Cite duas responsabilidades adequadas a um API gateway.

<details>
<summary>Ver resposta</summary>

Roteamento, terminação TLS, autenticação técnica, limite de tráfego, correlação e telemetria são responsabilidades possíveis. Tradução de vocabulário do laboratório e regras de elegibilidade não devem ser despejadas no gateway.
</details>

## Compreender

1. “A resposta de aceitação usa `202` e inclui `Location`.” Isso é contrato, implementação, evidência ou força do contexto?

<details>
<summary>Ver resposta</summary>

É uma decisão de contrato, porque o consumidor observa o status e o cabeçalho.
</details>

2. “O servidor guarda protocolos em um dicionário Python.” Como classificar essa frase?

<details>
<summary>Ver resposta</summary>

É detalhe de implementação enquanto o comportamento público prometido não muda. Ele também é um limite relevante: reiniciar o processo apaga os protocolos.
</details>

3. Por que `POST /aprovarAutomaticamente` pode ser RPC coerente, mas não deve ser chamado de REST apenas porque usa JSON e HTTP?

<details>
<summary>Ver resposta</summary>

RPC organiza a colaboração por operações nomeadas. REST requer restrições e semântica de recursos, representações e mensagens HTTP; uma URL com HTTP não comprova essas propriedades.
</details>

4. Quando GraphQL pode ajudar mais que uma API de leitura fixa?

<details>
<summary>Ver resposta</summary>

Quando consumidores precisam de combinações de campos e relações muito variáveis. Ainda é necessário controlar custo das consultas, autorização por campo e cache; não é a escolha automática para qualquer tela móvel.
</details>

5. O que WebSocket resolve e o que ele não resolve sozinho?

<details>
<summary>Ver resposta</summary>

Ele mantém um canal bidirecional persistente para atualização em tempo real. Não garante entrega durável, reprocessamento, ordenação de negócio ou recuperação após desconexão; essas políticas precisam ser projetadas.
</details>

6. Por que um adaptador é mais apropriado que o gateway para traduzir SOAP/TISS do laboratório para o vocabulário hospitalar?

<details>
<summary>Ver resposta</summary>

Porque a tradução contém conhecimento da dependência e de seus significados. O gateway pode aplicar políticas técnicas; o adaptador isola mudanças externas e protege o domínio interno da plataforma.
</details>

## Aplicar

**Objetivo**

Verificar, como consumidor do contrato, que a API local de elegibilidades diferencia uma solicitação aceita de uma solicitação incompatível com o contrato.

**Situação**

Antes da baseline, confirme caminho válido, recuperação por protocolo e erro de validação. A prática prova a fronteira HTTP local, não uma decisão real de plano.

**Seu papel**

Você atua como pessoa consumidora e revisora de contrato. Você não altera código, schemas nem o OpenAPI principal; registra evidências que outra pessoa possa repetir.

**Artefato que você irá usar**

`laboratorios/plataforma-hospitalar` contém a **API de elegibilidades da plataforma hospitalar**. `src/hospital/api/main.py` inicia FastAPI; `contratos/openapi.yaml` descreve `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`; `tests/test_api_contract.py` verifica parte da concordância. Dados são sintéticos e ficam em memória.

**Insumos disponíveis**

Use a [oficina de ferramentas](oficina-de-ferramentas.md), Bruno, Spectral, Python e o pedido sintético abaixo:

```json
{
  "cpf": "12345678901",
  "codigo_operadora": "OPS-001",
  "matricula_plano": "MAT-2026-001"
}
```

**Antes de executar**

Abra um terminal na raiz do clone `arquitetura-software` e siga a instalação da [oficina](oficina-de-ferramentas.md#instalacao) para o seu sistema operacional. Entre em `laboratorios/plataforma-hospitalar`, crie `.venv` e instale o pacote. A condição inicial verificável é: `tests/test_api_contract.py` existe, `contratos/openapi.yaml` abre no editor e o comando de teste indicado na oficina encerra sem falhas. Reserve um segundo terminal para o servidor.

**Como conduzir**

Primeiro confirme documento e testes; depois experimente o caminho válido; por fim, provoque uma violação pequena e compare o que cada evidência consegue provar.

**O que fazer**

1. Crie `evidencias-aplicar` dentro de `laboratorios/plataforma-hospitalar`; ela guardará somente seus resultados, sem modificar a baseline.
2. Execute os testes de `tests/test_api_contract.py` conforme o comando da oficina e salve a saída como `evidencias-aplicar/testes-contrato.txt`.
3. Valide `contratos/openapi.yaml` com Spectral e salve a saída.
4. Inicie `src/hospital/api/main.py`; prossiga ao aparecer `http://127.0.0.1:8000`.
5. Em `http://127.0.0.1:8000/docs`, envie o pedido válido e registre `202`, `Location`, `protocolo`, `situacao` e `criado_em`.
6. Consulte esse protocolo com `GET` e compare as duas respostas.
7. Remova apenas `cpf`, envie outro `POST` e registre `422`, `codigo`, `mensagem` e `body.cpf`.
8. Diferencie, em três frases, contrato, execução e limite da memória.

**Evidência esperada**

Há uma saída de teste, uma saída de Spectral, uma resposta `202` com `Location`, uma consulta `200` com o mesmo protocolo, uma resposta `422` estruturada e uma nota que não chama aceitação de aprovação.

**Entrega esperada**

Entregue a pasta `evidencias-aplicar` com os arquivos de saída, três respostas HTTP salvas e a nota de interpretação. Inclua comandos e versões usados para que outra pessoa consiga refazer a prática.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Execução reproduzível | 25% | Evidência: caminho e saída; insuficiência: resultado sem comando. |
| `POST` e `GET` coerentes | 30% | Evidência: protocolo usado; insuficiência: respostas desconectadas. |
| Erro interpretado | 25% | Evidência: `422` e detalhe; insuficiência: só status. |
| Limites precisos | 20% | Evidência: memória declarada; insuficiência: tratar como produção. |

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
