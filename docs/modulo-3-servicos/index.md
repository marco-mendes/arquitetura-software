# Arquitetura de Serviços

Um sistema não se torna bem arquitetado porque foi dividido em muitos executáveis. Antes de distribuir software, precisamos descobrir responsabilidades que façam sentido para o negócio, manter juntas as regras que mudam juntas e tornar explícitas as dependências inevitáveis. Este módulo começa pela decomposição lógica e só depois chega à distribuição física.

O caso condutor é uma plataforma hospitalar. A capacidade de negócio **verificar elegibilidade** responde se um beneficiário pode utilizar o plano. A capacidade **solicitar exames** registra uma intenção clínica depois de consultar aquela decisão. Elas se relacionam, mas não possuem os mesmos dados nem o mesmo ciclo de mudança. Essa diferença permite discutir limites sem fingir que cada limite precisa virar um microsserviço.

## Pergunta orientadora

Como separar capacidades e dados sem transformar uma operação local simples em uma cadeia remota frágil?

Ao final, você será capaz de justificar uma fronteira de serviço, comparar monólito modular, macrosserviço e microsserviço, explicar banco por serviço, reconhecer falhas parciais e escolher deliberadamente um modelo de consistência. Também executará dois processos FastAPI com dois PostgreSQL isolados por Docker Compose e observará o que ocorre quando uma dependência síncrona para.

## Percurso de aprendizagem

1. Em [Conceitos](conceitos.md), partimos de capacidade de negócio, bounded context, coesão e acoplamento.
2. Em [Padrões e decisões](padroes-e-decisoes.md), comparamos unidades de implantação, propriedade de dados, CAP, SAGA e CQRS.
3. Em [Exemplo arquitetural](exemplo-arquitetural.md), acompanhamos uma solicitação de exame pelos dois serviços.
4. Em [Estudo de caso](estudo-de-caso.md), avaliamos uma decomposição excessiva e uma consolidação responsável.
5. Na [Oficina de ferramentas](oficina-de-ferramentas.md), executamos, interrompemos e limpamos o ambiente.
6. Em [Exercícios](exercicios.md), avançamos pelos seis níveis da Taxonomia de Bloom.
7. Em [Síntese e referências](sintese-e-referencias.md), consolidamos heurísticas e fontes públicas.

```mermaid
flowchart LR
    A[Capacidades do negócio] --> B[Limites lógicos]
    B --> C[Propriedade dos dados]
    C --> D[Forma de implantação]
    D --> E[Comunicação e falhas]
    E --> F[Consistência e operação]
```

**Texto alternativo:** percurso que parte de capacidades de negócio, passa por limites e propriedade de dados, e chega à implantação, às falhas, à consistência e à operação.

*Figura 1 — Percurso de decisão para arquitetura de serviços. Fonte: curso.*

**Leitura textual da figura:** o percurso começa pelas capacidades, define limites e propriedade dos dados, escolhe a forma de implantação e somente então trata comunicação, falhas, consistência e operação.

## O que não será presumido

Microsserviços não são objetivo em si. Um limite de domínio pode existir dentro de um único processo. Um serviço não precisa usar tecnologia diferente dos vizinhos. Uma chamada REST não elimina acoplamento. Um banco por serviço não obriga persistência poliglota. Consistência eventual não resolve automaticamente transações distribuídas. SAGA e CQRS são opções com custos, não etapas obrigatórias de uma arquitetura moderna.

O laboratório usa duas aplicações pequenas para tornar a fronteira visível, não para afirmar que esse seja o desenho ideal de qualquer hospital. Em produção, segurança, privacidade, autorização, observabilidade, recuperação e gestão de segredos exigiriam decisões adicionais. Aqui, dados sintéticos e credenciais estritamente locais mantêm o foco na arquitetura.

## Critério central de decisão

Prefira o menor grau de distribuição que preserve a autonomia realmente necessária. Se duas áreas mudam juntas, pertencem ao mesmo time e precisam de uma única transação, uma fronteira interna forte pode ser superior a uma chamada de rede. Se possuem ritmos de entrega, escalabilidade, risco ou propriedade distintos, processos separados podem pagar seu custo. A resposta nasce do contexto e deve ser registrada como decisão arquitetural revisável.
