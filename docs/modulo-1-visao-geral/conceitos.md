# Conceitos: estilos arquiteturais

Para o vocabulário de leitura de diagramas, decisões, restrições e cenários, consulte [Como ler uma arquitetura](../referencia/como-ler-uma-arquitetura.md). Esta unidade começa pela comparação de estilos.

## Estilos arquiteturais

Um **estilo arquitetural** nomeia organizações com elementos, conectores e restrições comuns. Oferece vocabulário, não receita: duas soluções em camadas podem ter tecnologias distintas e ainda restringir dependências por responsabilidade.

## Um mapa antes da escolha

Antes de comparar implementações, localize o problema. O mapa não é sequência de evolução nem lista de tecnologias; evita usar microsserviços para uma regra local ou Kubernetes para uma fronteira ainda desconhecida.

![Diagrama em quatro cartões: organização interna pergunta como responsabilidades colaboram; decomposição por domínio reúne DDD, microsserviços e macrosserviços; integração e comunicação pergunta qual contrato atravessa a fronteira; execução e operação reúne nuvem, contêineres, orquestração e serverless.](../assets/images/m01-familias-arquiteturais.svg)

*Figura 1 — Quatro famílias de decisões para arquiteturas de backend. Fonte: curso.*

**Leitura textual da figura:** os cartões não têm uma ordem de maturidade. Organização interna reúne Camadas, MVC, Hexagonal, Microkernel e Monólito modular. Decomposição por domínio reúne DDD, microsserviços e macrosserviços. Integração e comunicação reúne Pipes and Filters, APIs e eventos. Execução e operação reúne nuvem, contêineres, orquestração e serverless. A escolha em uma família não impõe uma escolha nas demais.

| Família | Pergunta que vem antes da tecnologia | Termos do mapa | Quando aprofundaremos |
| --- | --- | --- | --- |
| Organização interna | Como responsabilidades colaboram dentro de uma aplicação? | Camadas, MVC, Hexagonal, Microkernel, Monólito modular | Nesta unidade |
| Decomposição por domínio | Onde termina um modelo de negócio e começa outro? | DDD, microsserviços, macrosserviços | [Unidade 3](../modulo-3-servicos/index.md) |
| Integração e comunicação | Qual contrato transporta uma intenção ou um fato entre fronteiras? | Pipes and Filters, APIs, eventos | [Unidades 2](../modulo-2-apis/index.md) e [5](../modulo-5-eventos/index.md) |
| Execução e operação | Onde a solução roda e como é recuperada ou escalada? | nuvem, contêineres, orquestração, serverless | [Unidade 6](../modulo-6-nuvem/index.md) |

### Organização interna

**Problema:** manter uma aplicação compreensível quando suas regras, entradas e recursos técnicos começam a se misturar.

**Ideia de organização:** declarar fronteiras internas e dependências permitidas. **Estilos abrangidos:** [Camadas](padroes-e-decisoes.md#camadas), MVC, Hexagonal, [Microkernel](padroes-e-decisoes.md#microkernel) e [Monólito modular](padroes-e-decisoes.md#monolito-modular-uma-implantacao-capacidades-com-autonomia-interna). 

**Quando ajuda:** uma equipe precisa mudar uma regra ou uma interface sem atravessar detalhes de infraestrutura. 

**Limite:** só separar pastas não cria fronteiras; atalhos e dependências não declaradas devolvem o acoplamento.

### Decomposição por domínio

**Problema:** descobrir quais regras pertencem à mesma capacidade de negócio antes de distribuir processos ou times. 

**Ideia de organização:** usar linguagem do domínio e contextos explícitos para decidir onde o modelo é válido. 

**Estilos abrangidos:** DDD (*Domain-Driven Design*), microsserviços e macrosserviços, tema retomado na [Unidade 3](../modulo-3-servicos/index.md). 

**Quando ajuda:** o negócio é complexo, há responsabilidades distintas e a conversa entre especialistas e desenvolvimento precisa ficar precisa. 

**Limite:** DDD não exige microsserviços; separar cedo multiplica contratos, dados e custos de operação, enquanto macrosserviços podem preservar coesão e reduzir coordenação quando a fragmentação já é excessiva.

### Integração e comunicação

**Problema:** transportar comandos, consultas, dados transformados ou fatos sem expor detalhes internos da outra parte. 

**Ideia de organização:** escolher um contrato e uma forma de acoplamento temporal adequados ao cenário. 

**Estilos abrangidos:** [Pipes and Filters](padroes-e-decisoes.md#pipes-and-filters), APIs e eventos; APIs aparecem na [Unidade 2](../modulo-2-apis/index.md) e eventos na [Unidade 5](../modulo-5-eventos/index.md). 

**Quando ajuda:** etapas de processamento, sistemas parceiros ou reações assíncronas precisam de limites claros. 

**Limite:** uma interface não resolve por si só versionamento, falhas parciais, correlação ou consistência.

### Execução e operação

**Problema:** disponibilizar a solução com capacidade, recuperação e entrega compatíveis com suas necessidades. 

**Ideia de organização:** tratar o ambiente de execução como decisão arquitetural, e não como detalhe posterior. 

**Estilos abrangidos:** nuvem, contêineres, orquestração e serverless, aprofundados na [Unidade 6](../modulo-6-nuvem/index.md). 

**Quando ajuda:** a carga varia, a implantação precisa ser repetível, a capacidade deve ser reconciliada ou a recuperação de falhas precisa ser observável. 

**Limite:** infraestrutura sofisticada não compensa fronteiras mal definidas e pode criar operação desproporcional ao problema.

O mapa não é escada de maturidade: um monólito modular pode usar APIs, faturamento pode usar Pipes and Filters e nuvem pode ter um processo. Decida por forças e evidências, não pelo nome.

![Mapa comparativo de quatro estilos arquiteturais: camadas, pipes e filtros, microkernel e monólito modular, com as forças de mudabilidade, vazão e extensibilidade.](../assets/images/m01-mapa-estilos.png)

*Figura 2 — Mapa comparativo de estilos arquiteturais. Fonte: curso.*

**Leitura textual da figura:** o mapa coloca quatro organizações lado a lado. Camadas separam responsabilidades por nível; pipes e filtros encadeiam transformações; microkernel mantém um núcleo e extensões; e monólito modular isola capacidades dentro de uma implantação. As forças na base lembram que a escolha compara modificabilidade, vazão e extensibilidade, em vez de eleger um estilo universalmente superior.

## Comparar, não eleger um vencedor universal

Camadas organizam níveis; Pipes and Filters, transformações; Microkernel, extensões; Monólito modular, capacidades numa implantação. Eles podem ser combinados. Compare forças, limites, premissas e evidências antes de escolher.
