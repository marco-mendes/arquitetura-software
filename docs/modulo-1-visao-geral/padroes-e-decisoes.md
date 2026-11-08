## Padrões, tecnologias e decisões

Esta seção examina estilos arquiteturais que ajudam a organizar softwares complexos.

## Quatro organizações, quatro tipos de fronteira

| Estilo            | Responsabilidade e Conectores                                                    | Forças                                        | Anti-padrão                             | Quando usar                                    | Evite quando                                       |
| ----------------- | -------------------------------------------------------------------------------- | --------------------------------------------- | --------------------------------------- | ---------------------------------------------- | -------------------------------------------------- |
| Camadas           | Separar interface, casos de uso, regras e infraestrutura por chamadas permitidas | testabilidade e mudança localizada            | sumidouro ou atalho oculto              | regras precisam ser isoladas da infraestrutura | a passagem obrigatória não agrega trabalho         |
| Pipes and Filters | Transformar dados por pipes com contratos de entrada, saída e rejeição           | composição e throughput                       | estado compartilhado invisível          | etapas de transformação são explícitas         | o fluxo é interativo e exige consistência imediata |
| Microkernel       | Manter invariantes no núcleo e variações por contrato de plugin                  | extensibilidade e modificabilidade            | core creep                              | variações podem entrar e sair isoladamente     | plugins precisam controlar detalhes do núcleo      |
| Monólito modular  | Organizar capacidades por interfaces internas numa implantação                   | simplicidade operacional e consistência local | módulos que leem dados internos alheios | equipe e operação ainda são uma unidade        | escala ou implantação independente já foi medida   |

Richards e Ford avaliam cada estilo com nove características numa escala de 1 (fraco) a 5 (forte), e a figura 3 reúne as quatro avaliações num único quadro para comparação direta. As observações de cada nota ficam recolhidas na seção de cada estilo.

![Mapa de calor com nove características nas linhas e quatro estilos nas colunas, em escala de 1 a 5; Pipes and Filters se destaca em testabilidade e modularidade, Microkernel fica em 3 na maioria das características, e Camadas e Monólito modular têm custo e simplicidade altos com elasticidade 1.](../assets/images/m01-caracteristicas-estilos.svg)

*Figura 3 — Características arquiteturais dos quatro estilos, de 1 a 5. Fonte: curso.*

**Leitura textual da figura:** Camadas recebe 5 em custo e simplicidade, 3 em testabilidade, desempenho e confiabilidade, 2 em escalabilidade, implantabilidade e modularidade e 1 em elasticidade. Pipes and Filters recebe 5 em custo, simplicidade, testabilidade e modularidade, 3 em implantabilidade e confiabilidade e 2 em escalabilidade, elasticidade e desempenho. Microkernel recebe 4 em modularidade e 3 nas demais. Monólito modular, avaliado pelo curso na mesma escala, recebe 5 em custo, 4 em simplicidade, testabilidade, desempenho e modularidade, 3 em implantabilidade e confiabilidade, 2 em escalabilidade e 1 em elasticidade.

## Camadas {#camadas}

> Pense nos andares de um prédio: cada andar conversa só com o vizinho, sem pular direto para outro.

Camadas é uma regra de dependência, não somente caixas empilhadas. A apresentação traduz interação e formato; a aplicação coordena casos de uso; o domínio preserva as regras e **invariantes** (condições que precisam valer sempre, como um saldo que nunca pode ficar negativo); a infraestrutura oferece banco, mensageria e outros adaptadores. Cada chamada atravessa uma fronteira conhecida, para que a regra de negócio possa ser exercitada sem iniciar HTTP ou banco.

O estilo em camadas (*layered architecture*) é o mais difundido da engenharia de software por um motivo simples: ele emerge naturalmente da estrutura da maioria das equipes. Mark Richards e Neal Ford descrevem esse fenômeno em *Fundamentals of Software Architecture* como *architecture by implication* — o estilo surge por inércia, não por decisão deliberada. A **Lei de Conway** explica o porquê: organizações produzem arquiteturas que espelham sua estrutura de comunicação. Uma equipe dividida em frontend, backend e banco de dados tende a produzir um sistema em três camadas — apresentação, negócios e dados —, mesmo que o arquiteto não tenha planejado isso. A forma apresentada nesta página refina a camada de negócios em aplicação e domínio.

![Quatro camadas empilhadas: Apresentação chama Aplicação, que usa Domínio e Infraestrutura, e a Infraestrutura acessa o banco. Uma seta tracejada azul da Apresentação à Infraestrutura marca a camada aberta deliberada; uma seta vermelha com um X da Apresentação ao banco marca o atalho proibido.](../assets/images/m01-camadas-dependencias.svg)

*Figura 4 — Dependência permitida, atalho deliberado e atalho proibido em camadas. Fonte: curso.*

**Leitura textual da figura:** a Apresentação chama a Aplicação, que usa as regras do Domínio e os mecanismos da Infraestrutura, e só a Infraestrutura acessa o banco. A seta tracejada azul liga a Apresentação à Infraestrutura e representa uma camada aberta, um atalho de leitura registrado em ADR. A seta vermelha liga a Apresentação ao banco e representa o atalho proibido, que contorna a regra de negócio.

Uma **camada fechada** obriga a passagem pela camada adjacente e protege uma regra, garantindo que mudanças numa camada não se propaguem para as outras, ao custo de cada requisição percorrer todas as camadas, mesmo quando é simples. Uma **camada aberta** permite um atalho deliberado, com contrato e teste, para reduzir o custo de uma leitura, e paga isso com acoplamento difuso que corrói o isolamento com o tempo. Por isso a decisão de abrir ou fechar cada camada deve ser documentada num ADR.

O anti-padrão do **sumidouro** aparece quando a passagem repetida não toma decisão, não valida e não transforma nada. Uma consulta simples é legítima, e o sinal de problema é a predominância de travessias sem propósito, que a figura 5 contrasta com uma camada que decide.

![Dois painéis. À esquerda, GET /usuarios atravessa Apresentação, Negócios e Dados em cinza, e cada camada só repassa. À direita, POST /consultas atravessa as mesmas camadas, que validam o formato, recusam horário sobreposto com 409 Conflito e gravam a consulta. Uma faixa inferior traz a regra dos 80%.](../assets/images/m01-sumidouro.svg)

*Figura 5 — Sumidouro comparado a uma camada que decide. Fonte: curso.*

**Leitura textual da figura:** no painel do sumidouro, a requisição GET /usuarios passa por apresentação, negócios e dados até o banco sem que nenhuma camada decida. No painel da camada que decide, a apresentação valida o formato de POST /consultas, a camada de negócios recusa o horário sobreposto com 409 Conflito e a camada de dados grava a consulta. A faixa inferior registra a regra prática de Richards e Ford: se mais de 80% das requisições se comportam como o painel da esquerda, o estilo em camadas provavelmente não serve ao sistema.

As forças são testabilidade, mudança localizada e dependência rastreável; os limites são latência, abstrações desnecessárias e sumidouro. Use camadas quando invariantes precisam sobreviver à troca de interface ou infraestrutura; abra leitura somente com evidência de custo e sem contornar regra.

### Características arquiteturais do estilo

As notas de Camadas estão na primeira coluna da [figura 3](#quatro-organizacoes-quatro-tipos-de-fronteira), segundo Richards e Ford (*Fundamentals of Software Architecture*, cap. 10).

<details markdown="1">
<summary>Observações por característica</summary>

| Característica   | Avaliação (1 a 5) | Observação                                                                             |
| ---------------- | ----------------- | -------------------------------------------------------------------------------------- |
| Custo geral      | 5                 | baixo custo de entrada; tecnologia amplamente conhecida                                |
| Simplicidade     | 5                 | fácil de compreender e implementar                                                     |
| Escalabilidade   | 2                 | escala como unidade única; difícil escalar camadas individualmente                     |
| Elasticidade     | 1                 | pouca capacidade de expansão e retração rápidas sob carga variável                     |
| Implantabilidade | 2                 | uma unidade de implantação; qualquer mudança implanta o pacote inteiro                 |
| Testabilidade    | 3                 | camadas podem ser testadas em isolamento com dublês de teste                           |
| Desempenho       | 3                 | adequado na maioria dos casos; sobrecarga quando a requisição atravessa muitas camadas |
| Modularidade     | 2                 | modular logicamente, mas fisicamente acoplado                                          |
| Confiabilidade   | 3                 | falha em um componente pode afetar o sistema inteiro                                   |

</details>

### O princípio aberto-fechado na fronteira com os dados

O **OCP** (*Open-Closed Principle*) aplicado à fronteira entre camadas significa abstrair o acesso ao banco de dados por uma interface: a camada de negócios depende da abstração, não da implementação concreta. Trocar o banco — de MySQL para PostgreSQL, por exemplo — não altera o serviço de negócio.

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

Repare no que o serviço faz **antes** de chamar `salvar`: consulta a agenda do dia e recusa a sobreposição. Essa decisão justifica a existência da camada. Se `agendar` apenas repassasse os argumentos ao repositório, a camada de negócios não decidiria nada — seria o sumidouro da figura 5, cobrando uma chamada extra sem devolver benefício. A regra de conflito pode ser testada com um repositório dublê, sem banco algum.

O exemplo executável completo está em `codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas`, explorado na [oficina de ferramentas](oficina-de-ferramentas.md), com a mesma invariante e um controller HTTP que devolve `409` no conflito.

### Variações no backend: MVC e DDD

**MVC** (*Model-View-Controller*) é a especialização do estilo em camadas para o ciclo requisição-resposta HTTP: o controller orquestra a requisição, o model concentra as regras de negócio e a view serializa a resposta — em APIs, tipicamente em JSON.

A figura 6 coloca o ciclo do MVC ao lado da estrutura do DDD, descrito a seguir, para mostrar os dois critérios de separação.

![Dois painéis. MVC: o cliente HTTP envia POST /pedidos ao Controller, que aciona o Model, recebe os dados, aciona a View e devolve 200 OK. DDD: dentro da fronteira do agregado, a raiz Pedido contém ItemPedido, que usa o objeto de valor Dinheiro; fora dela, PedidoRepositorio salva e busca a raiz e grava na persistência.](../assets/images/m01-mvc-ddd.svg)

*Figura 6 — MVC separa por papel técnico; DDD separa por conceito do domínio. Fonte: curso.*

**Leitura textual da figura:** no MVC, o cliente envia POST /pedidos ao controller, que aciona o model, recebe os dados processados, aciona a view e devolve 200 OK, nessa ordem numerada. No DDD, a fronteira tracejada do agregado contém a raiz Pedido, a entidade ItemPedido e o objeto de valor Dinheiro; o PedidoRepositorio, fora da fronteira, salva e busca apenas a raiz e grava o agregado na persistência.

O estilo foi consolidado em frameworks amplamente adotados:

| Camada           | Tecnologias                                             |
| ---------------- | ------------------------------------------------------- |
| Controller       | ASP.NET MVC, Spring MVC, Ruby on Rails, Laravel, Django |
| Model e negócios | .NET Core, Spring Boot, Node.js (Express), FastAPI      |
| Dados            | Entity Framework, Hibernate, ActiveRecord, SQLAlchemy   |

**DDD** (*Domain-Driven Design*) organiza a camada de negócios por conceitos do domínio em vez de tipo técnico. Enquanto o MVC separa model, view e controller, o DDD separa Pedido, Pagamento e Cliente — e protege as regras de negócio de cada conceito dentro de seu próprio **agregado** (um grupo de objetos tratado como uma unidade, com uma raiz que controla o acesso ao conjunto). Num exemplo de vendas, o agregado `Pedido` contém entidades `ItemPedido`, usa o objeto de valor `Dinheiro` para preservar invariantes monetárias e é salvo e recuperado por um repositório `PedidoRepositorio`. Prefira DDD a camadas simples quando as regras de negócio são complexas, mudam com frequência e o risco dominante é o mal-entendido entre o time técnico e os especialistas de negócio — tema retomado na [Unidade 3](../modulo-3-servicos/index.md).

### Camadas lógicas e camadas físicas

A arquitetura em camadas define uma estrutura **lógica** — as camadas físicas de implantação (*tiers*) são uma decisão separada.

![Três linhas alinhadas com as mesmas colunas Apresentação, Negócios, Dados e Banco. Na primeira, tudo está num único processo com banco embutido. Na segunda, um servidor de aplicação reúne as três camadas e fala por TCP com o banco em outro servidor. Na terceira, cada camada é um serviço, ligados por HTTP e gRPC. Selos âmbar marcam cada travessia de rede.](../assets/images/m01-camadas-fisicas.svg)

*Figura 7 — As mesmas camadas lógicas em uma, duas e três camadas físicas. Fonte: curso.*

**Leitura textual da figura:** as colunas mantêm as mesmas camadas lógicas nas três linhas, e só os contornos de processo mudam. Com uma camada física não há travessia de rede entre camadas; com duas, há uma travessia por TCP até o banco; com três, há travessias por HTTP entre apresentação e negócios e por gRPC entre negócios e dados.

Cada arranjo troca simplicidade por independência:

| Camadas físicas | Exemplo                                                | Vantagens                                                                 | Desvantagens                                                            |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Uma (monolito)  | processo único com banco embutido                      | simplicidade, menor custo, fácil de depurar e empacotar                   | difícil escalar componentes individualmente; risco alto em implantações |
| Duas            | servidor de aplicação e banco de dados separados       | backend e banco evoluem e escalam de forma independente                   | latência de rede entre camadas; gestão de dois serviços                 |
| Três ou mais    | apresentação, negócios e dados como serviços distintos | escalabilidade fina por camada; isolamento de falhas; times independentes | complexidade operacional; latência acumulada; exige observabilidade     |

Distribuir camadas fisicamente não resolve acoplamento lógico mal definido: um sistema com responsabilidades misturadas entre camadas continua acoplado mesmo rodando em servidores separados.

### Quando usar — e quando não usar

**Use camadas quando:** o sistema tem escopo e regras de negócio bem definidos; a equipe é pequena e o orçamento é limitado; velocidade de desenvolvimento inicial importa mais que escalabilidade; o sistema é predominantemente **CRUD** — as quatro operações básicas sobre dados: criar, ler, atualizar e remover — com lógica de negócio moderada.

**Não use camadas quando:** alta escalabilidade ou elasticidade são requisitos não negociáveis; mais de 80% das requisições são sumidouros — o estilo acrescenta latência sem valor; times independentes precisam implantar partes do sistema autonomamente; o problema central é processamento de dados em etapas — compare com [Pipes and Filters](#pipes-and-filters); ou a extensibilidade do produto para diferentes mercados é o driver central — compare com [Microkernel](#microkernel).

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly, 2022, cap. 10), Fowler (*Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002) e Evans (*Domain-Driven Design*, Addison-Wesley, 2003).

## Pipes and Filters {#pipes-and-filters}

> Pense numa esteira de fábrica: cada etapa faz uma coisa e passa o resultado adiante.

Pipes and Filters decompõe uma transformação em filtros ligados por pipes. Cada filtro recebe um valor contratual e devolve novo valor ou **rejeição** explícita; o pipe transporta o resultado sem expor detalhes internos. O contrato nomeia formato, correlação, campos preservados, motivo e destino da rejeição, permitindo testar e observar cada etapa.

Richards e Ford chamam o estilo de *Pipeline Architecture* (*Fundamentals of Software Architecture*, cap. 11). A premissa fundamental é a **ausência de estado compartilhado**: cada filtro recebe dados, os transforma e os emite, sem saber de onde vieram nem para onde vão. Filtros não se comunicam diretamente entre si, apenas através dos pipes — o que torna o sistema altamente modular: filtros podem ser adicionados, removidos ou reordenados sem impactar os demais. Os autores identificam quatro tipos canônicos de filtro, e a figura 8 mostra os quatro num pipeline de pedidos de e-commerce: o leitor constrói o pedido, o validador desvia os inválidos, o aplicador de desconto e o calculador de frete transformam sem descartar, e o finalizador aprova e reporta.

![Cinco filtros em linha ligados por pipes: LeitorDePedido (producer), ValidadorDePedido (tester), AplicadorDeDesconto e CalculadorDeFrete (transformers) e FinalizadorDePedido (consumer). Abaixo de cada pipe aparece o dado que passa por ele; do validador sai uma seta vermelha para a rejeição explícita com lote, etapa e causa.](../assets/images/m01-pipeline-pedidos.svg)

*Figura 8 — Pipeline de pedidos com os quatro tipos de filtro. Fonte: curso.*

**Leitura textual da figura:** o LeitorDePedido cria o pedido e o envia ao ValidadorDePedido. Os pedidos inválidos seguem para a rejeição explícita, que guarda lote, etapa e causa para reprocessamento; os válidos recebem desconto no AplicadorDeDesconto e frete no CalculadorDeFrete e chegam ao FinalizadorDePedido, que aprova e reporta. O quadro inferior lembra que nenhum filtro conhece o vizinho e que nenhum guarda estado.

| Tipo | Papel | Exemplos |
| --- | --- | --- |
| **Producer** | entrada do fluxo; gera ou lê os dados iniciais | leitura de arquivo, chamada a API, leitura de fila |
| **Transformer** | recebe dados, aplica transformação e os emite sem descartar | normalizar campos, enriquecer com dados externos, calcular métricas |
| **Tester** | avalia os dados contra um critério; descarta os que não passam | validar schema, filtrar por nível, separar por categoria |
| **Consumer** | término do fluxo; persiste ou envia os dados processados | gravar no banco, enviar e-mail, publicar em fila |

Um **filtro sem estado** depende apenas da entrada e é simples de repetir ou paralelizar. Um **filtro com estado** depende de memória, banco ou janela temporal; declara armazenamento, recuperação, concorrência e chave de correlação. A **ordenação** também é contrato: paralelize apenas etapas independentes e preserve a sequência exigida pela chave de negócio.

O anti-padrão correspondente é o **estado compartilhado invisível**: um filtro que acumula estado interno sem declará-lo introduz acoplamento implícito e torna o pipeline não determinístico — o resultado passa a depender da ordem de execução. Quando o fluxo requer acumulação, como janelas de tempo em streaming, use um mecanismo externo declarado, como Redis ou um *state store* dedicado, nunca estado interno do filtro.

```python
# Errado: estado de classe compartilhado entre invocações
class FiltroComEstado:
    total = 0

    def processar(self, valor: float) -> float:
        self.total += valor
        return self.total  # o resultado depende da ordem de execução

# Correto: filtro sem estado — cada invocação é independente
class FiltroTransformador:
    def processar(self, dado: dict) -> dict:
        return {**dado, "valor_normalizado": dado["valor"] / 100}
```

As forças são composição, reuso, diagnóstico e controle de **throughput** (a vazão de itens processados por unidade de tempo) por filtro; os limites são contratos intermediários, latência, estado e recuperação parcial. Use quando a sequência de dados e as entradas e saídas são claras; evite interação rica que exige consistência imediata.

No **Faturamento** hospitalar, validar, normalizar códigos, enriquecer dados do convênio e publicar formam um pipeline verificável. A rejeição preserva lote, etapa e causa; a decisão exige medir throughput em ambiente representativo e declarar a ordenação de documentos do mesmo atendimento.

### Características arquiteturais de Pipes and Filters

As notas de Pipes and Filters estão na segunda coluna da [figura 3](#quatro-organizacoes-quatro-tipos-de-fronteira), segundo Richards e Ford (*Fundamentals of Software Architecture*, cap. 11).

<details markdown="1">
<summary>Observações por característica</summary>

| Característica | Avaliação (1 a 5) | Observação |
| --- | --- | --- |
| Custo geral | 5 | baixo custo de entrada; conceito simples e direto |
| Simplicidade | 5 | estrutura linear fácil de entender e de explicar |
| Escalabilidade | 2 | filtros individuais podem escalar; o pipeline como unidade é limitado |
| Elasticidade | 2 | difícil expansão e retração rápidas sob carga variável |
| Implantabilidade | 3 | filtros podem ser implantados separadamente em versões modernas |
| Testabilidade | 5 | destaque do estilo: cada filtro é independente e testável em isolamento |
| Desempenho | 2 | o processamento sequencial introduz latência acumulada |
| Modularidade | 5 | destaque do estilo: máxima modularidade por design |
| Confiabilidade | 3 | falha num filtro interrompe o pipeline; exige estratégias de reprocessamento |

</details>

### Um framework mínimo e um exemplo de pipeline

O padrão cabe em duas classes: um contrato de filtro e um encadeador que executa a sequência.

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

Com esse framework, o pipeline da figura 8 é a sequência `LeitorDePedido`, `ValidadorDePedido`, `AplicadorDeDesconto`, `CalculadorDeFrete` e `FinalizadorDePedido` registrada por chamadas sucessivas a `adicionar`.

O acervo do curso traz ainda um segundo exemplo, que processa linhas de log e mantém apenas os níveis ERROR e CRITICAL. Os dois exemplos executáveis estão em `codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters`, explorados na [oficina de ferramentas](oficina-de-ferramentas.md).

### Quando usar Pipes and Filters — e quando não usar

**Use Pipes and Filters quando:** o problema é um fluxo de transformações de dados, como **ETL** (extrair, transformar e carregar dados de uma origem para um destino), validação em múltiplas etapas ou processamento de logs; a testabilidade isolada de cada etapa é crítica; equipes diferentes desenvolvem etapas de forma independente; ou o pipeline precisa ser composto e recomposto dinamicamente.

**Não use Pipes and Filters quando:** o sistema tem forte lógica de negócio hierárquica — compare com [Camadas](#camadas) e DDD; as etapas precisam compartilhar estado mútuo, o que destrói a independência dos filtros; a latência acumulada das etapas é inaceitável para o caso de uso; ou o fluxo é não linear e requer orquestração complexa — tema das arquiteturas de eventos na [Unidade 5](../modulo-5-eventos/index.md).

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly, 2022, cap. 11), Hohpe e Woolf (*Enterprise Integration Patterns*, Addison-Wesley, 2003) e Shaw e Garlan (*Software Architecture: Perspectives on an Emerging Discipline*, Prentice Hall, 1996).

## Microkernel {#microkernel}

> Pense num videogame com cartuchos: o núcleo é fixo e os encaixes são opcionais.

Microkernel separa um núcleo invariável das extensões. O núcleo preserva identidade, autorização, ciclo de vida e orquestração; o **registro** descobre extensões e seleciona a apropriada. Um **plugin** conhece apenas capacidades públicas, nunca tabelas ou objetos internos.

Richards e Ford chamam o estilo de *Plug-in Architecture* (*Fundamentals of Software Architecture*, cap. 12). A premissa fundamental: o **núcleo evolui lentamente**, enquanto os **plugins evoluem rapidamente** e de forma independente, sem coordenação entre equipes. O núcleo não sabe o que os plugins fazem; os plugins não sabem uns dos outros. A única relação entre eles é o contrato que o núcleo define e que cada plugin implementa.

A figura 9 mostra essa estrutura no caso canônico de cálculo de impostos, detalhado mais adiante.

![À esquerda, o núcleo SistemaFiscal com registro que mapeia SP e RJ a plugins, executor e serviços compartilhados. No centro, a barra do contrato CalculadorImposto. À direita, os plugins ImpostoSPPlugin, ImpostoRJPlugin e um novo estado tracejado encaixados no contrato. Uma faixa vermelha inferior mostra o core creep como um if por estado dentro do núcleo.](../assets/images/m01-microkernel-impostos.svg)

*Figura 9 — Núcleo, contrato e plugins no cálculo de impostos por estado. Fonte: curso.*

**Leitura textual da figura:** o núcleo SistemaFiscal reúne o registro, que mapeia SP e RJ aos seus plugins e seleciona pelo estado do pedido, o executor, que chama o plugin escolhido, e os serviços compartilhados de log, segurança e configuração. O executor chega aos plugins só pelo contrato CalculadorImposto. O plugin de São Paulo aplica 12% a eletrônicos e 18% aos demais produtos, o do Rio de Janeiro aplica 20% em qualquer produto, e um novo estado se registra sem alterar o núcleo. A faixa inferior mostra o core creep: um if por estado dentro do núcleo.

O **contrato de extensão** define entrada, resultado, erros, permissões e versão. A **compatibilidade** usa versão e capacidades: antes de carregar um plugin, o núcleo verifica contrato e dados autorizados. Registro por configuração, convenção ou catálogo dinâmico são variações; plugins no processo simplificam, enquanto serviços separados acrescentam isolamento, latência e operação.

O núcleo contém apenas a funcionalidade mínima para o sistema operar: gerencia o ciclo de vida dos plugins, define e impõe o contrato, orquestra a execução e provê serviços compartilhados. Ele não deve conter lógica de negócio específica — quando acumula lógica que pertence a plugins, o estilo degenera num monolito disfarçado. O registro admite quatro implementações:

- **Arquivo de configuração** (YAML ou JSON) — simples, mas exige reinicialização para alterar plugins;
- **Descoberta por convenção** — o núcleo varre pacotes em busca de classes que implementam a interface;
- **Registro explícito em código** — o plugin se registra no núcleo na inicialização;
- **Registry dinâmico** — banco ou serviço que permite adicionar e remover plugins em tempo de execução.

Um bom contrato é **estável**, porque cada mudança quebra os plugins existentes; **minimalista**, definindo apenas o que o núcleo precisa saber do plugin; e **versionado**, permitindo que versões diferentes de plugins coexistam.

As forças são extensibilidade controlada, implantação seletiva e teste de variações; os limites são versionamento, ciclo de vida, segurança e custo de um framework raro. **core creep** ocorre quando o núcleo acumula condicionais particulares e cada mudança volta ao centro. Use quando variações evoluem independentemente, mas compartilham invariantes; evite quando controlam estado interno ou há uma única implementação.

Na **Triagem** hospitalar, o núcleo controla identificação, estados e auditoria; plugins aplicam formulário ou validação por unidade. O registro seleciona a extensão compatível. Se um plugin editar dados internos ou o núcleo contiver regra por unidade, o core creep pede revisão da fronteira.

### Características arquiteturais do Microkernel

As notas de Microkernel estão na terceira coluna da [figura 3](#quatro-organizacoes-quatro-tipos-de-fronteira), segundo Richards e Ford (*Fundamentals of Software Architecture*, cap. 12).

<details markdown="1">
<summary>Observações por característica</summary>

| Característica | Avaliação (1 a 5) | Observação |
| --- | --- | --- |
| Custo geral | 3 | custo médio; exige design cuidadoso do contrato do núcleo |
| Simplicidade | 3 | conceito simples; a implementação do contrato requer disciplina |
| Escalabilidade | 3 | escala como unidade; plugins podem ser carregados e descarregados |
| Elasticidade | 3 | similar à escalabilidade |
| Implantabilidade | 3 | plugins podem ser implantados independentemente do núcleo |
| Testabilidade | 3 | o núcleo é fácil de testar; plugins requerem integração com o núcleo |
| Desempenho | 3 | overhead de dispatch para plugins; geralmente aceitável |
| Modularidade | 4 | destaque do estilo: plugins completamente independentes entre si |
| Confiabilidade | 3 | plugin com falha pode ser isolado sem derrubar o núcleo |

</details>

### Formas de implantação dos plugins

O mesmo contrato admite três formas de implantar o plugin, que trocam simplicidade por independência:

| Forma | Descrição | Custo |
| --- | --- | --- |
| **In-process** | plugin carregado no mesmo processo do núcleo | simples e performático; implanta junto com o núcleo |
| **Out-of-process** | plugin como processo ou serviço separado | implantação e escala independentes; latência de rede |
| **SaaS** | plugin como serviço externo na nuvem | máxima independência; dependência de disponibilidade externa |

### O caso canônico: cálculo de impostos

Sistemas tributários são o caso canônico de Microkernel em Richards e Ford, e são o caso desenhado na figura 9: as regras fiscais variam por estado, mas o fluxo de cálculo é o mesmo. O núcleo seleciona pelo registro o plugin do estado do pedido, e adicionar suporte a um novo estado significa registrar um novo plugin, sem alterar o núcleo.

O anti-padrão do core creep aparece quando essa seleção vira condicionais dentro do núcleo:

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

Quando o núcleo acumula condicionais por tipo de cliente ou região, a extensibilidade se perde: qualquer lógica que varia entre clientes pertence a um plugin. Um exemplo executável completo — núcleo, contrato e plugins de impostos e frete — está em `codigos/cap01-estilos-fundamentais/1.4-microkernel`, explorado na [oficina de ferramentas](oficina-de-ferramentas.md).

### Exemplos modernos

| Sistema | Núcleo | Plugins |
| --- | --- | --- |
| **Eclipse IDE** | plataforma OSGi e runtime | suporte a linguagens, debug, integração SCM |
| **Jenkins** | motor de pipeline e scheduler | build steps, notificações, cloud providers |
| **VS Code** | editor base e LSP | extensões de linguagem, temas, debug |
| **WordPress** | CMS base e sistema de hooks | temas, SEO, e-commerce, analytics |
| **Sistemas ERP** | módulo financeiro base | RH, manufatura, CRM por segmento |

### Quando usar Microkernel — e quando não usar

**Use Microkernel quando:** o produto precisa ser customizável para diferentes clientes ou mercados sem alterar o código central; equipes diferentes desenvolvem extensões de forma independente e paralela; regras de negócio variam por segmento fiscal, regulatório ou regional; ou o produto é uma plataforma que terceiros estendem.

**Não use Microkernel quando:** o sistema tem um único cliente e regras estáveis — o overhead não se justifica; as extensões precisam compartilhar estado entre si, o que quebra o isolamento do padrão; a lógica é hierárquica por responsabilidade técnica — compare com [Camadas](#camadas); ou o processamento é orientado a fluxo sequencial de dados — compare com [Pipes and Filters](#pipes-and-filters).

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly, 2022, cap. 12), Shaw e Garlan (*Software Architecture: Perspectives on an Emerging Discipline*, Prentice Hall, 1996) e Bass, Clements e Kazman (*Software Architecture in Practice*, 3ª ed., Addison-Wesley, 2012).

### Monólito modular: uma implantação, capacidades com autonomia interna

> Pense numa casa com cômodos bem separados: um só teto, paredes claras entre os cômodos.

Há uma implantação, mas Agenda, Triagem, Faturamento e Auditoria mantêm modelos e interfaces próprias. Uma pasta separada não cria, sozinha, uma fronteira efetiva: evite consulta direta, imports internos e contratos sem revisão. Reavalie quando escala, falha ou implantação independente forem medidos.

Um monólito é apenas um sistema com exatamente uma unidade de implantação — a definição, de Kamil Grzybek, separa a decisão de implantação da decisão de organização interna. O **monólito modular** explora essa separação: uma única unidade implantável, organizada em módulos alinhados ao domínio, em **fatias verticais** que reúnem API, casos de uso, regras e persistência de uma capacidade de negócio — em vez de camadas técnicas horizontais. Cada módulo é dono do próprio comportamento e dos próprios dados, atrás de um contrato estável; o restante fica encapsulado. Richards e Ford dedicam um capítulo ao estilo na 2ª edição de *Fundamentals of Software Architecture*, e Simon Brown popularizou a provocação que o acompanha: se você não consegue construir um monólito bem estruturado, o que faz pensar que microsserviços são a resposta?

![Em cima, uma unidade de implantação com os módulos Triagem, Agenda e Faturamento, cada um com API pública, regras e dados. O Faturamento chama a API da Agenda, permitido, e uma seta vermelha com X do Faturamento aos dados da Agenda marca o acesso proibido. Embaixo, depois de evidência medida, o Faturamento vira serviço com implantação própria e chama a Agenda pela mesma API, agora por HTTP.](../assets/images/m01-monolito-modular.svg)

*Figura 10 — Monólito modular hoje e depois da extração de um módulo. Fonte: curso.*

**Leitura textual da figura:** na parte superior, os módulos Triagem, Agenda e Faturamento convivem numa unidade de implantação, cada um com API pública, regras e dados próprios. O Faturamento chama a API pública da Agenda, e o acesso direto do Faturamento aos dados da Agenda é proibido. Na parte inferior, depois de evidência medida, como módulo quente, raio de incidente ou cadência própria, o Faturamento sai como serviço com implantação própria e continua consumindo a Agenda pelo mesmo contrato, agora por HTTP.

As regras de comunicação sustentam a autonomia: um módulo consome outro apenas pela API pública — por chamada síncrona ou por assinatura de eventos de domínio — e cada conjunto de dados tem **um único escritor**. Módulos podem compartilhar o mesmo banco físico, mas nunca tabelas ou modelos de escrita; transações são locais ao módulo, e fluxos que atravessam módulos se coordenam por eventos ou orquestração. O encapsulamento é a consequência prática: apenas os tipos exigidos pelo contrato são públicos, e tudo o que se expõe passa a ser API pública do módulo, com o dever de estabilidade que isso implica.

O anti-padrão característico é o módulo que lê dados internos alheios — a tabela ou o modelo de outro módulo — porque a pasta vizinha está a um import de distância. Sem verificação automática, os módulos são apenas mecânicos:

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

A fronteira entre módulos precisa ser verificada por ferramenta na integração contínua, não mantida por convenção. Os principais ecossistemas oferecem apoio direto:

| Ecossistema | Ferramentas | Mecanismo |
| --- | --- | --- |
| Java e Spring | Spring Modulith, ArchUnit | módulos declarados e testes de arquitetura (*fitness functions*) |
| Python | import-linter, pytestarch | regras de dependência entre pacotes |
| .NET | NetArchTest | verificação de dependências entre assemblies |
| Ruby | Packwerk | pacotes com API pública e dependências declaradas |
| TypeScript | Nx, dependency-cruiser | regras de workspace em monorepos |

O caso mais citado é o da Shopify, que mantém um dos maiores monólitos Ruby on Rails do mundo — milhares de componentes e centenas de implantações por dia — com fronteiras verificadas pelo Packwerk na integração contínua: cada pacote declara sua API pública e suas dependências permitidas, e violações bloqueiam a integração. O caso mostra que o estilo escala em tamanho de código e de equipe quando a verificação de fronteiras é contínua.

#### Características arquiteturais do Monólito modular

As notas de Monólito modular estão na quarta coluna da [figura 3](#quatro-organizacoes-quatro-tipos-de-fronteira) e são uma avaliação do curso na mesma escala. O estilo mantém o custo e a simplicidade do monólito e melhora implantabilidade, testabilidade e modularidade em relação às camadas, enquanto escalabilidade, elasticidade e isolamento de falhas continuam sendo os de um processo único.

<details markdown="1">
<summary>Observações por característica</summary>

| Característica | Avaliação (1 a 5) | Observação |
| --- | --- | --- |
| Custo geral | 5 | mantém o baixo custo do monólito; a disciplina de fronteiras é o investimento |
| Simplicidade | 4 | conceito direto; exige disciplina e verificação de fronteiras |
| Escalabilidade | 2 | escala por réplica do processo inteiro, como nas camadas |
| Elasticidade | 1 | expansão e retração continuam por unidade única |
| Implantabilidade | 3 | uma unidade de implantação, mas regressões ficam contidas nos módulos |
| Testabilidade | 4 | módulos testáveis em isolamento pelo contrato |
| Desempenho | 4 | chamadas em processo, sem latência de rede entre capacidades |
| Modularidade | 4 | fatias verticais com contrato; depende de verificação automática |
| Confiabilidade | 3 | uma falha ainda derruba o processo; o raio de dano é o sistema inteiro |

</details>

#### Da modularidade à extração de serviços

A extração de um módulo para um serviço é uma opção conquistada pela boa modularidade, não o plano inicial. Os gatilhos que a justificam são medidos, não presumidos: mudanças que exigem coordenação entre módulos com frequência sustentada, raio de incidentes que atravessa fronteiras, um módulo quente dominando os recursos do processo ou cadências de mudança muito diferentes entre módulos. Quando a evidência aparece, o contrato do módulo passa a ser a fronteira do serviço, como mostra a parte inferior da figura 10 — tema retomado na [Unidade 3](../modulo-3-servicos/index.md).

#### Quando usar Monólito modular — e quando não usar

**Use Monólito modular quando:** a equipe e a operação ainda são uma unidade e implantar um artefato basta; as fronteiras de domínio ainda estão sendo descobertas e mudá-las precisa ser barato; consistência forte e transações locais importam; ou a velocidade de desenvolvimento e o baixo custo operacional pesam mais que escala independente.

**Não use Monólito modular quando:** módulos precisam escalar de forma independente ou requerem isolamento rígido de falhas; times autônomos precisam implantar em cadências próprias; ou o raio de dano de um incidente precisa ficar contido numa única capacidade — nesses casos, a decomposição em serviços da [Unidade 3](../modulo-3-servicos/index.md) é o caminho natural.

A discussão do estilo acompanha Richards e Ford (*Fundamentals of Software Architecture*, 2ª ed., O'Reilly), Grzybek (*Modular Monolith: A Primer*, 2019), Brown (*Modular Monoliths*, palestras a partir de 2015) e o relato de engenharia da Shopify (*Deconstructing the Monolith*, 2019).

## ADR: O mecanismo para escolher estilos

Um ADR é um registro de decisão arquitetural — uma prática de documentação de decisões. É a principal ferramenta para o arquiteto registrar o racional da sua escolha da aplicação de um ou mais estilos no desenho ou evolução de arquiteturas de software.

Na prática, um **ADR** é documento Markdown versionado com contexto, forças, alternativas, decisão, consequências, evidências e revisão. O [template](../referencia/template-adr.md) facilita aqui o seu trabalho de usá-lo no curso e no seu trabalho.

##
