## Padrões, tecnologias e decisões

Esta página descreve quatro estilos de organização interna de um backend (camadas, pipes and filters, microkernel e monólito modular) e apresenta, para cada um, a estrutura, as forças, o anti-padrão característico, as características arquiteturais e os critérios de uso.

## Comparação dos quatro estilos {#comparacao-dos-quatro-estilos}

| Estilo            | Responsabilidade e Conectores                                                    | Forças                                        | Anti-padrão                             | Quando usar                                    | Evite quando                                       |
| ----------------- | -------------------------------------------------------------------------------- | --------------------------------------------- | --------------------------------------- | ---------------------------------------------- | -------------------------------------------------- |
| Camadas           | Separar interface, casos de uso, regras e infraestrutura por chamadas permitidas | testabilidade e mudança localizada            | sumidouro ou atalho oculto              | regras precisam ser isoladas da infraestrutura | a passagem obrigatória não agrega trabalho         |
| Pipes and Filters | Transformar dados por pipes com contratos de entrada, saída e rejeição           | composição e throughput                       | estado compartilhado invisível          | etapas de transformação são explícitas         | o fluxo é interativo e exige consistência imediata |
| Microkernel       | Manter invariantes no núcleo e variações por contrato de plugin                  | extensibilidade e modificabilidade            | core creep                              | variações podem entrar e sair isoladamente     | plugins precisam controlar detalhes do núcleo      |
| Monólito modular  | Organizar capacidades por interfaces internas numa implantação                   | simplicidade operacional e consistência local | módulos que leem dados internos alheios | equipe e operação ainda são uma unidade        | escala ou implantação independente já foi medida   |

Richards e Ford avaliam cada estilo em nove características, numa escala de 1 (fraco) a 5 (forte). A figura 3 reúne as avaliações dos quatro estilos num único quadro, e as observações que justificam cada nota estão recolhidas na seção do respectivo estilo.

![Mapa de calor com nove características nas linhas e quatro estilos nas colunas, em escala de 1 a 5. Pipes and Filters tem nota 5 em testabilidade e modularidade, Microkernel tem nota 3 em oito das nove características, e Camadas e Monólito modular têm nota alta em custo e simplicidade e nota 1 em elasticidade.](../assets/images/m01-caracteristicas-estilos.svg)

*Figura 3 — Características arquiteturais dos quatro estilos, de 1 a 5. Fonte: curso.*

**Leitura textual da figura:** Camadas recebe 5 em custo e simplicidade, 3 em testabilidade, desempenho e confiabilidade, 2 em escalabilidade, implantabilidade e modularidade e 1 em elasticidade. Pipes and Filters recebe 5 em custo, simplicidade, testabilidade e modularidade, 3 em implantabilidade e confiabilidade e 2 em escalabilidade, elasticidade e desempenho. Microkernel recebe 4 em modularidade e 3 nas demais. Monólito modular, avaliado pelo curso na mesma escala, recebe 5 em custo, 4 em simplicidade, testabilidade, desempenho e modularidade, 3 em implantabilidade e confiabilidade, 2 em escalabilidade e 1 em elasticidade.

## Camadas {#camadas}

> Pense nos andares de um prédio, em que cada andar se comunica apenas com o andar vizinho.

O estilo em camadas define uma regra de dependência entre quatro responsabilidades. A apresentação traduz a interação e o formato das mensagens, a aplicação coordena os casos de uso, o domínio preserva as regras de negócio e as **invariantes** (condições que precisam valer sempre, como um saldo que nunca pode ficar negativo), e a infraestrutura oferece banco de dados, mensageria e outros adaptadores. Como cada chamada atravessa uma fronteira conhecida, a regra de negócio pode ser exercitada em teste sem iniciar um servidor HTTP ou um banco de dados.

O estilo em camadas (*layered architecture*) é o mais difundido na engenharia de software porque costuma surgir da própria divisão das equipes. Mark Richards e Neal Ford chamam esse fenômeno de *architecture by implication* em *Fundamentals of Software Architecture*, situação em que o estilo é adotado por inércia e sem decisão registrada. A **Lei de Conway** explica o mecanismo: organizações produzem arquiteturas que reproduzem sua estrutura de comunicação, e uma equipe dividida em frontend, backend e banco de dados tende a produzir um sistema em três camadas (apresentação, negócios e dados) mesmo sem planejamento do arquiteto. A versão apresentada nesta página divide a camada de negócios em aplicação, que coordena os casos de uso, e domínio, que guarda as regras e as invariantes.

![Quatro camadas empilhadas. Apresentação chama Aplicação, Aplicação usa Domínio e Infraestrutura, e a Infraestrutura acessa o banco. Uma seta tracejada azul da Apresentação à Infraestrutura marca a camada aberta deliberada, e uma seta vermelha com um X da Apresentação ao banco marca o atalho proibido.](../assets/images/m01-camadas-dependencias.svg)

*Figura 4 — Dependência permitida, atalho deliberado e atalho proibido em camadas. Fonte: curso.*

**Leitura textual da figura:** a Apresentação chama a Aplicação, que usa as regras do Domínio e os mecanismos da Infraestrutura, e somente a Infraestrutura acessa o banco. A seta tracejada azul liga a Apresentação à Infraestrutura e representa uma camada aberta, isto é, um atalho de leitura registrado em ADR. A seta vermelha liga a Apresentação ao banco e representa o atalho proibido, que contorna a regra de negócio.

Uma **camada fechada** obriga a requisição a passar pela camada adjacente. Esse arranjo protege a regra de negócio e impede que uma mudança numa camada se propague para as outras, ao custo de toda requisição percorrer todas as camadas, inclusive as consultas simples. Uma camada aberta permite um atalho deliberado, com contrato e teste, para reduzir o custo de uma leitura específica, e esse atalho cria acoplamento entre camadas não adjacentes que reduz o isolamento a cada novo uso. A decisão de abrir ou fechar cada camada deve ser registrada num ADR.

O anti-padrão do **sumidouro** ocorre quando a requisição atravessa camadas que apenas repassam a chamada, sem validar nem transformar o dado. Uma consulta simples que atravessa as camadas é legítima, e o problema aparece quando esse tipo de travessia predomina no sistema. A figura 5 compara uma requisição de sumidouro com uma requisição em que cada camada executa uma decisão.

![Dois painéis. À esquerda, a requisição GET /usuarios atravessa Apresentação, Negócios e Dados, desenhadas em cinza, e cada camada apenas repassa a chamada. À direita, a requisição POST /consultas atravessa as mesmas camadas: a apresentação valida o formato, a camada de negócios recusa horário sobreposto com 409 Conflito e a camada de dados grava a consulta. Uma faixa inferior apresenta a regra dos 80%.](../assets/images/m01-sumidouro.svg)

*Figura 5 — Sumidouro comparado a uma camada que decide. Fonte: curso.*

**Leitura textual da figura:** no painel do sumidouro, a requisição GET /usuarios passa por apresentação, negócios e dados até o banco sem que nenhuma camada tome decisão. No painel da camada que decide, a apresentação valida o formato de POST /consultas, a camada de negócios recusa o horário sobreposto com 409 Conflito e a camada de dados grava a consulta. A faixa inferior registra a regra prática de Richards e Ford: se mais de 80% das requisições se comportam como o painel da esquerda, o estilo em camadas provavelmente não serve ao sistema.

As forças do estilo são a testabilidade, a mudança localizada e a rastreabilidade das dependências, e os limites são a latência acrescentada por camada, as abstrações sem função e o risco de sumidouro. Recomenda-se o estilo quando as invariantes precisam permanecer válidas após a troca da interface ou da infraestrutura, e a abertura de uma camada para leitura só se justifica com medição de custo e sem contornar regra de negócio.

### Características arquiteturais de Camadas

As notas de Camadas ocupam a primeira coluna da [figura 3](#comparacao-dos-quatro-estilos) e seguem Richards e Ford (*Fundamentals of Software Architecture*, cap. 10).

<details markdown="1">
<summary>Observações por característica</summary>

| Característica   | Avaliação (1 a 5) | Observação                                                                             |
| ---------------- | ----------------- | -------------------------------------------------------------------------------------- |
| Custo geral      | 5                 | baixo custo de entrada, tecnologia amplamente conhecida                                |
| Simplicidade     | 5                 | fácil de compreender e implementar                                                     |
| Escalabilidade   | 2                 | escala como unidade única, difícil escalar camadas individualmente                     |
| Elasticidade     | 1                 | pouca capacidade de expansão e retração rápidas sob carga variável                     |
| Implantabilidade | 2                 | uma unidade de implantação, qualquer mudança implanta o pacote inteiro                 |
| Testabilidade    | 3                 | camadas podem ser testadas em isolamento com dublês de teste                           |
| Desempenho       | 3                 | adequado na maioria dos casos, sobrecarga quando a requisição atravessa muitas camadas |
| Modularidade     | 2                 | modular logicamente, mas fisicamente acoplado                                          |
| Confiabilidade   | 3                 | falha em um componente pode afetar o sistema inteiro                                   |

</details>

### Princípio aberto-fechado na fronteira com os dados

O **OCP** (*Open-Closed Principle*), aplicado à fronteira entre camadas, consiste em acessar o banco de dados por meio de uma interface da qual a camada de negócios depende, com a implementação concreta mantida na infraestrutura. Com esse arranjo, a troca de MySQL por PostgreSQL altera apenas o repositório e mantém o serviço de negócio sem modificação.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime

@dataclass(frozen=True)
class Horario:
    inicio: datetime
    fim: datetime

    def conflita_com(self, outro: "Horario") -> bool:
        return self.inicio < outro.fim and self.fim > outro.inicio

class RepositorioConsulta(ABC):
    @abstractmethod
    def salvar(self, medico_id: int, horario: Horario) -> None: ...

    @abstractmethod
    def listar_do_dia(self, medico_id: int, dia: date) -> list[Horario]: ...

class EmMemoriaRepositorioConsulta(RepositorioConsulta):
    """Em produção, um PostgresRepositorioConsulta ocupa este lugar."""

    def __init__(self):
        self._consultas: dict[int, list[Horario]] = {}

    def salvar(self, medico_id: int, horario: Horario) -> None:
        self._consultas.setdefault(medico_id, []).append(horario)

    def listar_do_dia(self, medico_id: int, dia: date) -> list[Horario]:
        return [
            h for h in self._consultas.get(medico_id, [])
            if h.inicio.date() == dia
        ]

class ConflitoDeAgendaError(Exception):
    pass

class AgendamentoServico:
    """Camada de negócios: decide antes de persistir e depende da abstração."""

    def __init__(self, repositorio: RepositorioConsulta):
        self._repositorio = repositorio

    def agendar(self, medico_id: int, horario: Horario) -> None:
        ocupados = self._repositorio.listar_do_dia(medico_id, horario.inicio.date())
        if any(horario.conflita_com(h) for h in ocupados):
            raise ConflitoDeAgendaError(
                f"Médico {medico_id} já tem consulta sobreposta nesse intervalo"
            )
        self._repositorio.salvar(medico_id, horario)
```

O método `agendar` consulta a agenda do dia e recusa a sobreposição antes de chamar `salvar`, e essa decisão justifica a existência da camada de negócios. Se `agendar` apenas repassasse os argumentos ao repositório, a camada seria um caso de sumidouro, como o da figura 5, e acrescentaria uma chamada sem nenhuma decisão. A regra de conflito pode ser testada com um repositório dublê, sem banco de dados.

O exemplo executável completo, com a mesma invariante e um controller HTTP que devolve `409` em caso de conflito, está em `codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas` e é explorado na [oficina de ferramentas](oficina-de-ferramentas.md).

### MVC e DDD como variações do estilo em camadas

O **MVC** (*Model-View-Controller*) especializa o estilo em camadas para o ciclo de requisição e resposta HTTP. O controller orquestra a requisição, o model concentra as regras de negócio e a view serializa a resposta, que em APIs costuma ser JSON. A figura 6 apresenta o ciclo do MVC ao lado da estrutura do DDD, descrita mais abaixo, para mostrar o critério de separação de cada abordagem.

![Dois painéis. No painel do MVC, o cliente HTTP envia POST /pedidos ao Controller, que aciona o Model, recebe os dados, aciona a View e devolve 200 OK. No painel do DDD, a fronteira do agregado contém a raiz Pedido, a entidade ItemPedido e o objeto de valor Dinheiro, e o PedidoRepositorio, fora da fronteira, salva e busca a raiz e grava o agregado na persistência.](../assets/images/m01-mvc-ddd.svg)

*Figura 6 — Critério de separação no MVC e no DDD. Fonte: curso.*

**Leitura textual da figura:** no MVC, o cliente envia POST /pedidos ao controller, que aciona o model, recebe os dados processados, aciona a view e devolve 200 OK, na ordem numerada do desenho. No DDD, a fronteira tracejada do agregado contém a raiz Pedido, a entidade ItemPedido e o objeto de valor Dinheiro, e o PedidoRepositorio, fora da fronteira, salva e busca apenas a raiz e grava o agregado na persistência.

Os frameworks a seguir consolidaram o MVC no mercado:

| Camada           | Tecnologias                                             |
| ---------------- | ------------------------------------------------------- |
| Controller       | ASP.NET MVC, Spring MVC, Ruby on Rails, Laravel, Django |
| Model e negócios | .NET Core, Spring Boot, Node.js (Express), FastAPI      |
| Dados            | Entity Framework, Hibernate, ActiveRecord, SQLAlchemy   |

O **DDD** (*Domain-Driven Design*) organiza a camada de negócios pelos conceitos do domínio, como Pedido, Pagamento e Cliente, e protege as regras de cada conceito dentro de um agregado, que é um grupo de objetos tratado como unidade, com uma raiz que controla o acesso ao conjunto. No exemplo de vendas da figura 6, o agregado `Pedido` contém entidades `ItemPedido`, usa o objeto de valor `Dinheiro` para preservar as invariantes monetárias e é salvo e recuperado pelo repositório `PedidoRepositorio`. O DDD é preferível a camadas simples quando as regras de negócio são complexas e mudam com frequência e quando o risco principal é o desentendimento entre o time técnico e os especialistas de negócio, tema retomado na [Unidade 3](../modulo-3-servicos/index.md).

### Camadas lógicas e camadas físicas

A arquitetura em camadas define uma estrutura lógica, e a distribuição dessas camadas em unidades físicas de implantação (*tiers*) é uma decisão separada, ilustrada na figura 7.

![Três linhas alinhadas com as colunas Apresentação, Negócios, Dados e Banco. Na primeira linha, tudo roda num único processo com banco embutido. Na segunda, um servidor de aplicação reúne as três camadas e se comunica por TCP com o banco em outro servidor. Na terceira, cada camada é um serviço separado, e os serviços se comunicam por HTTP e gRPC. Selos âmbar marcam cada travessia de rede.](../assets/images/m01-camadas-fisicas.svg)

*Figura 7 — As mesmas camadas lógicas em uma, duas e três camadas físicas. Fonte: curso.*

**Leitura textual da figura:** as colunas mantêm as mesmas camadas lógicas nas três linhas, e somente os contornos de processo mudam. Com uma camada física não há travessia de rede entre camadas, com duas há uma travessia por TCP até o banco, e com três há travessias por HTTP entre apresentação e negócios e por gRPC entre negócios e dados.

A tabela compara os três arranjos, que aumentam a independência entre as camadas à medida que acrescentam travessias de rede:

| Camadas físicas | Exemplo                                                | Vantagens                                                                 | Desvantagens                                                            |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Uma (monolito)  | processo único com banco embutido                      | simplicidade, menor custo, fácil de depurar e empacotar                   | difícil escalar componentes individualmente, risco alto em implantações |
| Duas            | servidor de aplicação e banco de dados separados       | backend e banco evoluem e escalam de forma independente                   | latência de rede entre camadas, gestão de dois serviços                 |
| Três ou mais    | apresentação, negócios e dados como serviços distintos | escalabilidade fina por camada, isolamento de falhas, times independentes | complexidade operacional, latência acumulada, exige observabilidade     |

A distribuição física não corrige um acoplamento lógico mal definido, porque um sistema com responsabilidades misturadas entre camadas continua acoplado quando as camadas rodam em servidores separados.

### Quando usar camadas

Recomenda-se o estilo em camadas quando:

- O sistema tem escopo e regras de negócio bem definidos.
- A equipe é pequena e o orçamento é limitado.
- A velocidade de desenvolvimento inicial importa mais que a escalabilidade.
- O sistema é predominantemente **CRUD** (as quatro operações básicas sobre dados: criar, ler, atualizar e remover), com lógica de negócio moderada.

O estilo em camadas não é indicado quando:

- Escalabilidade alta ou elasticidade são requisitos obrigatórios.
- Mais de 80% das requisições são sumidouros, situação em que o estilo acrescenta latência sem decisão correspondente.
- Times independentes precisam implantar partes do sistema de forma autônoma.
- O problema central é o processamento de dados em etapas, caso descrito em [Pipes and Filters](#pipes-and-filters).
- A extensibilidade do produto para mercados diferentes é o requisito principal, caso descrito em [Microkernel](#microkernel).

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly, 2022, cap. 10), Fowler (*Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002) e Evans (*Domain-Driven Design*, Addison-Wesley, 2003).

## Pipes and Filters {#pipes-and-filters}

> Pense numa esteira de fábrica, em que cada etapa executa uma única operação e entrega o resultado à etapa seguinte.

O estilo Pipes and Filters decompõe uma transformação em filtros ligados por pipes. Cada filtro recebe um valor definido por contrato e devolve um novo valor ou uma **rejeição** explícita, e o pipe transporta o resultado sem expor detalhes internos do filtro. O contrato nomeia o formato, a correlação, os campos preservados e o motivo e o destino da rejeição, o que permite testar e observar cada etapa isoladamente.

Richards e Ford chamam o estilo de *Pipeline Architecture* (*Fundamentals of Software Architecture*, cap. 11) e apontam como premissa a ausência de estado compartilhado: cada filtro recebe dados, transforma-os e os emite sem conhecer a origem nem o destino. Como os filtros se comunicam apenas pelos pipes, é possível acrescentar, remover ou reordenar filtros sem alterar os demais. Os autores identificam quatro tipos de filtro, e a figura 8 mostra os quatro num pipeline de pedidos de comércio eletrônico em que o leitor constrói o pedido, o validador desvia os inválidos, o aplicador de desconto e o calculador de frete transformam o pedido sem descartá-lo e o finalizador aprova e reporta o resultado.

![Cinco filtros em linha ligados por pipes: LeitorDePedido (producer), ValidadorDePedido (tester), AplicadorDeDesconto e CalculadorDeFrete (transformers) e FinalizadorDePedido (consumer). Abaixo de cada pipe aparece o dado que passa por ele, e do validador sai uma seta vermelha para a rejeição explícita com lote, etapa e causa.](../assets/images/m01-pipeline-pedidos.svg)

*Figura 8 — Pipeline de pedidos com os quatro tipos de filtro. Fonte: curso.*

**Leitura textual da figura:** o LeitorDePedido cria o pedido e o envia ao ValidadorDePedido. Os pedidos inválidos seguem para a rejeição explícita, que guarda lote, etapa e causa para reprocessamento, e os válidos recebem desconto no AplicadorDeDesconto e frete no CalculadorDeFrete antes de chegar ao FinalizadorDePedido, que aprova e reporta. O quadro inferior registra que nenhum filtro conhece o filtro vizinho nem guarda estado.

| Tipo | Papel | Exemplos |
| --- | --- | --- |
| **Producer** | entrada do fluxo, gera ou lê os dados iniciais | leitura de arquivo, chamada a API, leitura de fila |
| **Transformer** | recebe dados, aplica transformação e os emite sem descartar | normalizar campos, enriquecer com dados externos, calcular métricas |
| **Tester** | avalia os dados contra um critério, descarta os que não passam | validar schema, filtrar por nível, separar por categoria |
| **Consumer** | término do fluxo, persiste ou envia os dados processados | gravar no banco, enviar e-mail, publicar em fila |

Um **filtro sem estado** depende apenas da entrada e pode ser repetido ou paralelizado sem cuidado adicional. Um filtro com estado depende de memória, banco ou janela temporal e precisa declarar armazenamento, recuperação, concorrência e chave de correlação. A ordenação também faz parte do contrato, de modo que somente etapas independentes podem ser paralelizadas e a sequência exigida pela chave de negócio precisa ser preservada.

O anti-padrão correspondente é o **estado compartilhado invisível**, em que um filtro acumula estado interno sem declará-lo. Esse estado cria acoplamento implícito e torna o pipeline não determinístico, porque o resultado passa a depender da ordem de execução. Quando o fluxo exige acumulação, como em janelas de tempo de streaming, o estado deve ficar num mecanismo externo declarado, como Redis ou um *state store* dedicado.

```python
# Errado: estado de classe compartilhado entre invocações
class FiltroComEstado:
    total = 0

    def processar(self, valor: float) -> float:
        self.total += valor
        return self.total  # o resultado depende da ordem de execução

# Correto: filtro sem estado, em que cada invocação é independente
class FiltroTransformador:
    def processar(self, dado: dict) -> dict:
        return {**dado, "valor_normalizado": dado["valor"] / 100}
```

As forças do estilo são composição, reuso, facilidade de diagnóstico e controle de **throughput** (vazão de itens processados por unidade de tempo) em cada filtro. Os limites são o custo dos contratos intermediários, a latência acumulada, o tratamento de estado e a recuperação parcial. O estilo é indicado quando a sequência de dados e as entradas e saídas de cada etapa são claras, e não é indicado para interações ricas que exigem consistência imediata.

No **Faturamento** hospitalar, as etapas de validar, normalizar códigos, enriquecer com dados do convênio e publicar formam um pipeline verificável. A rejeição preserva lote, etapa e causa, e a decisão pelo estilo exige medir o throughput em ambiente representativo e declarar a ordenação dos documentos de um mesmo atendimento.

### Características arquiteturais de Pipes and Filters

As notas de Pipes and Filters ocupam a segunda coluna da [figura 3](#comparacao-dos-quatro-estilos) e seguem Richards e Ford (*Fundamentals of Software Architecture*, cap. 11).

<details markdown="1">
<summary>Observações por característica</summary>

| Característica | Avaliação (1 a 5) | Observação |
| --- | --- | --- |
| Custo geral | 5 | baixo custo de entrada, conceito simples e direto |
| Simplicidade | 5 | estrutura linear fácil de entender e de explicar |
| Escalabilidade | 2 | filtros individuais podem escalar, o pipeline como unidade é limitado |
| Elasticidade | 2 | difícil expansão e retração rápidas sob carga variável |
| Implantabilidade | 3 | filtros podem ser implantados separadamente em versões modernas |
| Testabilidade | 5 | destaque do estilo: cada filtro é independente e testável em isolamento |
| Desempenho | 2 | o processamento sequencial introduz latência acumulada |
| Modularidade | 5 | destaque do estilo: máxima modularidade por design |
| Confiabilidade | 3 | falha num filtro interrompe o pipeline, exige estratégias de reprocessamento |

</details>

### Framework mínimo de pipeline

O padrão pode ser implementado com duas classes: um contrato de filtro e um encadeador que executa a sequência de filtros.

```python
from abc import ABC, abstractmethod
from typing import Any

class Filtro(ABC):
    """Contrato base: cada filtro recebe e devolve dados."""

    @abstractmethod
    def processar(self, dados: Any) -> Any: ...

class Pipeline:
    """Encadeia filtros e executa a transformação em sequência."""

    def __init__(self):
        self._filtros: list[Filtro] = []

    def adicionar(self, filtro: Filtro) -> "Pipeline":
        self._filtros.append(filtro)
        return self

    def executar(self, dados: Any) -> Any:
        resultado = dados
        for filtro in self._filtros:
            resultado = filtro.processar(resultado)
        return resultado
```

Com esse framework, o pipeline da figura 8 é montado por chamadas sucessivas a `adicionar` com `LeitorDePedido`, `ValidadorDePedido`, `AplicadorDeDesconto`, `CalculadorDeFrete` e `FinalizadorDePedido`, nessa ordem.

O acervo do curso traz um segundo exemplo, que processa linhas de log e mantém apenas os níveis ERROR e CRITICAL. Os dois exemplos executáveis estão em `codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters` e são explorados na [oficina de ferramentas](oficina-de-ferramentas.md).

### Quando usar Pipes and Filters

Recomenda-se Pipes and Filters quando:

- O problema é um fluxo de transformações de dados, como **ETL** (extração, transformação e carga de dados de uma origem para um destino), validação em várias etapas ou processamento de logs.
- A testabilidade isolada de cada etapa é requisito.
- Equipes diferentes desenvolvem etapas de forma independente.
- O pipeline precisa ser composto e recomposto em tempo de execução.

Pipes and Filters não é indicado quando:

- O sistema tem lógica de negócio hierárquica, caso descrito em [Camadas](#camadas) e no DDD.
- As etapas precisam compartilhar estado, o que elimina a independência dos filtros.
- A latência acumulada das etapas é inaceitável para o caso de uso.
- O fluxo não é linear e requer orquestração, tema das arquiteturas de eventos na [Unidade 5](../modulo-5-eventos/index.md).

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly, 2022, cap. 11), Hohpe e Woolf (*Enterprise Integration Patterns*, Addison-Wesley, 2003) e Shaw e Garlan (*Software Architecture: Perspectives on an Emerging Discipline*, Prentice Hall, 1996).

## Microkernel {#microkernel}

> Pense num videogame de cartuchos, em que o console permanece o mesmo e cada cartucho acrescenta um jogo sem alterar o console.

O estilo Microkernel separa um núcleo estável das extensões. O núcleo preserva identidade, autorização, ciclo de vida e orquestração, e o **registro** descobre as extensões disponíveis e seleciona a apropriada para cada caso. Um plugin conhece apenas as capacidades públicas do núcleo e não acessa tabelas nem objetos internos dele.

Richards e Ford chamam o estilo de *Plug-in Architecture* (*Fundamentals of Software Architecture*, cap. 12). A premissa do estilo é que o núcleo evolui lentamente e os plugins evoluem com rapidez e de forma independente, sem coordenação entre equipes. A única relação entre o núcleo e os plugins é o contrato que o núcleo define e que cada plugin implementa, e os plugins não dependem uns dos outros. A figura 9 mostra essa estrutura no cálculo de impostos por estado, caso de referência do estilo detalhado mais adiante.

![À esquerda, o núcleo SistemaFiscal com o registro que mapeia SP e RJ a plugins, o executor e os serviços compartilhados. No centro, a barra do contrato CalculadorImposto. À direita, os plugins ImpostoSPPlugin e ImpostoRJPlugin e um novo estado tracejado, encaixados no contrato. Uma faixa vermelha inferior mostra o core creep como um if por estado dentro do núcleo.](../assets/images/m01-microkernel-impostos.svg)

*Figura 9 — Núcleo, contrato e plugins no cálculo de impostos por estado. Fonte: curso.*

**Leitura textual da figura:** o núcleo SistemaFiscal reúne o registro, que mapeia SP e RJ aos seus plugins e seleciona pelo estado do pedido, o executor, que chama o plugin escolhido, e os serviços compartilhados de log, segurança e configuração. O executor chega aos plugins somente pelo contrato CalculadorImposto. O plugin de São Paulo aplica 12% a eletrônicos e 18% aos demais produtos, o do Rio de Janeiro aplica 20% em qualquer produto, e um novo estado se registra sem alterar o núcleo. A faixa inferior mostra o core creep, que é um if por estado escrito dentro do núcleo.

O **contrato de extensão** define entrada, resultado, erros, permissões e versão. A compatibilidade é verificada pela versão e pelas capacidades declaradas, e o núcleo confere o contrato e os dados autorizados antes de carregar um plugin.

O núcleo contém apenas a funcionalidade mínima para o sistema operar: gerencia o ciclo de vida dos plugins, define e impõe o contrato, orquestra a execução e provê serviços compartilhados. Quando o núcleo acumula lógica de negócio que pertence aos plugins, o sistema perde as fronteiras de extensão e volta a funcionar como um monolito comum.

O registro de plugins admite quatro implementações, que diferem no momento em que um plugin pode ser incluído ou removido:

- **Arquivo de configuração** (YAML ou JSON), simples de manter, que exige reinicialização para alterar plugins.
- **Descoberta por convenção**, em que o núcleo percorre pacotes em busca de classes que implementam a interface.
- **Registro explícito em código**, em que o plugin se registra no núcleo durante a inicialização.
- **Registro dinâmico** (*registry*), em que um banco ou serviço permite adicionar e remover plugins em tempo de execução.

Um bom contrato é estável, porque cada mudança quebra os plugins existentes, é mínimo, porque define apenas o que o núcleo precisa saber do plugin, e é versionado, para que versões diferentes de plugins possam coexistir.

As forças do estilo são a extensibilidade controlada, a implantação seletiva e o teste isolado das variações, e os limites são o versionamento, o ciclo de vida dos plugins, a segurança e o custo de manter um framework de extensão. O anti-padrão **core creep** ocorre quando o núcleo acumula condicionais particulares e toda mudança volta a exigir alteração no núcleo. O estilo é indicado quando as variações evoluem de forma independente e compartilham invariantes, e não é indicado quando os plugins precisam controlar estado interno do núcleo ou quando existe uma única implementação.

Na **Triagem** hospitalar, o núcleo controla identificação, estados e auditoria, e os plugins, selecionados pelo registro, aplicam o formulário ou a validação de cada unidade. Se um plugin editar dados internos do núcleo ou se o núcleo passar a conter regra específica de uma unidade, o core creep indica que a fronteira precisa ser revista.

### Características arquiteturais do Microkernel

As notas de Microkernel ocupam a terceira coluna da [figura 3](#comparacao-dos-quatro-estilos) e seguem Richards e Ford (*Fundamentals of Software Architecture*, cap. 12).

<details markdown="1">
<summary>Observações por característica</summary>

| Característica | Avaliação (1 a 5) | Observação |
| --- | --- | --- |
| Custo geral | 3 | custo médio, exige design cuidadoso do contrato do núcleo |
| Simplicidade | 3 | conceito simples, a implementação do contrato requer disciplina |
| Escalabilidade | 3 | escala como unidade, plugins podem ser carregados e descarregados |
| Elasticidade | 3 | similar à escalabilidade |
| Implantabilidade | 3 | plugins podem ser implantados independentemente do núcleo |
| Testabilidade | 3 | o núcleo é fácil de testar, plugins requerem integração com o núcleo |
| Desempenho | 3 | overhead de dispatch para plugins, geralmente aceitável |
| Modularidade | 4 | destaque do estilo: plugins completamente independentes entre si |
| Confiabilidade | 3 | plugin com falha pode ser isolado sem derrubar o núcleo |

</details>

### Formas de implantação dos plugins

O mesmo contrato admite três formas de implantação do plugin, com custos diferentes de operação e de independência:

| Forma | Descrição | Custo |
| --- | --- | --- |
| **In-process** | plugin carregado no mesmo processo do núcleo | simples e performático, implanta junto com o núcleo |
| **Out-of-process** | plugin como processo ou serviço separado | implantação e escala independentes, latência de rede |
| **SaaS** | plugin como serviço externo na nuvem | máxima independência, dependência de disponibilidade externa |

### Cálculo de impostos como caso de referência

Richards e Ford usam sistemas tributários como caso de referência do Microkernel, e a figura 9 desenha esse caso: as regras fiscais variam por estado, e o fluxo de cálculo é o mesmo para todos os estados. O núcleo seleciona pelo registro o plugin do estado do pedido, e o suporte a um novo estado exige apenas registrar um novo plugin, sem alteração no núcleo.

O core creep aparece quando essa seleção é implementada como condicionais dentro do núcleo:

```python
# Errado: lógica de plugin dentro do núcleo
class SistemaFiscalComCreep:
    def calcular(self, pedido: Pedido) -> float:
        if pedido.estado == "SP":
            return pedido.valor_base * 0.12  # lógica de plugin no núcleo
        elif pedido.estado == "RJ":
            return pedido.valor_base * 0.20
        # cada novo estado exige modificar o núcleo
```

Quando o núcleo acumula condicionais por tipo de cliente ou região, cada nova variação exige alterar o núcleo, e por isso toda lógica que varia entre clientes deve ficar num plugin. Um exemplo executável completo, com núcleo, contrato e plugins de impostos e frete, está em `codigos/cap01-estilos-fundamentais/1.4-microkernel` e é explorado na [oficina de ferramentas](oficina-de-ferramentas.md).

### Exemplos em produtos conhecidos

| Sistema | Núcleo | Plugins |
| --- | --- | --- |
| **Eclipse IDE** | plataforma OSGi e runtime | suporte a linguagens, debug, integração SCM |
| **Jenkins** | motor de pipeline e scheduler | build steps, notificações, cloud providers |
| **VS Code** | editor base e LSP | extensões de linguagem, temas, debug |
| **WordPress** | CMS base e sistema de hooks | temas, SEO, e-commerce, analytics |
| **Sistemas ERP** | módulo financeiro base | RH, manufatura, CRM por segmento |

### Quando usar Microkernel

Recomenda-se Microkernel quando:

- O produto precisa ser personalizado para clientes ou mercados diferentes sem alteração do código central.
- Equipes diferentes desenvolvem extensões de forma independente e em paralelo.
- As regras de negócio variam por segmento fiscal, regulatório ou regional.
- O produto é uma plataforma estendida por terceiros.

Microkernel não é indicado quando:

- O sistema tem um único cliente e regras estáveis, situação em que o custo do contrato e do registro não se justifica.
- As extensões precisam compartilhar estado entre si, o que elimina o isolamento do padrão.
- A lógica se organiza por responsabilidade técnica, caso descrito em [Camadas](#camadas).
- O processamento segue um fluxo sequencial de dados, caso descrito em [Pipes and Filters](#pipes-and-filters).

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly, 2022, cap. 12), Shaw e Garlan (*Software Architecture: Perspectives on an Emerging Discipline*, Prentice Hall, 1996) e Bass, Clements e Kazman (*Software Architecture in Practice*, 3ª ed., Addison-Wesley, 2012).

### Monólito modular {#monolito-modular}

> Pense numa casa em que todos os cômodos ficam sob o mesmo teto e cada cômodo tem paredes e porta próprias.

No monólito modular há uma única implantação, e os módulos Agenda, Triagem, Faturamento e Auditoria mantêm modelos e interfaces próprios. Uma pasta separada não basta para criar uma fronteira efetiva, que depende de proibir consultas diretas e imports internos entre módulos e de revisar os contratos. A decisão deve ser reavaliada quando houver medição de escala, de falha ou de necessidade de implantação independente.

Kamil Grzybek define um monólito como um sistema com exatamente uma unidade de implantação, definição que separa a decisão de implantação da decisão de organização interna. O monólito modular aproveita essa separação: uma única unidade implantável é organizada em módulos alinhados ao domínio, em **fatias verticais** que reúnem API, casos de uso, regras e persistência de uma capacidade de negócio. Cada módulo é dono do próprio comportamento e dos próprios dados, expõe-se por um contrato estável e mantém o restante encapsulado. Richards e Ford dedicam um capítulo ao estilo na 2ª edição de *Fundamentals of Software Architecture*, e Simon Brown divulgou o estilo em palestras a partir de 2015 com a pergunta: se uma equipe não consegue construir um monólito bem estruturado, por que microsserviços resolveriam o problema dela?

![Na parte superior, uma unidade de implantação contém os módulos Triagem, Agenda e Faturamento, cada um com API pública, regras e dados. O Faturamento chama a API pública da Agenda, o que é permitido, e uma seta vermelha com um X liga o Faturamento aos dados da Agenda para marcar o acesso proibido. Na parte inferior, depois de evidência medida, o Faturamento passa a ser um serviço com implantação própria e chama a Agenda pela mesma API, agora por HTTP.](../assets/images/m01-monolito-modular.svg)

*Figura 10 — Monólito modular antes e depois da extração de um módulo. Fonte: curso.*

**Leitura textual da figura:** na parte superior, os módulos Triagem, Agenda e Faturamento convivem numa unidade de implantação, cada um com API pública, regras e dados próprios. O Faturamento chama a API pública da Agenda, e o acesso direto do Faturamento aos dados da Agenda é proibido. Na parte inferior, depois de evidência medida, como módulo quente, raio de incidente ou cadência própria, o Faturamento sai como serviço com implantação própria e continua consumindo a Agenda pelo mesmo contrato, agora por HTTP.

Um módulo consome outro apenas pela API pública, por chamada síncrona ou por assinatura de eventos de domínio, e cada conjunto de dados tem **um único escritor**. Módulos podem compartilhar o mesmo banco físico desde que não compartilhem tabelas nem modelos de escrita, as transações são locais a cada módulo, e fluxos que atravessam módulos são coordenados por eventos ou por orquestração. Somente os tipos exigidos pelo contrato são públicos, e qualquer tipo exposto passa a fazer parte da API pública do módulo e precisa permanecer estável.

O anti-padrão característico é o módulo que lê a tabela ou o modelo interno de outro módulo, prática facilitada pelo fato de a pasta vizinha estar acessível por um import. Sem verificação automática, a separação em módulos existe apenas na estrutura de pastas:

```python
# Errado: Faturamento lê o modelo interno da Agenda
from agenda.infraestrutura.modelos import ReservaModel

class RelatorioFaturamento:
    def gerar(self) -> list[dict]:
        return [r.como_dict() for r in ReservaModel.buscar_do_dia()]

# Correto: Faturamento consome o contrato público da Agenda
from agenda.api import AgendaAPI

class RelatorioFaturamento:
    def __init__(self, agenda: AgendaAPI):
        self._agenda = agenda

    def gerar(self) -> list[dict]:
        return self._agenda.reservas_do_dia()
```

#### Fronteiras verificadas por ferramenta

A fronteira entre módulos deve ser verificada por ferramenta na integração contínua, e os principais ecossistemas oferecem apoio direto a essa verificação:

| Ecossistema | Ferramentas | Mecanismo |
| --- | --- | --- |
| Java e Spring | Spring Modulith, ArchUnit | módulos declarados e testes de arquitetura (*fitness functions*) |
| Python | import-linter, pytestarch | regras de dependência entre pacotes |
| .NET | NetArchTest | verificação de dependências entre assemblies |
| Ruby | Packwerk | pacotes com API pública e dependências declaradas |
| TypeScript | Nx, dependency-cruiser | regras de workspace em monorepos |

O caso mais citado é o da Shopify, que mantém um dos maiores monólitos Ruby on Rails em produção, com milhares de componentes e centenas de implantações por dia, e verifica as fronteiras com o Packwerk na integração contínua. Cada pacote declara sua API pública e suas dependências permitidas, e uma violação bloqueia a integração.

#### Características arquiteturais do Monólito modular

As notas de Monólito modular ocupam a quarta coluna da [figura 3](#comparacao-dos-quatro-estilos) e são uma avaliação do curso na mesma escala. O estilo mantém o custo e a simplicidade do monólito e melhora implantabilidade, testabilidade e modularidade em relação às camadas, e a escalabilidade, a elasticidade e o isolamento de falhas permanecem os de um processo único.

<details markdown="1">
<summary>Observações por característica</summary>

| Característica | Avaliação (1 a 5) | Observação |
| --- | --- | --- |
| Custo geral | 5 | mantém o baixo custo do monólito, a disciplina de fronteiras é o investimento |
| Simplicidade | 4 | conceito direto, exige disciplina e verificação de fronteiras |
| Escalabilidade | 2 | escala por réplica do processo inteiro, como nas camadas |
| Elasticidade | 1 | expansão e retração continuam por unidade única |
| Implantabilidade | 3 | uma unidade de implantação, mas regressões ficam contidas nos módulos |
| Testabilidade | 4 | módulos testáveis em isolamento pelo contrato |
| Desempenho | 4 | chamadas em processo, sem latência de rede entre capacidades |
| Modularidade | 4 | fatias verticais com contrato, depende de verificação automática |
| Confiabilidade | 3 | uma falha ainda derruba o processo, o raio de dano é o sistema inteiro |

</details>

#### Extração de um módulo para serviço

A extração de um módulo para um serviço é uma opção que a boa modularidade torna barata e que só deve ser exercida com evidência medida. Há quatro gatilhos para a extração: mudanças que exigem coordenação entre módulos com frequência sustentada, incidentes cujo raio atravessa fronteiras, um módulo quente que domina os recursos do processo e cadências de mudança muito diferentes entre módulos. Com a evidência, o contrato do módulo passa a ser a fronteira do serviço, como mostra a parte inferior da figura 10, tema retomado na [Unidade 3](../modulo-3-servicos/index.md).

#### Quando usar Monólito modular

Recomenda-se o monólito modular quando:

- A equipe e a operação ainda funcionam como uma unidade e implantar um único artefato é suficiente.
- As fronteiras de domínio ainda estão sendo descobertas e precisam continuar fáceis de mudar.
- Consistência forte e transações locais são requisitos.
- A velocidade de desenvolvimento e o baixo custo operacional pesam mais que a escala independente.

O monólito modular não é indicado quando:

- Módulos precisam escalar de forma independente ou exigem isolamento rígido de falhas.
- Times autônomos precisam implantar em cadências próprias.
- O raio de dano de um incidente precisa ficar contido numa única capacidade.

Nesses casos, a decomposição em serviços da [Unidade 3](../modulo-3-servicos/index.md) é o passo seguinte.

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly), Grzybek (*Modular Monolith: A Primer*, 2019), Brown (*Modular Monoliths*, palestras a partir de 2015) e o relato de engenharia da Shopify (*Deconstructing the Monolith*, 2019).

## Registro da escolha em ADR {#adr-o-mecanismo-para-escolher-estilos}

Um ADR (*Architecture Decision Record*) é um registro de decisão arquitetural, isto é, uma prática de documentação de decisões. É a principal ferramenta do arquiteto para registrar por que um ou mais estilos foram aplicados no desenho ou na evolução de uma arquitetura de software.

Na prática, um ADR é um documento Markdown versionado com contexto, forças, alternativas, decisão, consequências, evidências e revisão, e o [template do curso](../referencia/template-adr.md) traz essa estrutura pronta para uso.
