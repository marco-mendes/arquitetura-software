# Padrões e decisões para APIs

## Tipos de APIs

![Tipos de APIs conforme o contexto de solução: web, mobile, cloud, integração, omnichannel e IoT, cada um com exemplo real, protocolos de transporte e formatos de dados.](https://github.com/user-attachments/assets/8d90f8d0-aafd-41c4-9c82-0252819ce133)

**Leitura textual da figura:** o quadro compara seis contextos. APIs web alimentam sites e aplicações dinâmicas com HTTP/HTTPS e JSON, XML ou HTML, como a busca de produtos da Amazon. APIs mobile priorizam dados leves e experiência otimizada com HTTPS, HTTP/2, gRPC e WebSocket, como Uber e Instagram. APIs cloud expõem plataformas SaaS para automação e integração entre nuvens, como o Dropbox. APIs de integração conectam empresas e parceiros com contratos rígidos, usando HTTPS, gRPC, SOAP e JMS ou AMQP, como o SAP e as APIs de governo. APIs omnichannel garantem experiência consistente entre canais e dispositivos, como a Shopify. APIs de IoT coletam dados e enviam comandos com MQTT, CoAP, HTTPS e AMQP, como o Google Nest. Uma legenda final resume os protocolos e formatos citados.

---

### API para Soluções Web

Aplicativos da Web exibem páginas da Web dinâmicas. Com base nas solicitações dos usuários, as páginas da Web são criadas dinamicamente com os dados disponíveis no back-end. Os dados exibidos nas páginas da web podem ser exibidos por APIs. O aplicativo da Web extrai os dados brutos das APIs, processa os dados e os exibe em páginas HTML.

Um aplicativo da Web de comércio eletrônico, por exemplo, exibe produtos em um site com base nos critérios de pesquisa do cliente. Os dados do produto são atendidos pela API do produto, que busca os dados do produto de um banco de dados e retorna campos relevantes na forma de uma estrutura JSON. O aplicativo da Web interpreta a estrutura JSON e a transforma em uma página HTML.

**Exemplo Real:**

- **API de Busca de Produtos da Amazon:** Permite que desenvolvedores integrem funções de busca e apresentação de produtos em seus aplicativos personalizados, como sistemas de afiliados.
- **Protocolos de Transporte e Dados:** HTTP/HTTPS para transporte e formatos como JSON ou XML para dados.

---

### API para Soluções Móveis

O número de dispositivos móveis e tablets superou o número de computadores. Os aplicativos para celular são diferentes dos aplicativos de desktop tradicionais, já que a maioria dos aplicativos móveis não é autônoma nem autossuficiente.

Os aplicativos precisam se conectar aos servidores na Internet para serem utilizáveis ou, pelo menos, serem utilizáveis em seu pleno potencial.

Os dados entregues pelas APIs precisam ser leves e particionados. Isso garante que a API possa ser consumida por dispositivos com capacidade de processamento limitada e largura de banda limitada de conexão à Internet.

**Exemplo Real:**

- **API da Uber:** Fornece acesso aos motoristas e passageiros. Se iniciou em protocolo HTTP e JSON. Com o crescimento da Uber, foi modificada para protocolos de alta escalabilidade como o gRPC e o ProtoBuffer.
- **API do Instagram:** Fornece acesso a dados como posts, comentários e publicações recentes, permitindo a criação de experiências otimizadas para dispositivos móveis.
- **GraphQL no Spotify:** Usado para permitir que aplicativos móveis busquem exatamente os dados de álbuns, artistas e playlists em uma única consulta, otimizando a experiência do usuário.
- **Protocolos de Transporte e Dados:** HTTP/HTTPS com JSON para APIs REST e consultas estruturadas no caso de GraphQL.

---

### APIs para Soluções de Nuvens

As soluções em nuvem SaaS normalmente consistem em um aplicativo da Web e APIs. O aplicativo da web é visível para os consumidores.

Embaixo do capô, as soluções em nuvem geralmente oferecem uma API também, no entanto, a API normalmente permanece sob a superfície. Essa API pode ser usada para conectar o aplicativo de nuvem a outros aplicativos de nuvem para realizar a automação ou para conectar a solução de nuvem a aplicativos móveis e software de desktop.

**Exemplo Real:**

- **API do Dropbox:** Permite a sincronização de arquivos com aplicativos de terceiros, como Google Workspace e Microsoft Office.
- **Protocolos de Transporte e Dados:** HTTPS é usado para transporte seguro; os dados são geralmente enviados em JSON para simplicidade.

---

### APIs para Soluções de Integração

APIs fornecem os recursos, que são essenciais para conectar, estender e integrar software. Ao integrar software, as APIs conectam empresas a outras empresas. Eles são usados em soluções de integração de negócios para empresas.

O negócio de uma empresa pode ser expandido conectando-se os negócios aos parceiros para cima e para baixo na cadeia de valor.

Como os negócios são executados pela TI, os negócios podem ser mais bem vinculados, integrando os sistemas de TI de um negócio em toda a cadeia de valor aos sistemas de TI de outras empresas, parceiros, funcionários e, é claro, aos clientes.

**Exemplo Real:**

- **gRPC no Uber:** Usado para comunicação de alta performance entre microserviços e sistemas internos de integração, garantindo baixa latência e maior eficiência.
- **API do SAP:** Integra ERPs corporativos com outros sistemas de TI, permitindo transações entre parceiros de negócios, como fornecedores e clientes.
- **API do Governo Brasileirao (NF-e, e-Social, TISS):** Faz uso extensivo de XML como protocolo de dados devido aos mecansimos avançados da pilha XML para a validacão de dados e segurança da informação.
- **Protocolos de Transporte e Dados:** gRPC (Protocol Buffers) para comunicações de alta eficiência e SOAP ou REST para integrações mais tradicionais.

---

### APIs para Soluções Multicanal

Essas APIs são projetadas para conectar sistemas diferentes, geralmente entre organizações ou dentro de cadeias de valor, possibilitando a automação de processos e troca de dados.

Para melhorar a experiência de compra, os mesmos dados e ações do usuário precisam estar disponíveis em todos os dispositivos do usuário, mesmo que sejam construídos em hardware diferente, executem sistemas operacionais diferentes e aplicativos diferentes.

Soluções Omni-Canal ou soluções multicanais fornecem exatamente isso. Independentemente do canal usado pelos clientes, eles obtêm uma experiência consistente em todos os dispositivos e podem alternar facilmente entre os dispositivos.

**Exemplo Real:**

- **API da Shopify:** Permite a integração de lojas virtuais para oferecer experiências consistentes em dispositivos móveis, desktops e quiosques.
- **Protocolos de Transporte e Dados:** HTTP/HTTPS para transporte, JSON para dados e WebSockets para atualizações em tempo real.

---

### APIs para Soluções IoT

A internet das coisas é composta de dispositivos físicos com uma conexão à internet. Os dispositivos são controlados por software por meio de seus atores ou os dispositivos podem coletar dados por meio de seus sensores. Assim, o dispositivo em si não precisa ser "inteligente", no entanto, ele pode se comportar como um dispositivo inteligente.

O dispositivo se conecta a funções inteligentes, que são expostas na internet por meio de APIs.

Exemplos de tais soluções API incluem wearables inteligentes, carros inteligentes, casas inteligentes ou cidades inteligentes.

**Exemplo Real:**

- **API do Google Nest:** Gerencia dispositivos inteligentes como termostatos e câmeras de segurança remotamente.
- **Protocolos de Transporte e Dados:** MQTT (protocolo leve para dispositivos IoT) ou HTTP/HTTPS para transporte; dados em JSON ou Protocol Buffers para comunicações otimizadas.

## Como pensar em APIs a partir da lente de uma plataforma

![Arquitetura de referência moderna com firewall, gateway de API, servidor web, fila de mensagens, sistemas legados e banco de dados, ao lado da visão de plataforma de APIs com desenvolvimento, execução e engajamento.](https://github.com/user-attachments/assets/1cad9c6b-da09-4bf6-91e4-0620428e4809)

**Leitura textual da figura:** à esquerda, usuários web e mobile acessam o sistema principal: o firewall encaminha as requisições ao gateway de API, que roteia para o servidor web com a lógica de negócios, publica mensagens na fila e consulta e atualiza dois sistemas legados; o servidor web grava no banco de dados. À direita, a plataforma de APIs tem três camadas: a plataforma de desenvolvimento (IDE e extensões, templates, mock servers, testes locais e governança) implanta as APIs na plataforma de execução (gateway, roteamento e transformação, segurança e OAuth, rate limiting e observabilidade), que as publica na plataforma de engajamento (portal do desenvolvedor, documentação e SDKs, catálogo, planos e assinaturas, analytics e feedback). Na base, segurança, escalabilidade, observabilidade, padronização e experiência atravessam o conjunto.

### Ferramentas para Cada Parte da Plataforma de APIs

#### **API Development Platform (Desenvolvimento de APIs)**

1. **Swagger Editor** - Ferramenta para criar especificações de APIs: [Swagger Editor](https://swagger.io/tools/swagger-editor/)
2. **Postman** - Ideal para desenvolvimento e simulação de APIs: [Postman](https://www.postman.com/)
3. **Insomnia** - Cliente HTTP para testar e organizar APIs: [Insomnia](https://insomnia.rest/)
4. **Visual Studio Code (com extensões)** - Oferece suporte para desenvolvimento de APIs: [VS Code](https://code.visualstudio.com/)
5. **OpenAPI Generator** - Gera SDKs a partir de especificações de APIs: [OpenAPI Generator](https://openapi-generator.tech/)

---

#### **API Runtime Platform (Execução de APIs)**

1. **AWS API Gateway** - Para execução e escalabilidade de APIs: [AWS API Gateway](https://aws.amazon.com/api-gateway/)
2. **Apigee** - Gerenciamento e execução em tempo real: [Apigee](https://cloud.google.com/apigee)
3. **Kong** - Plataforma para execução e monitoramento de APIs: [Kong](https://konghq.com/)
4. **Nginx** - Proxy reverso amplamente usado para APIs: [Nginx](https://www.nginx.com/)
5. **Ocelot** - Gateway leve para APIs baseadas em .NET: [Ocelot](https://ocelot.readthedocs.io/)

---

#### **API Engagement Platform (Engajamento com APIs)**

1. **RapidAPI** - Marketplace para descoberta e integração: [RapidAPI](https://rapidapi.com/)
2. **API Landscape** - Mapeamento de APIs globais: [API Landscape](https://apilandscape.apiscene.io)
3. **ReadMe** - Ferramenta de engajamento e documentação: [ReadMe](https://readme.com/)
4. **Docusaurus** - Criação de portais para desenvolvedores: [Docusaurus](https://docusaurus.io/)
5. **Redocly** - Solução de documentação e portais: [Redocly](https://redoc.ly/)

---

Estas ferramentas abrangem o desenvolvimento, execução e engajamento de APIs, oferecendo soluções robustas para cada etapa do ciclo de vida de uma API.

## Resumo - A Agenda do Arquiteto para APIs

![A agenda do arquiteto para APIs em seis frentes: desenhar, implementar e testar, documentar, definir tecnologias, gerenciar e reutilizar APIs, com etapas conduzidas junto com o time.](https://github.com/user-attachments/assets/cf10adc2-d2a1-4a37-b95f-57d59151afaf)

**Leitura textual da figura:** o infográfico organiza a agenda em seis perguntas. Como identificar, escolher e desenhar APIs: entender requisitos, definir escopo, escolher o estilo arquitetural e criar um protótipo. Como implementar e testar: escolher plataforma, implementar endpoints, testar e iterar. Como documentar e comunicar: gerar documentação, adicionar exemplos e publicar um portal. Como definir tecnologias: avaliar requisitos, escolher linguagens e frameworks e selecionar protocolos. Como gerenciar: publicar, monitorar, versionar e proteger. Como descobrir e reutilizar: mapear catálogos, avaliar compatibilidade e reutilizar com SDKs e conectores. Cada frente lista ferramentas de apoio, e a moldura lembra que arquitetura é sociotécnica: o arquiteto conduz junto com o time e responde pelas consequências das decisões.

### Como identificar, escolher e desenhar APIs?

**Detalhes:**  

O processo de identificar e desenhar uma API começa com o entendimento dos requisitos de negócios e das necessidades dos consumidores da API. As etapas incluem:

1. **Entender os requisitos:** Identifique os dados e funcionalidades que a API deve fornecer. Use técnicas como entrevistas com stakeholders e levantamento de casos de uso.
2. **Definir escopo e objetivo:** Determine o que a API deve resolver e quais consumidores ela atenderá.
3. **Escolher o estilo arquitetural:** Decida entre REST, GraphQL, gRPC, SOAP ou WebSocket com base no contexto do uso.
4. **Criar um protótipo:** Utilize ferramentas como Swagger ou Postman para modelar e simular a API antes de sua implementação.

**Ferramentas de ajuda:**

- Swagger Editor: [https://swagger.io/tools/swagger-editor/](https://swagger.io/tools/swagger-editor/)
- Postman: [https://www.postman.com/](https://www.postman.com/)

---

### Como implementar e testar APIs?

**Detalhes:**  

A implementação de APIs segue a definição do design e seu desenvolvimento em linguagens e frameworks compatíveis. O ciclo de desenvolvimento inclui:

1. **Escolher uma plataforma ou framework:** Frameworks como Express.js (Node.js), Flask (Python) ou Spring Boot (Java) podem ser usados.
2. **Implementar endpoints:** Desenvolva cada endpoint conforme especificado no protótipo da API.
3. **Testar a API:** Realize testes unitários, de integração e de carga usando ferramentas automatizadas.
4. **Iterar e corrigir:** Ajuste o código conforme resultados de testes.

**Ferramentas de ajuda:**

- Postman para testes manuais: [https://www.postman.com/](https://www.postman.com/)
- Newman (CLI para testes com Postman): [https://github.com/postmanlabs/newman](https://github.com/postmanlabs/newman)
- JMeter para testes de carga: [https://jmeter.apache.org/](https://jmeter.apache.org/)

---

### Como documentar e comunicar APIs?

**Detalhes:**  

Uma boa documentação é essencial para que os consumidores possam usar a API de forma eficiente. Os passos incluem:

1. **Gerar documentação automática:** Use ferramentas como Swagger ou API Blueprint para gerar documentação a partir do código.
2. **Adicionar exemplos:** Inclua exemplos de uso de cada endpoint e possíveis respostas.
3. **Publicar a documentação:** Disponibilize um portal para desenvolvedores com acesso à documentação e exemplos.

**Ferramentas de ajuda:**

- SwaggerHub: [https://swagger.io/tools/swaggerhub/](https://swagger.io/tools/swaggerhub/)
- Redocly: [https://redoc.ly/](https://redoc.ly/)
- Docusaurus para criar portais de documentação: [https://docusaurus.io/](https://docusaurus.io/)

---

### Como definir tecnologias de APIs?

**Detalhes:**  

A definição de tecnologias para APIs depende de fatores como desempenho, escalabilidade e interoperabilidade. As etapas incluem:

1. **Avaliar requisitos:** Considere aspectos como latência, segurança e compatibilidade com sistemas existentes.
2. **Escolher linguagens e frameworks:** Para APIs leves e rápidas, escolha Node.js. Para APIs robustas e corporativas, opte por Java ou .NET.
3. **Selecionar protocolos:** REST para simplicidade, gRPC para alto desempenho ou WebSocket para comunicação em tempo real.

**Ferramentas de ajuda:**

- Comparador de frameworks: [https://www.thoughtworks.com/radar/](https://www.thoughtworks.com/radar/)
- Guias sobre WebSocket e gRPC: [https://grpc.io/](https://grpc.io/)
- Referência de RESTful APIs: [https://restfulapi.net/](https://restfulapi.net/)

---

### Como gerenciar APIs?

**Detalhes:**  

Gerenciar APIs inclui publicação, monitoramento, controle de versão e segurança. As etapas incluem:

1. **Publicar APIs:** Use plataformas como AWS API Gateway ou Apigee para hospedar APIs.
2. **Monitorar desempenho:** Utilize ferramentas para rastrear latência, erros e uso.
3. **Controlar versões:** Defina versões claras e mantenha compatibilidade com consumidores.
4. **Proteger APIs:** Implemente autenticação (OAuth, API keys) e crie limites de taxa para evitar abuso.

**Ferramentas de ajuda:**

- AWS API Gateway: [https://aws.amazon.com/api-gateway/](https://aws.amazon.com/api-gateway/)
- Apigee: [https://cloud.google.com/apigee](https://cloud.google.com/apigee)
- Prometheus e Grafana para monitoramento: [https://prometheus.io/](https://prometheus.io/)
- Ocelot para gerenciamento: [https://ocelot.readthedocs.io/](https://ocelot.readthedocs.io/)

---

### Como descobrir e reusar APIs?

**Detalhes:**  

Reutilizar APIs existentes acelera o desenvolvimento e promove padronização. As etapas incluem:

1. **Mapear APIs internas e externas:** Identifique APIs existentes em catálogos internos ou em marketplaces como API Landscape.
2. **Avaliar compatibilidade:** Certifique-se de que a API atende às necessidades do projeto.
3. **Reutilizar APIs:** Use SDKs ou ferramentas para integração fácil.

**Ferramentas de ajuda:**

- API Landscape: [https://apilandscape.apiscene.io](https://apilandscape.apiscene.io)
- RapidAPI: [https://rapidapi.com/](https://rapidapi.com/)
- Postman para exploração de APIs: [https://www.postman.com/explore](https://www.postman.com/explore)

##
