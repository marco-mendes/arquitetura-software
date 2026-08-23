# Casos reais: Shopify e o monólito modular

O [estudo de caso deste módulo](estudo-de-caso.md) trabalha a escolha de estilo numa plataforma hospitalar, onde você controla os requisitos. Esta página traz o mesmo tipo de decisão numa empresa existente, documentada por ela própria. Leia antes o [protocolo de leitura de caso público](../referencia/como-ler-um-caso-publico.md), que explica o que se transfere de um relato desses e o que não se transfere.

O caso é a Shopify, plataforma de comércio eletrônico, e a fonte é um artigo assinado por Kirsten Westeinde no blog de engenharia da empresa, publicado em 21 de fevereiro de 2019.

## A restrição

A Shopify descreve o próprio sistema como *"one of the largest Ruby on Rails codebases in existence"*, trabalhado por mais de mil desenvolvedores ao longo de mais de uma década.

O sintoma que o artigo escolhe para abrir é preciso e vale reter, porque é o mesmo que aparece em sistemas mil vezes menores: *"Making a seemingly innocuous change could trigger a cascade of unrelated test failures."* Uma mudança pequena provocava falhas em testes que nada tinham a ver com ela.

O segundo sintoma é de carga cognitiva. Para mexer em uma parte do sistema, uma pessoa recém-contratada precisava entender como pedidos são criados e como pagamentos são processados, porque tudo estava entrelaçado.

Nenhum desses dois sintomas é sobre desempenho ou escala de tráfego. São sintomas de **acoplamento**, que é a variável que o [mapa de estilos deste módulo](conceitos.md#um-mapa-antes-da-escolha) usa para separar as famílias.

## A decisão que a Shopify não tomou

O artigo registra que a equipe considerou microsserviços e recusou. A justificativa é explícita: a mudança resolveria os problemas existentes e traria outro conjunto inteiro de problemas, entre eles múltiplas esteiras de implantação, sobrecarga de infraestrutura, latência de rede e dificuldade de coordenar refatorações que atravessam serviços.

Essa recusa é o valor didático do caso. Uma empresa com mais de mil desenvolvedores no mesmo repositório é o cenário em que o argumento por microsserviços é mais forte, e ainda assim a decisão foi outra.

## A decisão que a Shopify tomou

A definição que o artigo dá é curta e serve como referência: *"A modular monolith is a system where all of the code powers a single application and there are strictly enforced boundaries between different domains."*

Duas metades importam igualmente. A primeira: o código inteiro continua sustentando uma aplicação única, com uma implantação e um banco. A segunda: existem fronteiras entre domínios e elas são impostas por verificação, sem depender de disciplina individual.

A execução foi reorganizar o código por domínio de negócio, com pedidos, envio e faturamento como unidades de primeira classe em vez de camadas técnicas. Para impor as fronteiras, a equipe construiu uma ferramenta interna chamada Wedge, que acompanha o progresso de isolamento de cada componente e detecta violação de fronteira usando *tracepoints* de Ruby durante a integração contínua.

A fronteira, aqui, é verificada por máquina. É a diferença entre uma convenção de equipe, que dura até a próxima entrega urgente, e uma restrição arquitetural.

## A evidência

O artigo é econômico em números, e isso é uma qualidade. O resultado concreto que ele apresenta é a substituição completa do sistema de cálculo de impostos, com a observação de que, antes do trabalho de modularização, aquilo teria sido uma tarefa quase impossível.

É uma evidência de segunda ordem, e ela mede exatamente o que o estilo pretendia melhorar: a capacidade de trocar uma parte sem tocar no resto. Compare com um resultado de latência ou de custo, que mediria outra coisa.

## O que o caso não prova

A Shopify tem um único produto com um modelo de domínio coerente, e o comércio eletrônico permite manter quase tudo numa transação de banco. Um hospital tem domínios com ciclos regulatórios distintos e integrações externas obrigatórias, que às vezes forçam um processo separado por exigência contratual de terceiro, mesmo quando a técnica permitiria mantê-lo junto.

A ferramenta Wedge também depende de uma característica do Ruby que nem toda plataforma oferece. Em Java o papel equivalente cabe a testes de arquitetura ou a módulos verificados na compilação; em .NET, a projetos separados com visibilidade controlada. O mecanismo muda; a exigência de que a fronteira seja verificada automaticamente permanece.

Por fim, mil desenvolvedores num repositório é uma escala que impõe investimento em ferramental próprio. Uma equipe de dez pessoas obtém o mesmo efeito com convenções de pacote e uma regra de dependência na esteira de integração.

## Leitura guiada

**1. Sintoma e causa.** A falha em cascata de testes não relacionados indica qual propriedade estrutural? Explique por que aumentar a cobertura de testes não resolveria esse sintoma.

**2. A recusa.** Reconstrua o argumento pelo qual a Shopify recusou microsserviços e identifique qual dos quatro custos citados seria mais grave numa equipe pequena.

**3. Fronteira imposta.** Diferencie fronteira acordada de fronteira verificada, e proponha o mecanismo de verificação que você usaria na plataforma hospitalar, dada a linguagem do laboratório deste módulo.

**4. Escolha da métrica.** A Shopify mediu o resultado pela capacidade de substituir um subsistema inteiro. Justifique por que essa métrica se ajusta à decisão tomada, e diga qual métrica seria adequada se a decisão tivesse sido distribuir.

**5. Transferência.** Aplique a definição de monólito modular ao [Exercício 2 do estudo de caso](estudo-de-caso.md#exercicio-2-matriz-de-estilos-por-capacidade) e indique quais capacidades hospitalares ficariam no mesmo processo sob esse critério.

## Fontes

- Kirsten Westeinde, [Deconstructing the Monolith: Designing Software that Maximizes Developer Productivity](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity) — Shopify Engineering, 21 de fevereiro de 2019. Fonte primária de todas as citações e da definição de monólito modular.
- Simon Brown, [Modular Monoliths](https://www.infoq.com/presentations/modular-monoliths/) — apresentação que estabelece o vocabulário usado no caso.
- ArchUnit, [documentação oficial](https://www.archunit.org/userguide/html/000_Index.html) — verificação automatizada de regras de dependência, equivalente funcional do Wedge no ecossistema Java.
