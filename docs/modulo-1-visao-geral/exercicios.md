# Exercícios por Taxonomia de Bloom

Os exercícios avançam de vocabulário para criação de uma baseline. Recordar e Compreender incluem retorno comentado para estudo autônomo. Aplicar, Analisar, Avaliar e Criar exigem que você produza evidências e justifique escolhas; as instruções não pressupõem uma única arquitetura correta.

## Recordar

1. O que diferencia um componente de um conector?
2. Cite os quatro estilos estudados neste módulo.
3. Qual termo descreve uma condição considerada verdadeira, mas ainda sujeita a revisão?
4. Quais partes mínimas conectam um cenário de atributo de qualidade a uma medida?
5. O que um ADR preserva além da alternativa escolhida?
6. Qual estilo organiza transformações independentes conectadas por fluxos?

**Respostas comentadas**

1. Componente é uma unidade de computação ou armazenamento com responsabilidade identificável; conector é o mecanismo de colaboração, como chamada, mensagem ou fluxo.
2. Camadas, pipes and filters, microkernel e monólito modular.
3. Premissa. Uma restrição limita alternativas; uma premissa precisa ser confirmada ou revista.
4. Fonte do estímulo, estímulo, ambiente, artefato, resposta e medida. A medida impede que “rápido” ou “modificável” permaneçam vagos.
5. Contexto, forças, alternativas, consequências, evidências e gatilho de revisão. O ADR conserva o racional, não somente o resultado.
6. Pipes and filters. Cada filtro transforma uma entrada, e cada pipe transporta o resultado para a etapa seguinte.

## Compreender

Leia as afirmações e explique se cada uma descreve estilo, padrão, tecnologia, força ou evidência.

1. “A solução será executada em Python 3.12.”
2. “As regras de negócio não podem importar adaptadores de persistência.”
3. “Uma nova variação deve entrar sem mudar o núcleo.”
4. “O teste cria um plugin e executa o núcleo com outro plugin desabilitado.”
5. “Adapter traduz o modelo externo para o modelo interno.”
6. “A solução é implantada como uma unidade e dividida por capacidades.”

**Respostas comentadas**

1. Python é tecnologia. A frase não define organização nem racional.
2. É uma restrição compatível com camadas; a regra de dependência dá significado ao estilo.
3. É uma força de modificabilidade e extensibilidade. Ainda precisa de cenário e medida.
4. É evidência, pois observa propriedades esperadas do microkernel.
5. Adapter é padrão: resolve uma incompatibilidade de interface contextualizada.
6. Descreve monólito modular: unidade de implantação combinada com fronteiras internas.

Agora compare as frases “usar FastAPI” e “separar entrada, aplicação, domínio e infraestrutura com dependências voltadas para dentro”. A primeira escolhe mecanismo; a segunda declara estrutura e restrição. Uma equipe pode usar FastAPI sem adotar camadas e pode implementar camadas em Java ou .NET.

## Aplicar

**Situação**

A equipe da plataforma hospitalar precisa escolher uma organização inicial para uma capacidade cuja regra muda mensalmente. Há uma validação comum e variações por unidade. A decisão ainda é provisória.

**Seu papel**

Você é responsável por executar o comparador didático, relacionar a saída ao cenário e registrar uma evidência reproduzível.

**Insumos disponíveis**

Use `src/hospital/estilos.py`, `tests/test_estilos.py`, o cenário de modificabilidade em [atributos de qualidade](../referencia/atributos-de-qualidade.md) e o [template de ADR](../referencia/template-adr.md).

**Como conduzir**

1. Ative o ambiente do laboratório e execute `python -m pytest tests/test_estilos.py -q`.
2. Crie um cenário com prioridades `modificabilidade` e `extensibilidade`.
3. Execute `comparar_estilos` e registre estilo, força, limite e evidência da primeira alternativa.
4. Reescreva a necessidade como cenário com estímulo, resposta e medida.
5. Preencha um mini-ADR com ao menos duas alternativas.
6. Declare uma condição que exigiria revisar a escolha.

**Entrega esperada**

Um arquivo com cenário, saída do comparador, comando executado, interpretação, mini-ADR e limite do experimento.

**Critérios de avaliação**

| Critério | Percentual |
| --- | ---: |
| Execução reproduzível e resultado registrado | 25% |
| Cenário de qualidade observável | 25% |
| Relação coerente entre força, alternativa e limite | 30% |
| ADR com consequência e gatilho de revisão | 20% |

## Analisar

**Situação**

Agenda, triagem administrativa e faturamento fazem parte da mesma plataforma, mas apresentam concorrência, variação e processamento em lote. Uma proposta aplica microkernel a todas as capacidades para “padronizar a arquitetura”.

**Seu papel**

Você atua como analista de arquitetura e precisa decompor a proposta, identificar onde as forças diferem e comparar alternativas pelas mesmas dimensões.

**Insumos disponíveis**

Use o [contexto hospitalar](../projeto-integrador/contexto-hospitalar.md), a matriz do estudo de caso, os quatro estilos e os cenários de qualidade compartilhados. Considere somente informações administrativas.

**Como conduzir**

1. Identifique estímulo, resposta e medida para cada capacidade.
2. Liste componentes, conectores e restrições sugeridos pela proposta global.
3. Compare microkernel, camadas, pipes and filters e monólito modular para cada capacidade.
4. Marque tensões entre consistência, modificabilidade, throughput e simplicidade operacional.
5. Desenhe em Mermaid uma estrutura combinada ou uma alternativa única.
6. Escreva duas hipóteses que ainda precisam de evidência.

**Entrega esperada**

Uma matriz comparativa, um diagrama Mermaid com leitura textual e uma análise de até mil palavras que explique diferenças entre as três capacidades.

**Critérios de avaliação**

| Critério | Percentual |
| --- | ---: |
| Decomposição correta de forças e capacidades | 25% |
| Comparação simétrica de estilos e limites | 30% |
| Coerência entre diagrama, conectores e texto | 25% |
| Hipóteses e evidências necessárias explícitas | 20% |

## Avaliar

**Situação**

Duas equipes apresentaram propostas para a baseline. A primeira usa um monólito modular com estilos internos por capacidade. A segunda cria unidades de implantação separadas desde o início. Ambas afirmam melhorar modificabilidade, mas ainda não demonstraram carga nem cadência independente.

**Seu papel**

Você integra uma revisão técnica e deve recomendar uma proposta, rejeitar ambas ou aprovar uma experiência limitada antes da decisão.

**Insumos disponíveis**

Considere equipe pequena, operação inicial local, necessidade de rastreabilidade, indisponibilidade eventual de parceiros, frequência de mudança desconhecida e os artefatos do módulo. Use o [modelo de entrega](../projeto-integrador/modelos-de-entrega.md) para conferir rastreabilidade.

**Como conduzir**

1. Defina cinco critérios antes de comparar as propostas.
2. Atribua evidência disponível, ausente ou contraditória para cada critério.
3. Examine consequências favoráveis e desfavoráveis das duas propostas.
4. Faça uma recomendação condicionada, sem apresentar preferência pessoal como força.
5. Defina duas experiências reproduzíveis e um gatilho de revisão.
6. Registre opiniões divergentes como alternativa, não como erro.

**Entrega esperada**

Um parecer arquitetural com tabela de critérios, recomendação argumentada, incertezas, experiências e relação com o ADR-001.

**Critérios de avaliação**

| Critério | Percentual |
| --- | ---: |
| Critérios definidos antes da recomendação | 20% |
| Uso honesto de evidências e incertezas | 25% |
| Consequências e restrições comparadas | 25% |
| Recomendação coerente e revisável | 20% |
| Experiências alinhadas às forças | 10% |

## Criar

**Situação**

O grupo iniciará o [incremento 1](../projeto-integrador/incrementos.md#incremento-1-estrutura-e-decisoes-iniciais). A baseline precisa orientar os próximos encontros sem antecipar APIs, serviços, eventos ou infraestrutura que ainda não foram justificados.

**Seu papel**

Você coordena a criação de uma descrição arquitetural inicial que outra equipe possa compreender, executar e revisar.

**Insumos disponíveis**

Use mapa de atores e capacidades, atributos de qualidade, estilos, resultado da oficina, Structurizr DSL, Mermaid e template de ADR. Preserve triagem, agenda, faturamento e auditoria no escopo administrativo.

**Como conduzir**

1. Delimite sistema, atores, sistemas externos e responsabilidades fora de escopo.
2. Escreva três cenários mensuráveis, incluindo modificabilidade e mais dois atributos.
3. Crie uma matriz com ao menos três alternativas e as mesmas forças.
4. Modele contexto e contêineres em Structurizr DSL.
5. Modele em Mermaid uma sequência com caminho normal e falha.
6. Registre ADR-001 com decisão, consequências, evidências e revisão.
7. Execute o teste do laboratório e conecte a saída à decisão sem tratá-la como seleção automática.
8. Faça uma revisão cruzada entre diagrama, ADR, cenários e evidências.

**Entrega esperada**

Uma pasta versionável com cenários, matriz, `workspace.dsl`, diagrama de sequência, ADR-001, resultado de teste e índice que explique a ligação entre artefatos.

**Critérios de avaliação**

| Critério | Percentual |
| --- | ---: |
| Delimitação e cenários mensuráveis | 20% |
| Alternativas e consequências comparáveis | 20% |
| Modelos consistentes e compreensíveis | 20% |
| ADR rastreável às forças | 20% |
| Evidências reproduzíveis e limites declarados | 15% |
| Revisão cruzada e organização da entrega | 5% |
