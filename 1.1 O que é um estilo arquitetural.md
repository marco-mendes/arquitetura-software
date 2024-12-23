
# Sobre estilos arquiteturais

## O que é um estilo arquitetural?

Considere a figura abaixo? <p>
Por que faria sentido projetar uma casa de madeira com telhados pontudos?

<img width="1092" alt="Estilos Arquiteturais" src="https://github.com/user-attachments/assets/f8d9f646-4731-43b6-b6c4-98d1276ec2a8" />
Fonte: ShutterStock
<p></p>

* Em arquitetura, a função segue a forma. Ou seja, uma casa de forma de madeira tem uma função, que é operar como isolamento térmico e impedir o acúmulo de neve no telhado.

* Um estilo arquitetural é uma escolha crucial que o time de arquitetura deve fazer em um projeto.  Ele representa uma abordagem estratégica para projetar, implementar e distribuir uma aplicação.  Dentro do campo da arquitetura de software para TI, existem diversos estilos arquiteturais disponíveis, cada um com suas próprias vantagens e desvantagens. 

* É importante que um arquiteto esteja familiarizado com esses estilos e seja capaz de avaliá-los de acordo com o contexto específico do projeto. É importante notar que não existem estilos arquiteturais universais que sejam melhores ou piores em todas as situações. A escolha do estilo arquitetural deve ser feita com base no contexto específico do projeto e na análise dos requisitos do usuário.

**Lembre-se! A escolha do estilo arquitetural é a maior decisão na definição da arquitetura.**


## Exemplos de estilos arquiteturais

<img width="659" alt="image" src="https://github.com/user-attachments/assets/1a9ebdb9-c038-4033-8055-930f18a0b157" />

---

**1. Arquitetura em Camadas (Layered Architecture)**

* A arquitetura em camadas organiza o sistema em grupos hierárquicos de responsabilidades, com comunicação claramente definida entre as camadas adjacentes. Cada camada isola uma parte da funcionalidade, como interface de usuário, lógica de negócios e persistência de dados. Esse estilo é amplamente adotado devido à sua simplicidade e ao alinhamento natural com paradigmas de desenvolvimento modular. Ele facilita a separação de responsabilidades, tornando a manutenção, substituição de componentes e o teste mais simples.

* Por exemplo, a camada de apresentação (UI) interage apenas com a camada de lógica de negócios, que, por sua vez, acessa os dados por meio de uma camada de persistência. Isso cria uma dependência unidirecional que reduz o acoplamento e melhora a coesão interna de cada camada. Entretanto, a navegação rígida entre as camadas pode trazer desafios de desempenho, especialmente em sistemas que demandam alta resposta em tempo real.

* Esse estilo é particularmente indicado para sistemas empresariais com escopos bem definidos e estruturas organizacionais que demandam independência entre equipes de desenvolvimento. Patterns of Enterprise Application Architecture, de Martin Fowler, é uma referência essencial que explora este paradigma e inclui exemplos detalhados de implementação prática. Link: .

---

**2. Model-View-Controller (MVC)****

* O padrão arquitetural MVC separa uma aplicação em três componentes interligados: Model (dados e lógica de negócios), View (interface do usuário) e Controller (ponte entre Model e View). Criado originalmente para o desenvolvimento de interfaces gráficas no Smalltalk, o MVC é amplamente utilizado em aplicações web devido à sua capacidade de isolar responsabilidades, simplificando a manutenção e evolução de sistemas.

* Model: Representa os dados e as regras de negócios. Ele encapsula o estado da aplicação e é responsável por gerenciar o comportamento do domínio.

* View: Exibe os dados do Model ao usuário. Essa camada é passiva e depende do Controller para interagir com os dados.

* Controller: Manipula a entrada do usuário, processa as interações e atualiza o Model ou a View.

* Um dos principais benefícios do MVC é o desacoplamento, permitindo que as equipes trabalhem em paralelo nas diferentes camadas. No entanto, a complexidade pode aumentar em sistemas com interações intensas entre camadas, como atualizações frequentes de dados em tempo real.

* Referência: O livro Design Patterns: Elements of Reusable Object-Oriented Software por Erich Gamma, Richard Helm, Ralph Johnson, e John Vlissides apresenta os fundamentos de padrões como MVC.

---

**3. Model-View-ViewModel (MVVM)**

* O padrão MVVM é uma evolução do MVC, projetado para facilitar o desenvolvimento de interfaces ricas e reativas. Ele introduz o conceito de ViewModel, que atua como um intermediário entre a View e o Model, permitindo um binding bidirecional de dados e eventos. Popularizado no desenvolvimento de aplicações WPF (Windows Presentation Foundation), o MVVM é amplamente adotado em frameworks como Angular e React.

* Model: Gerencia os dados e a lógica de negócios, semelhante ao MVC.

* View: Representa a interface do usuário e é responsável por exibir os dados de forma declarativa.

* ViewModel: Exposição do estado da View e manipulação de comandos. Ele encapsula lógica de apresentação, mantendo a View desacoplada do Model.
Uma das vantagens principais do MVVM é o binding de dados, que reduz a necessidade de código repetitivo e facilita a testabilidade. Contudo, pode ser mais difícil gerenciar a complexidade à medida que o número de bindings cresce em grandes aplicações.

* Referência: MVVM in WPF por Laurent Bugnion é um guia prático para entender e aplicar este padrão no contexto de interfaces ricas.

---

**4. Domain-Driven Design (DDD)**

* DDD é uma abordagem para design de software que foca na modelagem de sistemas complexos baseando-se no domínio do problema e na colaboração contínua entre especialistas de negócios e desenvolvedores. Proposto por Eric Evans em seu livro seminal, o DDD visa criar um modelo de domínio que reflete as necessidades reais do negócio, garantindo alinhamento contínuo entre a solução técnica e os objetivos organizacionais.

* Entidades: Representam objetos do domínio com identidade persistente ao longo do tempo.

* Value Objects: Representam descrições de aspectos do domínio sem identidade própria.

* Agregados: Conjuntos de objetos que mantêm uma consistência transacional e lógica.

* Repositórios: Interfaces que gerenciam o ciclo de vida das entidades.

* Linguagem ubíqua: Linguagem comum que une especialistas do domínio e desenvolvedores.

* DDD é ideal para sistemas com alta complexidade, onde a lógica de negócios é central. No entanto, sua aplicação pode demandar um esforço significativo de aprendizado e implementação inicial.

* Referência : Domain-Driven Design: Tackling Complexity in the Heart of Software de Eric Evans.

---

**5. Arquitetura Hexagonal (Hexagonal Architecture)**

* Conhecida também como Ports and Adapters, a Arquitetura Hexagonal promove uma separação clara entre o núcleo da aplicação (lógica de negócios) e as interfaces externas (entradas e saídas). Este estilo ajuda a reduzir o acoplamento ao permitir que os adaptadores se conectem aos sistemas externos, como APIs, bancos de dados ou interfaces de usuário, enquanto a lógica de negócios permanece independente e testável.

* Um dos grandes benefícios é a facilidade de teste, já que o núcleo da aplicação pode ser testado isoladamente de suas dependências externas. Além disso, mudanças em sistemas periféricos, como o banco de dados ou interfaces externas, podem ser realizadas sem impactar diretamente o núcleo da aplicação. Contudo, esse modelo exige maior esforço inicial de design para garantir uma implementação eficaz.

* Explorado no contexto de design de software robusto e escalável, o livro Implementing Domain-Driven Design de Vaughn Vernon apresenta o uso desse estilo com detalhes.

---

**6. Pipes and Filters**

* O estilo arquitetural Pipes and Filters é projetado para sistemas que processam dados em etapas sequenciais. Ele organiza a lógica de aplicação como uma sequência de componentes independentes chamados Filtros, que transformam os dados recebidos, e Pipes, que conectam esses filtros e transportam os dados entre eles. Este estilo é amplamente utilizado em sistemas de processamento de dados, como pipelines de ETL (Extract, Transform, Load), ferramentas de linha de comando e sistemas de streaming.

* Os filtros são altamente modulares e encapsulam funcionalidades específicas, como validação, transformação e agregação. Eles não compartilham estado entre si, o que facilita a substituição ou reordenação sem impacto no restante do pipeline. Já os pipes gerenciam a comunicação, transmitindo dados na forma de fluxos. Em sistemas modernos, tecnologias como Apache Kafka e Apache NiFi utilizam conceitos derivados desse estilo.

* As vantagens incluem flexibilidade, escalabilidade e reusabilidade de componentes, tornando-o ideal para sistemas que requerem processamento em etapas bem definidas. Entretanto, a sobrecarga de comunicação entre os filtros pode ser uma preocupação, especialmente em pipelines longos ou sistemas com alta latência.

* Referência: O livro Enterprise Integration Patterns de Gregor Hohpe explora os conceitos e padrões relacionados, incluindo Pipes and Filters, em sistemas de integração.

---

**7. MicroKernel (Plugin Architecture)**

* O estilo MicroKernel, também conhecido como arquitetura de plugins, separa a funcionalidade central de um sistema (núcleo) das extensões que oferecem capacidades adicionais. Essa abordagem é ideal para sistemas que requerem personalização frequente ou precisam suportar diferentes cenários de uso sem alterar a lógica central. Exemplos incluem sistemas operacionais (como o kernel do Linux), servidores de aplicação e ferramentas como Eclipse IDE.

* O núcleo (MicroKernel) fornece serviços básicos, como gerenciamento de fluxo de trabalho, segurança e infraestrutura de comunicação, enquanto os plugins estendem as funcionalidades do sistema. Essa separação permite que o núcleo permaneça leve e estável, enquanto novos recursos podem ser adicionados dinamicamente como módulos ou plugins.

* As vantagens incluem flexibilidade e extensibilidade, pois novos recursos podem ser desenvolvidos de forma independente do núcleo. No entanto, a compatibilidade entre o núcleo e os plugins pode ser um desafio, exigindo uma interface bem definida e controle rigoroso de versões.

* Referência essencial: Designing Software Architectures: A Practical Approach de Humberto Cervantes e Rick Kazman detalha a aplicação do estilo MicroKernel em diferentes contextos.

---

**8. Arquitetura Baseada em APIs (API-Driven Architecture)**

* A Arquitetura Baseada em APIs é um estilo arquitetural que organiza sistemas em torno de Application Programming Interfaces (APIs), promovendo a interoperabilidade, modularidade e escalabilidade. Nesse modelo, as APIs servem como contratos formais entre diferentes componentes ou sistemas, permitindo que eles se comuniquem e troquem informações de maneira padronizada. Este estilo é amplamente adotado em arquiteturas modernas, especialmente em ecossistemas que combinam microsserviços, integrações externas e aplicações móveis ou web.

* As APIs podem ser classificadas em três tipos principais: APIs internas (para comunicação entre microsserviços ou sistemas internos), APIs externas (expostas para parceiros ou consumidores) e APIs públicas (abertas a qualquer desenvolvedor ou aplicação). Este estilo arquitetural possibilita que as APIs sejam reutilizadas em diferentes contextos, acelerando o desenvolvimento de novas funcionalidades e promovendo a agilidade organizacional.

* A arquitetura baseada em APIs é particularmente poderosa em ecossistemas distribuídos, pois permite que equipes independentes desenvolvam, implantem e escalem serviços sem impactar outros sistemas. Ferramentas como API Gateways (e.g., Kong, AWS API Gateway) fornecem gerenciamento centralizado para autenticação, autorização, limitação de taxa e observabilidade, garantindo segurança e monitoramento robustos. No entanto, o gerenciamento eficaz do ciclo de vida das APIs é crítico para evitar problemas de versionamento e dependências rígidas.

* Uma das maiores vantagens dessa arquitetura é o desacoplamento entre consumidores e provedores, promovendo maior flexibilidade e interoperabilidade. Além disso, ela facilita a transformação digital, pois permite que organizações integrem rapidamente novos parceiros, canais ou serviços em seus sistemas existentes. 

A adoção de uma arquitetura baseada em APIs pode ser um catalisador para a inovação, especialmente em empresas que buscam expandir suas operações digitais ou se integrar a novos mercados. Quando projetada e gerenciada de forma eficaz, ela oferece um modelo sustentável para crescimento e resiliência tecnológica.

---

**9. Arquitetura Baseada em Eventos (Event-Driven Architecture)**

* A Arquitetura Baseada em Eventos (Event-Driven Architecture - EDA) é um estilo arquitetural que organiza o sistema para reagir a eventos como principal mecanismo de comunicação entre seus componentes. Em vez de depender de chamadas síncronas, os eventos permitem a troca de informações de forma assíncrona, criando um sistema mais flexível, escalável e resiliente. Esse estilo é amplamente utilizado em aplicações que exigem processamento em tempo real, como sistemas de monitoramento IoT, comércio eletrônico, e plataformas financeiras.

* Na EDA, um evento é uma alteração no estado de um sistema ou uma ocorrência significativa que deve ser comunicada. Os sistemas baseados em eventos consistem em dois papéis principais: produtores (ou emissores), que geram eventos, e consumidores (ou assinantes), que reagem a esses eventos. A comunicação é geralmente intermediada por um barramento de eventos ou um message broker, como Apache Kafka ou RabbitMQ. Esse modelo promove o desacoplamento entre os componentes, uma vez que os produtores não precisam conhecer os consumidores, e vice-versa.

* Os principais benefícios da arquitetura de eventos incluem escalabilidade, pois os consumidores podem processar os eventos em paralelo, e flexibilidade, já que novos consumidores podem ser adicionados sem impactar os produtores. Além disso, a EDA é ideal para sistemas distribuídos, pois os eventos podem ser propagados em diferentes regiões geográficas com baixa latência. No entanto, ela também apresenta desafios, como a necessidade de gerenciar a consistência eventual dos dados e o risco de sobrecarga em sistemas que geram um grande volume de eventos.

* A arquitetura baseada em eventos é explorada em profundidade no livro Designing Event-Driven Systems de Ben Stopford, que descreve como projetar pipelines de eventos e integrações escaláveis usando plataformas como por exemplo o Kafka. 

Esse estilo arquitetural tem se tornado central em sistemas modernos, alinhando-se às demandas por escalabilidade e processamento em tempo real. Quando implementado corretamente, o modelo baseado em eventos pode transformar a eficiência e a modularidade de sistemas complexos.

---

**10. Arquitetura de Microsserviços (Microservices Architecture)**
* A arquitetura de microsserviços fragmenta sistemas complexos em pequenos serviços independentes, onde cada serviço aborda uma função específica do domínio de negócios. Essa abordagem oferece uma maneira robusta de gerenciar escalabilidade e modularidade, permitindo que os serviços sejam desenvolvidos, implantados e escalados independentemente. Serviços como autenticação, pagamento e catálogo de produtos em um sistema e-commerce são exemplos típicos de microsserviços.

* Uma das principais vantagens é a possibilidade de usar tecnologias e frameworks distintos para cada serviço, dependendo da necessidade. Contudo, essa liberdade traz desafios em orquestração e comunicação, exigindo mecanismos robustos como API Gateways e malhas de serviço (e.g., Istio). Além disso, o controle de transações distribuídas e a observabilidade representam desafios significativos para arquiteturas baseadas em microsserviços.

* O livro Building Microservices de Sam Newman oferece uma visão prática sobre como implementar esse estilo, abordando desafios e melhores práticas. 

---
**11. Arquitetura Strangler (Strangler Pattern)**
* O Strangler Pattern é ideal para modernizar sistemas legados, permitindo que novos componentes sejam introduzidos de forma incremental enquanto o sistema antigo continua operando. Inspirado por árvores que crescem ao redor de outras, eventualmente substituindo-as, esse estilo promove transições seguras e gradativas.

* A principal vantagem é a redução de risco associado a grandes migrações, uma vez que cada componente é substituído por uma nova implementação em fases. No entanto, é essencial planejar uma estratégia de integração clara, com ferramentas de roteamento e proxies para garantir a continuidade das operações. Além disso, esse padrão pode prolongar o tempo de migração se não houver uma estratégia bem definida.

* Discutido por Martin Fowler em seu artigo homônimo, o Strangler Pattern é amplamente utilizado para transformar monolitos em arquiteturas baseadas em microsserviços.

---

Para saber mais:

* Livro - [Fundamentals of Software Architecture, 2End Edition, de Mark Richards e Neal Ford](https://learning.oreilly.com/library/view/fundamentals-of-software/9781098175504/) 
