# Seis incrementos cumulativos

Cada incremento atualiza a mesma baseline. Preserve os artefatos anteriores, registre mudanças e mantenha conexões entre contexto, decisão e evidência. Os passos indicam o mínimo esperado; a solução continua aberta a alternativas justificadas.

## Incremento 1 — Estrutura e decisões iniciais

### Objetivo

Delimitar o sistema, priorizar atributos de qualidade e escolher uma estrutura inicial compreensível para as equipes.

### Insumos

Use o [contexto hospitalar](contexto-hospitalar.md), o [catálogo de padrões](../referencia/catalogo-de-padroes.md), os [atributos de qualidade](../referencia/atributos-de-qualidade.md) e as evidências coletadas no encontro de estilos.

### Passos

1. Mapeie pessoas, sistemas externos, responsabilidades e fronteiras.
2. Escreva ao menos três cenários mensuráveis para privacidade, interoperabilidade e disponibilidade.
3. Compare estilos arquiteturais pelas forças do caso, incluindo consequências negativas.
4. Escolha uma estrutura inicial e registre a decisão em ADR.

### Artefato

Crie a versão 1 da baseline com diagrama de contexto, mapa de capacidades, cenários de qualidade e `ADR-001` sobre o estilo inicial.

### Evidência

Mostre que cada elemento do diagrama pertence ao escopo e que a alternativa escolhida responde aos cenários prioritários. Registre dúvidas como suposições verificáveis.

### Conexão com o próximo encontro

A fronteira e os fluxos desta baseline identificam quais interações precisarão de contratos no incremento 2.

## Incremento 2 — Contratos de APIs e integrações externas

### Objetivo

Definir contratos estáveis e compreensíveis para agenda, plano de saúde e laboratório sem acoplar a plataforma aos modelos internos de cada participante.

### Insumos

Parta do diagrama, dos cenários de qualidade e do `ADR-001` produzidos no incremento 1. Use as fronteiras já definidas para evitar criar APIs sem responsabilidade clara.

### Passos

1. Selecione interações síncronas para agenda, elegibilidade e autorização.
2. Modele recursos, operações, estados, erros e identificadores de correlação.
3. Defina um adaptador para o plano de saúde e outro para o laboratório.
4. Registre autenticação, autorização, versionamento, idempotência e limites de tempo.
5. Teste exemplos válidos, recusas e indisponibilidade externa contra os contratos.

### Artefato

Acrescente à baseline contratos de integração, exemplos de requisição e resposta, mapa de erros e `ADR-002` sobre estilo de API e fronteira de adaptação.

### Evidência

Execute validação dos contratos e demonstre que a linguagem da plataforma permanece consistente quando os modelos da operadora ou do laboratório diferem.

### Conexão com o próximo encontro

Operações, estados e responsabilidades expostos pelos contratos orientam limites de serviços, dados e transações no incremento 3.

## Incremento 3 — Limites de serviços, dados e coordenação

### Objetivo

Refinar a solução em unidades responsáveis por capacidades, com propriedade de dados explícita e tratamento consciente de operações distribuídas.

### Insumos

Reutilize a baseline e os contratos validados no incremento 2. Para cada operação, identifique a capacidade responsável, os dados necessários e a consequência de uma falha parcial.

### Passos

1. Agrupe capacidades por coesão e ritmo de mudança antes de nomear serviços.
2. Defina propriedade e compartilhamento de dados para cadastro, agenda, autorização, exames e faturamento.
3. Modele um fluxo distribuído com estados intermediários, repetição, compensação e reconciliação.
4. Compare consistência imediata e eventual com base no impacto observável para cada ator.
5. Atualize os ADRs quando o novo limite alterar uma decisão anterior.

### Artefato

Evolua a baseline com diagrama de contêineres, catálogo de responsabilidades, mapa de propriedade de dados, sequência de falha parcial e `ADR-003` sobre coordenação.

### Evidência

Demonstre com um teste de cenário que a perda temporária da operadora ou do laboratório produz estado conhecido, recuperável e auditável, sem duplicar a ação de negócio.

### Conexão com o próximo encontro

Os limites e contratos agora permitem definir políticas comuns de segurança, evolução e observabilidade no incremento 4.

## Incremento 4 — Governança e operação consistente

### Objetivo

Tornar decisões, políticas e sinais operacionais aplicáveis de forma consistente sem retirar a autonomia necessária de cada serviço.

### Insumos

Use serviços, contratos, propriedade de dados e cenários de falha do incremento 3. Identifique onde duplicação de política gera risco e onde centralização criaria acoplamento.

### Passos

1. Defina políticas mínimas para identidade, autorização, limites de uso e dados sensíveis.
2. Estabeleça regras de evolução e compatibilidade dos contratos.
3. Propague correlação entre plataforma, plano de saúde e laboratório.
4. Escolha logs, métricas e rastros que respondam a perguntas operacionais concretas.
5. Registre exceções, responsáveis, prazo de revisão e evidência de conformidade.

### Artefato

Acrescente à baseline um mapa de políticas, padrão de telemetria, fluxo de exceção, estratégia de evolução e `ADR-004` sobre aplicação de governança.

### Evidência

Reproduza uma requisição entre fronteiras e mostre a correlação no rastro, a aplicação da política e a localização da falha sem depender de inspeção manual em cada componente.

### Conexão com o próximo encontro

Os sinais operacionais e limites governados revelam onde eventos podem reduzir acoplamento e quais garantias precisam ser preservadas no incremento 5.

## Incremento 5 — Colaboração orientada por eventos

### Objetivo

Introduzir comunicação assíncrona somente onde ela melhora o fluxo, tornando entrega, repetição, ordenação e consistência explicitamente observáveis.

### Insumos

Parta dos serviços, políticas e sinais de telemetria validados no incremento 4. Selecione uma interação cuja dependência temporal cause fragilidade, como o andamento de autorização ou a chegada de resultado do laboratório.

### Passos

1. Nomeie eventos como fatos ocorridos e defina produtor, consumidores e dados mínimos.
2. Modele publicação confiável com outbox transacional quando houver mudança de dados associada.
3. Defina consumidor idempotente, tratamento de repetição e destino de mensagens não processáveis.
4. Explicite ordenação, consistência eventual e reconciliação para paciente, faturamento e auditoria.
5. Compare broker e mediator e registre por que a opção escolhida serve ao fluxo.

### Artefato

Evolua a baseline com catálogo e esquema de eventos, sequência temporal, matriz de produtores e consumidores, estratégia de recuperação e `ADR-005` sobre mensageria.

### Evidência

Reproduza entrega repetida e indisponibilidade de um consumidor. Mostre que o estado converge, a ação não é duplicada e a correlação continua visível.

### Conexão com o próximo encontro

O comportamento sob repetição e falha fornece cenários concretos para topologia, capacidade e recuperação em nuvem no incremento 6.

## Incremento 6 — Implantação, resiliência e síntese

### Objetivo

Projetar uma implantação operável que atenda aos cenários prioritários e consolidar a argumentação arquitetural da solução completa.

### Insumos

Use a baseline acumulada, os testes de falha e os sinais observáveis do incremento 5. Recupere as medidas de qualidade definidas no primeiro encontro e verifique se continuam adequadas.

### Passos

1. Mapeie componentes, dados, broker e integrações para uma topologia de implantação.
2. Defina verificação de vida e prontidão, escalabilidade, isolamento e modo degradado.
3. Estabeleça cópia de segurança, restauração, recuperação e reversão de implantação.
4. Relacione alertas a objetivos mensuráveis e a ações de um runbook.
5. Revise todos os ADRs, conflitos entre diagramas e evidências dos seis encontros.

### Artefato

Finalize a baseline com diagrama de implantação, cenários de resiliência, runbook enxuto, plano de capacidade, índice de ADRs e narrativa de evolução arquitetural.

### Evidência

Execute uma verificação reproduzível de implantação e recuperação. Apresente a cadeia contexto → decisão → consequência → evidência para as escolhas mais importantes.

### Conexão com o próximo encontro

O ciclo de encontros termina, mas a baseline permanece evolutiva: riscos não resolvidos, gatilhos de revisão e próximos experimentos formam o plano de continuidade da arquitetura.
