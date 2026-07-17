# Especificação do site da disciplina de Arquitetura de Software

## 1. Propósito

Transformar o repositório atual em um site didático completo para uma disciplina de pós-graduação com 24 horas, distribuídas em seis encontros de quatro horas. O novo site deve preservar o conteúdo útil já existente, mas reorganizá-lo para conduzir profissionais de desenvolvimento que dominam tecnologias como .NET, Java ou Python e ainda não possuem uma base sistemática em arquitetura de software.

O resultado deve combinar formação conceitual, contato com ferramentas reais, práticas locais reproduzíveis e um projeto integrador progressivo. O site será publicado pelo GitHub Pages com MkDocs Material e deverá continuar legível diretamente no GitHub.

## 2. Público e princípios pedagógicos

### 2.1 Público

- estudantes de pós-graduação;
- desenvolvedores, analistas e especialistas técnicos;
- experiência prévia em implementação com .NET, Java ou Python;
- pouca ou nenhuma formação estruturada em conceitos arquiteturais.

### 2.2 Princípios

1. **Conceito antes do caso:** cada módulo apresenta vocabulário, problema e mecanismos antes de pedir análise ou decisão.
2. **Condução explícita:** atividades informam contexto, artefato de entrada, local da alteração, sequência de passos, resultado esperado e forma de verificação.
3. **Complexidade progressiva:** lembrar e compreender preparam aplicar; aplicar prepara analisar; avaliar aparece somente depois de critérios e evidências terem sido ensinados.
4. **Decisão com evidência:** estudantes comparam alternativas por atributos de qualidade, restrições, riscos e consequências observáveis.
5. **Ferramentas a serviço do conceito:** toda ferramenta é apresentada pelo problema que ajuda a observar, e não como uma lista isolada de produtos.
6. **Prática local e aberta:** toda oficina obrigatória deve poder ser executada localmente com ferramentas open source, sem depender de serviço comercial.
7. **Equivalência entre ecossistemas:** Python será a implementação de referência; páginas conceituais e oficinas indicarão equivalentes em Java e .NET quando isso ajudar o estudante a transferir o aprendizado.
8. **Separação entre aluno e professor:** o site público contém instruções e critérios de avaliação; respostas, decisões didáticas e roteiros de condução ficam fora da publicação.

## 3. Roteirização da disciplina

| Encontro | Tema | Resultado principal |
| --- | --- | --- |
| 1 | Visão Geral de Estilos Arquiteturais | Reconhecer estilos, relacioná-los a atributos de qualidade e registrar uma decisão inicial. |
| 2 | Arquitetura de APIs | Projetar e validar um contrato de API para uma integração hospitalar. |
| 3 | Arquitetura de Serviços | Delimitar serviços, dados e interações sem confundir distribuição com boa modularidade. |
| 4 | Governança de Serviços | Aplicar políticas, observabilidade e controles operacionais a serviços existentes. |
| 5 | Arquiteturas de Eventos | Modelar eventos, consumidores, entrega, idempotência e consistência eventual. |
| 6 | Arquiteturas de Nuvens | Relacionar implantação, elasticidade, resiliência e operação à arquitetura construída. |

Cada encontro utilizará uma organização de quatro horas com abertura e recuperação, exposição conceitual dialogada, exemplo arquitetural, oficina guiada, discussão de evidências, aplicação ao projeto integrador e fechamento. O material do professor definirá a distribuição exata de tempo e permitirá selecionar quais extensões serão executadas em cada turma.

## 4. Caso integrador

O fio condutor será uma **plataforma hospitalar com integração a planos de saúde e laboratórios**. O domínio deve ser suficientemente concreto para dar significado às decisões, sem exigir conhecimento clínico especializado.

### 4.1 Capacidades iniciais

- cadastro e identificação de pacientes;
- agendamento e atendimento;
- solicitação e consulta de exames laboratoriais;
- verificação de elegibilidade e autorização junto a planos de saúde;
- faturamento e acompanhamento de contas;
- notificação de mudanças relevantes;
- auditoria de integrações e decisões.

### 4.2 Evolução por encontro

1. comparar estilos e criar o primeiro contexto arquitetural;
2. definir contratos síncronos para elegibilidade e pedidos de exame;
3. delimitar serviços, responsabilidades e propriedade dos dados;
4. aplicar políticas de acesso, limites, rastreabilidade e observabilidade;
5. introduzir eventos para resultados, autorizações e faturamento;
6. definir topologia de implantação, resiliência, escalabilidade e operação.

O projeto final consolidará os incrementos em uma proposta arquitetural coerente. Cada entrega deverá reaproveitar evidências produzidas nas oficinas, evitando um trabalho final desconectado das aulas.

## 5. Arquitetura da informação

O conteúdo público será organizado sob `docs/`:

```text
docs/
├── index.md
├── comecar/
├── modulo-1-visao-geral/
├── modulo-2-apis/
├── modulo-3-servicos/
├── modulo-4-governanca/
├── modulo-5-eventos/
├── modulo-6-nuvem/
├── projeto-integrador/
├── referencia/
├── sobre/
├── assets/
└── superpowers/
```

Cada módulo terá uma navegação previsível:

1. visão do encontro e objetivos;
2. conceitos fundamentais;
3. padrões, decisões e atributos de qualidade;
4. exemplos em Python e equivalências em Java/.NET;
5. aplicação ao caso hospitalar;
6. exemplo arquitetural completo;
7. oficina de ferramentas;
8. exercícios por objetivos de aprendizagem;
9. síntese e preparação para o próximo encontro.

## 6. Transição e preservação do material atual

A migração será incremental. Os arquivos Markdown atuais na raiz não serão removidos durante a primeira versão do novo site. O conteúdo relevante será revisado e incorporado às páginas canônicas sob `docs/`, mantendo os documentos antigos disponíveis para que links externos e referências já distribuídas continuem funcionando.

O `README.md` da raiz passará a apresentar o curso e apontará para o site, mas conservará uma seção de compatibilidade com os documentos legados. Nenhum arquivo atual será apagado até que uma auditoria de cobertura confirme a migração e o professor autorize a retirada.

Quando houver conteúdo duplicado, a página canônica será identificada no documento antigo. Links internos novos sempre apontarão para a estrutura `docs/`.

## 7. Padrão didático das páginas

### 7.1 Conceitos

Termos são definidos no primeiro uso, com exemplo e contraponto. Expressões como fronteira, contrato, idempotência, consistência eventual, telemetria ou plano de controle não podem aparecer como pré-requisitos implícitos. Cada conceito relevante deve responder:

- qual problema nomeia ou resolve;
- como se manifesta na arquitetura;
- o que o estudante deve observar;
- quais limites ou trade-offs possui;
- quais ferramentas ajudam a torná-lo visível.

### 7.2 Ferramentas no texto conceitual

As páginas devem citar ferramentas reais junto ao conceito correspondente. Exemplos: FastAPI e Spring Boot ao apresentar APIs; OpenAPI, Bruno e Spectral ao discutir contratos; Kong ao tratar gateways e políticas; OpenTelemetry e Jaeger ao explicar rastreabilidade; RabbitMQ e Kafka ao comparar mensageria; Docker e kind ao introduzir implantação e orquestração.

As menções não substituem a explicação. Cada ferramenta deve ter nome, finalidade e relação explícita com a decisão arquitetural discutida.

### 7.3 Exercícios e Taxonomia de Bloom

Os exercícios serão agrupados por resultados de aprendizagem, sem transformar todos os níveis em uma obrigação de aula. O professor poderá escolher o subconjunto adequado ao ritmo da turma.

- **Lembrar e compreender:** identificar, explicar e classificar com apoio direto do texto.
- **Aplicar:** seguir um procedimento conhecido em um cenário delimitado.
- **Analisar:** comparar evidências usando dimensões e perguntas fornecidas.
- **Avaliar:** recomendar uma alternativa com critérios previamente ensinados.
- **Criar:** reservado principalmente aos incrementos do projeto integrador.

Todo enunciado de aplicar, analisar ou avaliar deve conter cenário, insumos, passos, artefato esperado, localização do trabalho e indícios de conclusão. O estudante não será solicitado a “desenhar fronteiras”, “avaliar governança” ou “propor uma arquitetura” sem uma definição operacional, um ponto de partida e critérios.

### 7.4 Critérios de avaliação

O termo público será **critérios de avaliação**, e não “rubrica”. A avaliação usará percentuais sem pontos. Cada critério explicará em linguagem direta:

- o que será observado;
- quais evidências demonstram atendimento;
- o que caracteriza uma entrega insuficiente;
- qual percentual representa no trabalho.

## 8. Oficinas executáveis

Todas as oficinas obrigatórias devem funcionar em Windows, macOS e Linux. Cada uma terá objetivo, duração estimada, pré-requisitos, instalação por sistema operacional, verificação da instalação, arquivos utilizados, comandos copiáveis, resultado esperado, diagnóstico de erros comuns, experimentos graduais e questões exploratórias.

| Módulo | Prática de referência | Ferramentas principais |
| --- | --- | --- |
| 1 | Comparar estruturas e registrar uma decisão arquitetural | Python, pytest, Mermaid e Structurizr Lite |
| 2 | Implementar, chamar e validar uma API hospitalar | FastAPI, OpenAPI, Bruno ou `curl`, Spectral |
| 3 | Separar serviços e testar contratos e persistência | FastAPI, Docker Compose, PostgreSQL, testes de contrato |
| 4 | Aplicar políticas e seguir uma requisição distribuída | Kong em modo declarativo, OpenTelemetry, Jaeger |
| 5 | Publicar, consumir e repetir eventos com segurança | RabbitMQ como trilha principal; Kafka como comparação/extensão |
| 6 | Implantar, observar falha e executar recuperação local | Docker, kind, Kubernetes, health checks e rollback |

As oficinas utilizarão um repositório de código progressivo para o caso hospitalar. Python será a trilha executável oficial. Quadros de equivalência indicarão bibliotecas ou comandos correspondentes em ASP.NET Core e Spring Boot, sem exigir três implementações completas de cada laboratório.

Experimentos opcionais deverão estar claramente marcados como extensão. O professor poderá decidir em aula quais serão executados, e o estudante conseguirá distinguir o percurso essencial das explorações adicionais.

## 9. Projeto integrador e avaliação

O projeto será desenvolvido em seis incrementos, um por encontro, e culminará em um dossiê arquitetural enxuto:

- contexto, usuários, sistemas externos e restrições;
- decisões de estilo e respectivos atributos de qualidade;
- contratos de API relevantes;
- fronteiras de serviço e responsabilidade pelos dados;
- políticas de governança e sinais operacionais;
- eventos, consumidores e tratamento de repetição/falha;
- topologia de nuvem, escalabilidade e recuperação;
- ADRs com alternativas, decisão, consequências e evidências.

Os critérios de avaliação serão amplos o bastante para não prescrever uma única solução, mas explícitos o bastante para orientar iniciantes. A soma dos percentuais será sempre 100%, validada automaticamente.

## 10. Material do professor

O diretório `material-professor/` ficará ignorado pelo Git público. Ele conterá:

- roteiro minuto a minuto de cada encontro;
- objetivos essenciais e extensões opcionais;
- preparação e teste prévio das oficinas;
- respostas esperadas e erros diagnósticos;
- perguntas de mediação e pontos de parada;
- critérios de avaliação detalhados;
- solução de referência do projeto integrador;
- alternativas para turmas com ritmos ou ambientes distintos.

As páginas públicas não devem revelar respostas de exercícios nem decisões reservadas à condução docente. Testes automatizados verificarão essa separação.

## 11. Design visual e acessibilidade

O site seguirá a linguagem visual **Academia** já aprovada na disciplina de Arquitetura de Soluções com IA Generativa: tipografia editorial, alto contraste, navegação clara, hierarquia consistente e uso comedido de cores acadêmicas.

Os conceitos centrais receberão infográficos didáticos em português gerados especificamente para o curso. Diagramas de relações estruturais poderão usar imagens estilizadas; sequências, fluxos e modelos que se beneficiem de edição e precisão usarão Mermaid. Toda imagem ou diagrama terá texto alternativo e uma explicação textual equivalente próxima, para acessibilidade e leitura no GitHub.

A formatação Markdown privilegiará parágrafos curtos, listas separadas corretamente, tabelas legíveis e blocos de código com instruções antes e verificação depois. Uma folha de estilo específica poderá refinar o tema sem comprometer a renderização padrão do GitHub.

## 12. Plataforma técnica e publicação

- MkDocs com Material for MkDocs;
- configuração central em `mkdocs.yml`;
- navegação explícita por encontro;
- extensões Markdown estritamente necessárias;
- Mermaid integrado ao tema;
- CSS e JavaScript versionados em `docs/assets/`;
- GitHub Actions para validar e publicar no GitHub Pages;
- dependências Python fixadas em arquivo próprio;
- instruções locais de visualização no `README.md`.

A construção do site deverá falhar quando houver links inválidos, configuração inconsistente ou problemas detectáveis de conteúdo. Arquivos internos de planejamento e material docente não entrarão na navegação pública.

## 13. Garantia de qualidade

A validação automatizada cobrirá:

- presença dos seis módulos e seções obrigatórias;
- links internos e arquivos referenciados;
- imagens, textos alternativos e equivalentes textuais;
- estrutura mínima das oficinas e instruções para Windows, macOS e Linux;
- definição de conceitos antes do uso em exercícios;
- enunciados explícitos para aplicar, analisar e avaliar;
- uso de “critérios de avaliação” e ausência de “rubrica” nas páginas públicas;
- percentuais de avaliação totalizando 100%;
- comandos e testes dos códigos de referência;
- separação entre conteúdo público e material do professor;
- construção estrita do MkDocs.

Além dos testes automáticos, cada módulo terá revisão visual no site construído e uma execução limpa da oficina em ambiente documentado.

## 14. Estratégia de implementação

A implementação ocorrerá em etapas verificáveis:

1. criar a fundação MkDocs, o tema Academia e os validadores;
2. estabelecer o caso hospitalar, o projeto integrador e o padrão de módulo;
3. migrar e reescrever um módulo por vez, preservando os arquivos legados;
4. construir e testar a oficina correspondente antes de avançar;
5. produzir e indexar os recursos visuais de cada módulo;
6. criar o material privado do professor em paralelo ao conteúdo público;
7. auditar cobertura, links, acessibilidade e respostas indevidamente expostas;
8. ativar a publicação no GitHub Pages após a validação integral.

O plano detalhado deverá dividir o trabalho em pequenas entregas com testes definidos antes das alterações e checkpoints de revisão após a fundação, os três primeiros módulos, os três últimos módulos e a publicação.

## 15. Critérios de aceite

O trabalho será considerado concluído quando:

- o site representar os seis encontros e as 24 horas da disciplina;
- um arquiteto iniciante conseguir seguir conceitos, exemplos e oficinas sem depender de instruções orais omitidas;
- todas as oficinas essenciais forem reproduzíveis localmente nos três sistemas operacionais suportados;
- o caso hospitalar evoluir de forma coerente ao longo dos módulos;
- o projeto final reutilizar as evidências produzidas em aula;
- os conteúdos atuais permanecerem acessíveis durante a transição;
- o material docente estiver separado da publicação;
- testes, validação de conteúdo e construção estrita passarem;
- o GitHub Pages publicar a versão aprovada do site.
