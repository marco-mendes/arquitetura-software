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

Uma rede de laboratórios regionais precisa enviar resultados administrativos para uma central de vigilância. Dezoito parceiros produzem JSON, CSV ou XML, com convenções próprias. Juntos, enviam quatro milhões de registros por dia e chegam a seiscentos registros por segundo durante duas horas. Layouts mudam, em média, duas vezes por mês. Há registros repetidos ou fora de ordem, e uma auditoria deve reconstruir origem, versão do contrato, transformações e motivo de rejeição. O prazo para disponibilizar um lote aceito é vinte minutos.

**Seu papel**

Você atua como analista de arquitetura e precisa decompor ingestão, tradução, validação, deduplicação e auditoria antes de comparar organizações possíveis.

**Insumos disponíveis**

Considere os fatos da situação, uma equipe de cinco pessoas, implantação inicial operada como uma unidade e estes dados sintéticos: três exemplos válidos por formato, dois registros repetidos, um registro atrasado e duas versões do layout de um parceiro. Segurança clínica não está em escopo; identifique os registros apenas por códigos fictícios. Use somente esses fatos e as definições compartilhadas de [atributos de qualidade](../referencia/atributos-de-qualidade.md).

**Como conduzir**

1. Separe forças de throughput, variação por parceiro, ordenação, deduplicação e rastreabilidade.
2. Formule três cenários mensuráveis com ambiente, resposta e medida.
3. Modele pelo menos duas decomposições alternativas, nomeando componentes, conectores e estado.
4. Compare camadas, pipes and filters, microkernel e monólito modular pelas mesmas forças, sem exigir que um único estilo organize todas as escalas.
5. Analise como cada alternativa identifica versão, repetição, atraso e rejeição.
6. Desenhe em Mermaid uma alternativa e uma sequência de falha parcial.
7. Registre três hipóteses e a evidência capaz de confirmá-las ou refutá-las.

**Entrega esperada**

Uma matriz comparativa, dois cenários de estrutura, um diagrama Mermaid com leitura textual e uma análise de até mil palavras sobre forças, estado, falhas e incertezas.

**Critérios de avaliação**

| Critério | Percentual |
| --- | ---: |
| Decomposição correta de forças e etapas | 25% |
| Comparação simétrica de estilos e limites | 30% |
| Coerência entre diagrama, conectores e texto | 25% |
| Hipóteses e evidências necessárias explícitas | 20% |

## Avaliar

**Situação**

Uma secretaria estadual consolida disponibilidade de leitos administrativos enviada por quarenta e cinco hospitais. Vinte e oito parceiros publicam JSON a cada trinta segundos; dezessete enviam CSV a cada cinco minutos. O pico é novecentas atualizações por minuto. Mensagens podem repetir, atrasar ou contradizer a versão anterior. O painel deve refletir a atualização aceita mais recente em até sessenta segundos, e a auditoria precisa explicar fonte, versão, transformação e regra de desempate. Os formatos mudaram seis vezes no último trimestre.

**Seu papel**

Você integra uma revisão técnica e deve avaliar duas propostas, recomendar uma delas, rejeitar ambas ou autorizar uma experiência limitada. Não há alternativa previamente aprovada.

**Insumos disponíveis**

Considere uma equipe de seis pessoas e uma única equipe operacional. A proposta A mantém conectores por parceiro, um modelo canônico e uma sequência compartilhada de transformações na mesma implantação. A proposta B implanta um coletor por parceiro e envia atualizações canônicas a um processador comum. Nenhuma equipe mediu carga, custo de operação ou tempo de inclusão de parceiro. Use uma amostra sintética com mil atualizações, cinquenta repetições, vinte atrasos e cinco contradições.

**Como conduzir**

1. Transforme atualização, variação, repetição, atraso, auditoria e operação em critérios mensuráveis.
2. Atribua evidência disponível, ausente ou contraditória para cada critério.
3. Relacione cada proposta a estilos possíveis sem inferir adequação somente pelo nome.
4. Examine consequências favoráveis e desfavoráveis, inclusive isolamento de falha e esforço operacional.
5. Faça uma recomendação condicionada ou proponha adiar a decisão, sustentando-a pelos critérios.
6. Defina duas experiências reproduzíveis com a amostra fornecida e um gatilho de revisão.
7. Registre a principal objeção à sua conclusão e como nova evidência poderia alterá-la.

**Entrega esperada**

Um parecer arquitetural com tabela de critérios, recomendação condicionada, incertezas, objeção principal, experiências e gatilho de revisão.

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
