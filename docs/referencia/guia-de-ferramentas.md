# Guia de ferramentas

As oficinas essenciais usam ferramentas executáveis localmente e com licença aberta. Cada ferramenta é introduzida pela finalidade didática e pela evidência que permite observar.

| Ferramenta | Finalidade | Licença aberta | Módulo | Instalação de referência | Equivalentes ou complementos |
| --- | --- | --- | --- | --- | --- |
| Python e pytest | Executar exemplos e testes automatizados | PSF e MIT | 1–6 | Distribuição Python e ambiente virtual | JUnit em Java; xUnit em .NET |
| Mermaid | Descrever diagramas como texto versionável | MIT | 1–6 | Renderização integrada ao site | PlantUML; diagramas C4 |
| Structurizr Lite | Explorar modelos C4 executáveis localmente | Apache 2.0 | 1 | Contêiner local | PlantUML com C4-PlantUML |
| FastAPI | Implementar a API de referência em Python | MIT | 2–4 | Pacote no ambiente virtual | Spring Boot; ASP.NET Core |
| OpenAPI | Descrever contratos HTTP de forma portável | Apache 2.0 | 2–4 | Gerado pela aplicação e validado localmente | Springdoc; Swashbuckle |
| Bruno | Executar coleções de chamadas versionáveis | MIT | 2 | Aplicativo para o sistema operacional | `curl`; REST Client |
| Spectral | Verificar regras em contratos OpenAPI | Apache 2.0 | 2 | Pacote de linha de comando | Validadores integrados ao build |
| Docker e Docker Compose | Reproduzir serviços e dependências locais | Apache 2.0 | 3–6 | Docker Engine ou ambiente compatível | Podman e Podman Compose |
| PostgreSQL | Observar decisões de persistência e isolamento | PostgreSQL License | 3 | Contêiner da oficina | SQL Server; MariaDB |
| Kong Gateway | Aplicar roteamento e políticas declarativas | Apache 2.0 | 4 | Contêiner local | Apache APISIX; YARP em .NET |
| OpenTelemetry | Produzir telemetria portável | Apache 2.0 | 4–6 | SDK e Collector locais | Micrometer; .NET Diagnostics |
| Jaeger | Consultar rastros distribuídos | Apache 2.0 | 4 | Contêiner local | Grafana Tempo; Zipkin |
| RabbitMQ | Exercitar filas, confirmação e repetição | MPL 2.0 | 5 | Contêiner local | ActiveMQ Artemis; MassTransit |
| Kafka | Comparar log distribuído e consumo por deslocamento | Apache 2.0 | 5 | Extensão opcional em contêiner | Redpanda; bibliotecas Kafka para JVM e .NET |
| kind e Kubernetes | Implantar, observar e recuperar cargas orquestradas | Apache 2.0 | 6 | Cluster local criado por linha de comando | minikube; k3d |

## Instalação responsável

Cada oficina apresenta comandos separados para Windows, macOS e Linux, uma verificação da instalação e uma contingência. Prefira as versões registradas no repositório da disciplina para que a evidência seja reproduzível.
