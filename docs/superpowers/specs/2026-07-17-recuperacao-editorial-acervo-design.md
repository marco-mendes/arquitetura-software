# Recuperação editorial do acervo de Arquitetura de Software

## Objetivo

Reintegrar ao site didático os conceitos, diagramas, exemplos e estudos de caso relevantes do acervo original da disciplina, sem produzir páginas que pareçam uma colagem de documentos legados. O resultado deve permanecer uma narrativa única, progressiva e orientada a arquitetos iniciantes.

## Resultado para o aluno

Cada uma das seis unidades apresenta, no próprio fluxo do módulo, os conceitos necessários para compreender as decisões seguintes. O aluno não precisa conhecer o nome de um arquivo legado, inferir o significado de um artefato do repositório ou executar comandos sem saber sua finalidade e seu resultado esperado.

O acervo original é fonte editorial interna. O site não mostrará rótulos como “conteúdo recuperado”, “material legado” ou equivalentes.

## Organização conceitual

### Unidade 1 — Visão geral de estilos arquiteturais

Reconstituir o mapa de quatro famílias: monolítica, distribuída por domínio, integração e comunicação, e infraestrutura. Explicar no fluxo principal Camadas, MVC, Hexagonal, Microkernel, Pipes and Filters, DDD, microsserviços, APIs, eventos, nuvem e contêineres. Diferenciar antecipação de aprofundamento: DDD, microsserviços, APIs, eventos e nuvem são apresentados como mapa e retomados com profundidade nas unidades seguintes.

Integrar as explicações e diagramas de Camadas, Pipes and Filters e Microkernel, incluindo forças, variações, anti-padrões e critérios de uso. A figura de estilos existente pode permanecer como síntese visual, desde que a explicação textual cubra cada estilo efetivamente apresentado.

### Unidade 2 — Arquitetura de APIs

Incorporar o material sobre estilo de APIs, tipos e protocolos, processo de construção, plataforma de APIs, gateway, cenários de gateway, tecnologias e modelagem hospitalar. Comparar REST, GraphQL, gRPC, WebSocket e HTTP de modo arquitetural: contrato, acoplamento, semântica, capacidade e limites; não como catálogo de ferramentas.

### Unidade 3 — Arquitetura de serviços

Incorporar introdução e aprofundamento de microsserviços, persistência, consistência eventual, CAP, SAGA, CQRS, event sourcing, padrões de adoção, Netflix, estrangulador, chassi arquitetural, macrosserviços e desafios distribuídos. Explicitar quando cada conceito é alternativa, restrição ou consequência, e não uma recomendação automática.

### Unidade 4 — Governança de serviços

Ampliar a base de governança com mediação, gateway, políticas, versionamento, observabilidade, rastreabilidade e controles de fronteira. O conteúdo deve ligar governança a contratos, operação e autonomia de times, não apenas a produtos de gateway.

### Unidade 5 — Arquiteturas de eventos

Incorporar EDA, broker, mediator, topologias, payloads, processamento, boas práticas, limitações, Kafka e comparação com ActiveMQ ou RabbitMQ. Manter a ênfase em contratos, idempotência, ordem, falha, DLQ e evidências de operação.

### Unidade 6 — Arquiteturas de nuvens

Incorporar modelos IaaS, PaaS e SaaS, on-premise, AWS como exemplo contextualizado, contêineres, orquestração, iFood e Taco Bell. Distinguir modelo de serviço, forma de implantação e mecanismo operacional; exemplos de fornecedor não podem ser tratados como arquitetura universal.

## Figuras e diagramas

Uma figura é integrada apenas quando responde a uma pergunta didática concreta. Imagens externas frágeis, sem fonte verificável ou com baixo contraste não são incorporadas por inércia. Quando a informação for estrutural, o diagrama será refeito em Mermaid ou outro formato acessível e alinhado ao visual Academia.

Toda figura terá:

- texto alternativo útil;
- legenda que explica sua função no argumento;
- leitura textual imediatamente associada;
- fonte quando for figura externa ou adaptação identificável.

## Exercícios e oficinas

### Recordar e Compreender

Cada pergunta terá sua própria resposta expansível com o padrão:

```html
<details>
<summary>Ver resposta</summary>

Resposta comentada.
</details>
```

O aluno formula a resposta antes de abrir o bloco. As respostas corrigem vocabulário e interpretação; não substituem atividades de decisão arquitetural.

### Aplicar, Analisar, Avaliar e Criar

Cada atividade é auto-contida e segue a ordem abaixo:

1. **Objetivo:** capacidade a desenvolver e decisão arquitetural em foco.
2. **Situação:** contexto, restrições e dados disponíveis.
3. **Seu papel:** responsabilidade assumida pelo aluno.
4. **Artefato que você irá usar:** nome, finalidade, caminho no repositório e limites do artefato.
5. **Antes de executar:** condição inicial, preparação necessária e sinal verificável para continuar.
6. **O que fazer:** passos ordenados; cada comando ou manipulação declara intenção e resultado observável.
7. **Evidência esperada:** saídas, arquivos, comparações ou justificativas que demonstram a aprendizagem.
8. **Entrega e critérios de avaliação:** artefato final, percentual, evidência de atendimento e condição de insuficiência.

Termos que ainda não foram apresentados — por exemplo, baseline, contrato, endpoint, protocolo, corpus ou idempotência — são definidos no ponto de uso ou recebem link para a definição exata. Nenhuma instrução diz apenas “execute”, “compare” ou “acrescente” sem dizer onde, por quê e o que observar.

## Rastreabilidade interna

Manter uma matriz privada de trabalho que associe cada capítulo fonte ao conceito e à página canônica que o absorve. A matriz serve a revisão editorial e testes, mas não aparece na navegação pública nem cria uma experiência de acervo migrado.

## Critérios de aceitação

- Todos os capítulos conceituais do acervo original têm destino editorial explícito ou justificativa documentada de consolidação/remoção por redundância, obsolescência ou fragilidade de fonte.
- As unidades 1 a 6 incorporam conceitos sem duplicar explicações literais entre módulos.
- Recordar e Compreender usam resposta expansível por pergunta.
- Atividades avançadas e oficinas identificam artefato, caminho, estado inicial, intenção, resultado observável e evidência esperada.
- Figuras mantidas ou criadas possuem acessibilidade e leitura textual.
- O site continua a atender aos contratos de navegação, Bloom, critérios de avaliação e build estrito.

## Fora de escopo

- Copiar documentos legados integralmente para o site.
- Converter a disciplina em certificação de tecnologias ou fornecedores.
- Inserir imagens somente para decorar páginas.
- Publicar gabaritos para atividades arquiteturais de níveis avançados.
