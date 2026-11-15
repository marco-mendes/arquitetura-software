# Padrões e decisões para APIs

## Tipos de APIs

![Quadro dos tipos de APIs conforme o contexto de solução com as categorias web, mobile e cloud e as categorias integração, omnichannel e IoT. Cada categoria traz um exemplo real com seus protocolos de transporte e formatos de dados.](https://github.com/user-attachments/assets/8d90f8d0-aafd-41c4-9c82-0252819ce133)

**Leitura textual da figura:** o quadro compara seis contextos de uso de APIs. As APIs web alimentam sites e aplicações dinâmicas com HTTP/HTTPS e com os formatos JSON, XML ou HTML, como a busca de produtos da Amazon. As APIs mobile priorizam dados leves e experiência otimizada com HTTPS e HTTP/2, além de gRPC e WebSocket, como nos casos da Uber e do Instagram. As APIs cloud expõem plataformas SaaS para automação e integração entre nuvens, como o Dropbox. As APIs de integração conectam empresas e parceiros por contratos rígidos sobre HTTPS, gRPC e SOAP ou sobre JMS e AMQP, como o SAP e as APIs de governo. As APIs omnichannel garantem experiência consistente entre canais e dispositivos, como a Shopify. As APIs de IoT coletam dados e enviam comandos com MQTT e CoAP ou com HTTPS e AMQP, como o Google Nest. Uma legenda no rodapé do quadro resume os protocolos e formatos citados nas seis categorias.

---

### API para Soluções Web

Aplicativos web exibem páginas criadas dinamicamente a partir das solicitações dos usuários e dos dados disponíveis no *back-end*. As APIs fornecem esses dados ao aplicativo web, que extrai os dados brutos, processa o conteúdo e o exibe em páginas HTML.

Um aplicativo web de comércio eletrônico, por exemplo, exibe produtos com base nos critérios de pesquisa do cliente. A API de produtos busca os dados num banco de dados e retorna os campos relevantes numa estrutura JSON, que o aplicativo web interpreta e transforma em página HTML.

**Exemplo Real:**

- **API de Busca de Produtos da Amazon:** permite que desenvolvedores integrem funções de busca e apresentação de produtos em aplicativos próprios, como sistemas de afiliados.
- **Protocolos de Transporte e Dados:** HTTP/HTTPS para transporte e formatos como JSON ou XML para dados.

---

### API para Soluções Móveis

O número de dispositivos móveis e *tablets* superou o número de computadores. Os aplicativos para celular diferem dos aplicativos de *desktop* tradicionais porque a maioria deles não é autônoma nem autossuficiente.

Os aplicativos móveis precisam se conectar a servidores na internet para funcionar ou, pelo menos, para oferecer a totalidade de suas funções.

Os dados entregues pelas APIs a esses aplicativos precisam ser leves e particionados. Essa característica permite o consumo da API por dispositivos com capacidade de processamento limitada e com largura de banda restrita na conexão à internet.

**Exemplo Real:**

- **API da Uber:** fornece acesso a motoristas e passageiros. A API começou com o protocolo HTTP e o formato JSON e, com o crescimento da Uber, foi modificada para protocolos de alta escalabilidade como o gRPC e o ProtoBuffer.
- **API do Instagram:** fornece acesso a dados como *posts*, comentários e publicações recentes e permite a criação de experiências otimizadas para dispositivos móveis.
- **GraphQL no Spotify:** permite que aplicativos móveis busquem numa única consulta exatamente os dados de álbuns, artistas e *playlists* de que precisam, o que otimiza a experiência do usuário.
- **Protocolos de Transporte e Dados:** HTTP/HTTPS com JSON para APIs REST e consultas estruturadas no caso de GraphQL.

---

### APIs para Soluções de Nuvens

As soluções SaaS em nuvem normalmente consistem num aplicativo web visível para os consumidores e em APIs que operam por trás desse aplicativo.

As soluções em nuvem geralmente oferecem também uma API que permanece oculta ao usuário final. Essa API conecta o aplicativo de nuvem a outros aplicativos de nuvem para fins de automação ou conecta a solução a aplicativos móveis e a *software* de *desktop*.

**Exemplo Real:**

- **API do Dropbox:** permite a sincronização de arquivos com aplicativos de terceiros, como Google Workspace e Microsoft Office.
- **Protocolos de Transporte e Dados:** HTTPS para transporte seguro e dados geralmente enviados em JSON pela simplicidade do formato.

---

### APIs para Soluções de Integração

As APIs fornecem os recursos essenciais para conectar, estender e integrar *software*. Na integração de *software*, as APIs conectam uma empresa a outras empresas e sustentam soluções de integração de negócios entre organizações.

O negócio de uma empresa pode ser expandido pela conexão com fornecedores e clientes ao longo da cadeia de valor.

Como a TI executa os processos de negócio, a integração dos sistemas de TI de uma empresa aos sistemas de parceiros, de funcionários e de clientes vincula os negócios ao longo de toda a cadeia de valor.

**Exemplo Real:**

- **gRPC no Uber:** usado na comunicação de alto desempenho entre microsserviços e sistemas internos de integração, com baixa latência e maior eficiência.
- **API do SAP:** integra ERPs corporativos a outros sistemas de TI e permite transações entre parceiros de negócios, como fornecedores e clientes.
- **API do Governo Brasileiro (NF-e, e-Social, TISS):** faz uso extensivo de XML como formato de dados devido aos mecanismos da pilha XML para validação de dados e segurança da informação.
- **Protocolos de Transporte e Dados:** gRPC com Protocol Buffers para comunicações de alta eficiência e SOAP ou REST para integrações mais tradicionais.

---

### APIs para Soluções Multicanal

As APIs multicanal conectam sistemas diferentes entre organizações ou dentro de cadeias de valor e possibilitam a automação de processos e a troca de dados.

Para melhorar a experiência de compra, os mesmos dados e ações do usuário precisam estar disponíveis em cada dispositivo que ele usa. Essa exigência vale mesmo quando os dispositivos têm *hardware* diferente e executam sistemas operacionais e aplicativos diferentes.

As soluções omnicanal ou multicanal atendem a essa exigência. Os clientes obtêm uma experiência consistente em qualquer canal ou dispositivo e alternam entre os dispositivos sem perder o estado da interação.

**Exemplo Real:**

- **API da Shopify:** permite a integração de lojas virtuais para oferecer experiências consistentes em dispositivos móveis, *desktops* e quiosques.
- **Protocolos de Transporte e Dados:** HTTP/HTTPS para transporte e JSON para dados, com WebSockets para atualizações em tempo real.

---

### APIs para Soluções IoT

A internet das coisas é composta de dispositivos físicos conectados à internet. O *software* controla esses dispositivos por meio de seus atuadores e os dispositivos coletam dados por meio de seus sensores. O dispositivo em si não precisa ter capacidade de processamento sofisticada para se comportar como um dispositivo inteligente.

O dispositivo se conecta a funções inteligentes expostas na internet por meio de APIs.

Exemplos dessas soluções incluem dispositivos vestíveis, carros, casas e cidades inteligentes.

**Exemplo Real:**

- **API do Google Nest:** gerencia remotamente dispositivos inteligentes como termostatos e câmeras de segurança.
- **Protocolos de Transporte e Dados:** MQTT, protocolo leve para dispositivos IoT, ou HTTP/HTTPS para transporte e dados em JSON ou em Protocol Buffers para comunicações otimizadas.

## Como pensar em APIs a partir da lente de uma plataforma

![Arquitetura de referência moderna com firewall, gateway de API e servidor web, além de fila de mensagens e sistemas legados com banco de dados. Ao lado aparece a visão de plataforma de APIs com desenvolvimento, execução e engajamento.](https://github.com/user-attachments/assets/1cad9c6b-da09-4bf6-91e4-0620428e4809)

**Leitura textual da figura:** à esquerda, usuários web e mobile acessam o sistema principal por um *firewall* que encaminha as requisições ao *gateway* de API. O *gateway* roteia as requisições para o servidor web com a lógica de negócios, publica mensagens na fila e consulta e atualiza dois sistemas legados. O servidor web grava os dados de negócio no banco de dados da arquitetura de referência.

À direita, a plataforma de APIs tem três camadas encadeadas, da mais próxima do desenvolvedor para a mais próxima do consumidor. A plataforma de desenvolvimento reúne IDE e extensões, *templates* e *mock servers*, testes locais e governança e implanta as APIs na plataforma de execução. A plataforma de execução reúne *gateway*, roteamento e transformação e também cuida da segurança com OAuth, do *rate limiting* e da observabilidade. Essa camada publica as APIs na plataforma de engajamento. A plataforma de engajamento oferece portal do desenvolvedor, documentação e SDKs e catálogo de APIs. Ela também oferece planos e assinaturas, *analytics* e *feedback*. Na base da figura, as preocupações de segurança e escalabilidade atravessam o conjunto das três camadas. A observabilidade, a padronização e a experiência do desenvolvedor também se aplicam às três camadas.

### Ferramentas para Cada Parte da Plataforma de APIs

#### **API Development Platform (Desenvolvimento de APIs)**

1. **Swagger Editor** - Ferramenta para criar especificações de APIs: [Swagger Editor](https://swagger.io/tools/swagger-editor/)
2. **Postman** - Ideal para desenvolvimento e simulação de APIs: [Postman](https://www.postman.com/)
3. **Insomnia** - Cliente HTTP para testar e organizar APIs: [Insomnia](https://insomnia.rest/)
4. **Visual Studio Code com extensões** - Oferece suporte para desenvolvimento de APIs: [VS Code](https://code.visualstudio.com/)
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

## Resumo - A Agenda do Arquiteto para APIs

![Agenda do arquiteto para APIs em seis frentes. As frentes são o desenho, a implementação com teste e a documentação de APIs, além da definição de tecnologias e da gestão e reutilização de APIs. As etapas são conduzidas junto com o time.](https://github.com/user-attachments/assets/cf10adc2-d2a1-4a37-b95f-57d59151afaf)

**Leitura textual da figura:** o infográfico organiza a agenda do arquiteto em seis perguntas, cada uma com suas etapas.

- Identificar, escolher e desenhar APIs envolve entender requisitos e definir escopo, escolher o estilo arquitetural e criar um protótipo.
- Implementar e testar envolve escolher a plataforma, implementar *endpoints*, testar e iterar.
- Documentar e comunicar envolve gerar documentação, adicionar exemplos e publicar um portal.
- Definir tecnologias envolve avaliar requisitos, escolher linguagens e *frameworks* e selecionar protocolos.
- Gerenciar envolve publicar, monitorar, versionar e proteger as APIs.
- Descobrir e reutilizar envolve mapear catálogos, avaliar compatibilidade e reutilizar com SDKs e conectores.

Cada frente lista ferramentas de apoio. A moldura da figura registra que a arquitetura é sociotécnica, de modo que o arquiteto conduz as etapas junto com o time e responde pelas consequências das decisões.

### Como identificar, escolher e desenhar APIs?

**Detalhes:**  

O processo de identificar e desenhar uma API começa com o entendimento dos requisitos de negócio e das necessidades dos consumidores da API. As etapas incluem:

1. **Entender os requisitos:** Identifique os dados e funcionalidades que a API deve fornecer. Use técnicas como entrevistas com *stakeholders* e levantamento de casos de uso.
2. **Definir escopo e objetivo:** Determine o que a API deve resolver e quais consumidores ela atenderá.
3. **Escolher o estilo arquitetural:** Decida entre REST, GraphQL e gRPC ou entre SOAP e WebSocket com base no contexto do uso.
4. **Criar um protótipo:** Utilize ferramentas como Swagger ou Postman para modelar e simular a API antes de sua implementação.

**Ferramentas de ajuda:**

- Swagger Editor: [https://swagger.io/tools/swagger-editor/](https://swagger.io/tools/swagger-editor/)
- Postman: [https://www.postman.com/](https://www.postman.com/)

---

### Como implementar e testar APIs?

**Detalhes:**  

A implementação de APIs segue a definição do desenho e ocorre em linguagens e *frameworks* compatíveis. O ciclo de desenvolvimento inclui:

1. **Escolher uma plataforma ou framework:** Frameworks como Express.js (Node.js), Flask (Python) ou Spring Boot (Java) podem ser usados.
2. **Implementar endpoints:** Desenvolva cada *endpoint* conforme especificado no protótipo da API.
3. **Testar a API:** Realize testes unitários, de integração e de carga usando ferramentas automatizadas.
4. **Iterar e corrigir:** Ajuste o código conforme os resultados dos testes.

**Ferramentas de ajuda:**

- Postman para testes manuais: [https://www.postman.com/](https://www.postman.com/)
- Newman, CLI para testes com Postman: [https://github.com/postmanlabs/newman](https://github.com/postmanlabs/newman)
- JMeter para testes de carga: [https://jmeter.apache.org/](https://jmeter.apache.org/)

---

### Como documentar e comunicar APIs?

**Detalhes:**  

Uma documentação completa permite que os consumidores usem a API de forma eficiente. Os passos incluem:

1. **Gerar documentação automática:** Use ferramentas como Swagger ou API Blueprint para gerar documentação a partir do código.
2. **Adicionar exemplos:** Inclua exemplos de uso de cada *endpoint* e as respostas possíveis.
3. **Publicar a documentação:** Disponibilize um portal para desenvolvedores com acesso à documentação e aos exemplos.

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

O gerenciamento de APIs inclui publicação, monitoramento, controle de versão e segurança. As etapas incluem:

1. **Publicar APIs:** Use plataformas como AWS API Gateway ou Apigee para hospedar APIs.
2. **Monitorar desempenho:** Utilize ferramentas para rastrear latência, erros e uso.
3. **Controlar versões:** Defina versões claras e mantenha compatibilidade com consumidores.
4. **Proteger APIs:** Implemente autenticação com OAuth ou com chaves de API e crie limites de taxa para evitar abuso.

**Ferramentas de ajuda:**

- AWS API Gateway: [https://aws.amazon.com/api-gateway/](https://aws.amazon.com/api-gateway/)
- Apigee: [https://cloud.google.com/apigee](https://cloud.google.com/apigee)
- Prometheus e Grafana para monitoramento: [https://prometheus.io/](https://prometheus.io/)
- Ocelot para gerenciamento: [https://ocelot.readthedocs.io/](https://ocelot.readthedocs.io/)

---

### Como descobrir e reusar APIs?

**Detalhes:**  

A reutilização de APIs existentes acelera o desenvolvimento e promove padronização. As etapas incluem:

1. **Mapear APIs internas e externas:** Identifique APIs existentes em catálogos internos ou em *marketplaces* como API Landscape.
2. **Avaliar compatibilidade:** Certifique-se de que a API atende às necessidades do projeto.
3. **Reutilizar APIs:** Use SDKs ou ferramentas de integração.

**Ferramentas de ajuda:**

- API Landscape: [https://apilandscape.apiscene.io](https://apilandscape.apiscene.io)
- RapidAPI: [https://rapidapi.com/](https://rapidapi.com/)
- Postman para exploração de APIs: [https://www.postman.com/explore](https://www.postman.com/explore)

##
