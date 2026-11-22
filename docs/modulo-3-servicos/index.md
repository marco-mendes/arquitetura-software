# Arquitetura de Serviços

Um sistema não se torna bem arquitetado porque foi dividido em muitos executáveis. Antes de distribuir software, a equipe precisa descobrir responsabilidades que façam sentido para o negócio e manter juntas as regras que mudam pelo mesmo motivo. Este módulo trata primeiro da decomposição lógica dessas responsabilidades e depois da distribuição física em serviços, bancos e contêineres.

O caso condutor do módulo é uma plataforma hospitalar com duas capacidades de negócio relacionadas. A capacidade **verificar elegibilidade** responde se um beneficiário pode utilizar o plano de saúde. A capacidade **solicitar exames** registra uma intenção clínica depois de consultar essa decisão de elegibilidade. As duas capacidades se relacionam sem compartilhar os mesmos dados ou o mesmo ciclo de mudança, o que permite discutir limites de serviço sem supor que cada limite exige um microsserviço.

## Pergunta orientadora

Como separar capacidades e dados sem transformar uma operação local simples em uma cadeia remota frágil?

Ao final do módulo, você será capaz de justificar uma fronteira de serviço e de comparar monólito modular, macrosserviço e microsserviço. Também será capaz de explicar o banco por serviço, de reconhecer falhas parciais e de escolher um modelo de consistência de forma deliberada. Na oficina, você executará dois processos FastAPI com dois PostgreSQL isolados por Docker Compose e observará o que ocorre quando uma dependência síncrona para.

## Percurso de aprendizagem

1. [Conceitos](conceitos.md) apresenta capacidade de negócio, *bounded context*, coesão e acoplamento.
2. [Padrões e decisões](padroes-e-decisoes.md) compara unidades de implantação e propriedade de dados e apresenta CAP, SAGA e CQRS com código executável.
3. Em [Exemplo arquitetural](exemplo-arquitetural.md), acompanhamos uma solicitação de exame pelos dois serviços.
4. Em [Estudo de caso](estudo-de-caso.md), avaliamos uma decomposição excessiva e uma consolidação responsável.
5. Em [Casos reais](casos-reais.md), acompanhamos a Netflix reconstruir tudo na nuvem e aprender a perder uma região inteira.
6. Na [Oficina de ferramentas](oficina-de-ferramentas.md), executamos, interrompemos e limpamos o ambiente.
7. Em [Exercícios](exercicios.md), avançamos pelos seis níveis da Taxonomia de Bloom.
8. Em [Síntese e referências](sintese-e-referencias.md), consolidamos heurísticas e fontes públicas.

```mermaid
flowchart LR
    A[Capacidades do negócio] --> B[Limites lógicos]
    B --> C[Propriedade dos dados]
    C --> D[Forma de implantação]
    D --> E[Comunicação e falhas]
    E --> F[Consistência e operação]
```

**Texto alternativo:** percurso que parte das capacidades de negócio e passa por limites e propriedade de dados até chegar à implantação, às falhas, à consistência e à operação.

*Figura 1 — Percurso de decisão para arquitetura de serviços. Fonte: curso.*

**Leitura textual da figura:** o percurso começa pelas capacidades e define limites e propriedade dos dados antes de escolher a forma de implantação. Somente depois dessa escolha o percurso trata de comunicação, falhas, consistência e operação.

## Prática guiada nas ODAs 05 e 06

As ODAs da disciplina são atividades individuais de 25 minutos que executam programas Python curtos sobre o mesmo caso hospitalar deste módulo. Os programas usam apenas a biblioteca padrão do Python e ficam nas pastas `codigo/oda-05` e `codigo/oda-06` do [repositório das ODAs](https://github.com/aulas-marco/odas-arquitetura-software). A tabela relaciona cada ODA às seções deste módulo que apresentam o mesmo código com a saída de uma execução real.

| ODA | Tema | Seções do módulo |
| --- | --- | --- |
| [ODA 05](https://aulas-marco.github.io/odas-arquitetura-software/oda-05/) | Falha parcial, prazo de espera, nova tentativa com chave de idempotência e disjuntor | [Chamadas síncronas e falhas parciais](conceitos.md#chamadas-sincronas-e-falhas-parciais) e [Orçamento de falha das chamadas síncronas](padroes-e-decisoes.md#chamadas-sincronas-orcamento-de-falha) |
| [ODA 06](https://aulas-marco.github.io/odas-arquitetura-software/oda-06/) | SAGA orquestrada com compensação e projeção CQRS com defasagem e reconstrução | [Orquestração do agendamento de exame em Python](padroes-e-decisoes.md#orquestracao-do-agendamento-de-exame-em-python) e [Comando e projeção no mesmo processo](padroes-e-decisoes.md#comando-e-projecao-no-mesmo-processo) |

A seção [Partição simulada com três réplicas](padroes-e-decisoes.md#particao-simulada-com-tres-replicas) usa um terceiro programa da pasta `codigo/oda-06/particao`, que mostra o comportamento de um armazenamento durante uma partição e não faz parte do laboratório da ODA 06.

## Premissas e limites do módulo {#o-que-nao-sera-presumido}

Microsserviços não são objetivo em si, porque um limite de domínio pode existir dentro de um único processo. A tecnologia de um serviço pode ser a mesma dos serviços vizinhos sem prejuízo à fronteira entre eles. Trocar uma chamada local por uma chamada REST mantém o acoplamento entre as duas partes e apenas muda a sua forma. Banco por serviço define a propriedade dos dados e não implica persistência poliglota. A consistência eventual atenua alguns riscos e não resolve sozinha uma transação distribuída. SAGA e CQRS entram no módulo como opções com custo, adotadas somente quando o contexto justifica esse custo.

O laboratório usa duas aplicações pequenas para tornar a fronteira visível e não pretende apresentar o desenho ideal de um hospital. Em produção, a segurança, a privacidade e a autorização exigiriam decisões adicionais. A observabilidade, a recuperação e a gestão de segredos também exigiriam decisões próprias. O laboratório usa dados sintéticos e credenciais válidas só na máquina local, de modo que a atividade não envolve dados de pacientes reais.

## Critério central de decisão

O critério central é preferir o menor grau de distribuição que preserve a autonomia necessária. Quando duas áreas mudam juntas e pertencem ao mesmo time, além de precisarem de uma única transação, uma fronteira interna forte costuma ser melhor que uma chamada de rede. Quando as áreas têm ritmos de entrega e escala distintos ou diferem em risco e propriedade, processos separados podem compensar o custo operacional da distribuição. A decisão resultante deve ser registrada como decisão arquitetural com o sinal que levaria à sua revisão.
