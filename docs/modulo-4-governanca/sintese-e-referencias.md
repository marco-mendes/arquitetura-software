# Síntese e referências

Governança de serviços torna decisões arquiteturais explícitas, aplicáveis e revisáveis. Ela começa antes da execução com catálogo, ownership, contrato, versão e decisão registrada. Continua durante a execução com política de borda, logs, métricas, traces e SLO. O ciclo se fecha quando a evidência pode provocar revisão: configuração sem teste pode divergir; dashboard sem dono pode ser ignorado; regra de domínio escondida no gateway perde o contexto que a justifica.

## Heurísticas para decisão

Comece pelo recurso e pelo consumidor. Pergunte quem é dono do contrato, do dado, do risco e do SLO. Determine se a regra é comum de borda ou se depende de estado e linguagem do domínio. Roteamento, correlação, proteção de volume e telemetria normalmente pertencem ao gateway. Validação semântica, autorização contextual, invariantes e transições de estado pertencem ao serviço. Segurança pode cruzar ambos: borda autentica tecnicamente; domínio autoriza ação concreta.

Faça a política pequena e verificável. “Proteger contra pico” é intenção; “limitar três chamadas por segundo por origem, responder 429, medir recusas e revisar quando consumidores legítimos forem afetados” é hipótese operável. Declare chave, janela, consequência e responsável. Limite local é suficiente para experimento de uma instância, mas não é limite global por acidente. Alterar esse fato não é falha: é reconhecer o escopo da evidência.

Trate sinais como instrumentos distintos. Logs descrevem evento e devem usar campos seguros, sem prontuários, tokens ou corpos integrais. Métricas mostram taxa, distribuição e tendência; rótulos precisam ser estáveis. Traces mostram caminho causal e tempo entre componentes. Correlation ID une a busca humana; traceparent preserva árvore técnica. SLO dá sentido à observabilidade ao declarar o resultado que importa ao consumidor e a reação quando orçamento de erro se esgota.

## Checklist de revisão

Antes de publicar rota, confirme:

- catálogo com owner, consumidores, contrato, dado e dependências;
- estratégia de versão e retirada compatível;
- política de borda declarada, revisada e com condição de mudança;
- regra de domínio testada no serviço, sem ser copiada para proxy;
- correlação, logs seguros, métricas e traces com propósito definido;
- SLO com indicador, janela, dono e comportamento de revisão;
- teste automatizado para comportamento prometido;
- limpeza de ambiente local e ausência de estado manual.

O laboratório usa Kong DB-less e arquivos montados somente para leitura. Compose fixa versões de imagem, mantém banco fora da rede de Kong e expõe portas de estudo. O teste envia correlation ID, excede limite e consulta API de traces do Jaeger. Essas escolhas não representam plataforma completa: produção pede identidade, segredos, retenção, tolerância a falhas, capacidade, auditoria e controles adequados ao risco.

## Próximo passo

No módulo seguinte, eventos introduzirão novas decisões de governança: schema de evento, idempotência, ownership de tópico, retenção e rastreabilidade assíncrona. A pergunta permanece: que política é verificável, quem a possui e qual evidência demonstrará que continua verdadeira depois de mudar o sistema?

## Referências públicas

- [Kong Gateway: declarative configuration](https://docs.konghq.com/gateway/latest/production/deployment-topologies/db-less-and-declarative-config/)
- [Kong Gateway: correlation ID plugin](https://docs.konghq.com/hub/kong-inc/correlation-id/)
- [Kong Gateway: rate limiting plugin](https://docs.konghq.com/hub/kong-inc/rate-limiting/)
- [Kong Gateway: OpenTelemetry plugin](https://docs.konghq.com/hub/kong-inc/opentelemetry/)
- [OpenTelemetry: documentação e especificação](https://opentelemetry.io/docs/)
- [OpenTelemetry Collector: configuração](https://opentelemetry.io/docs/collector/configuration/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [Jaeger: documentação e API de consulta](https://www.jaegertracing.io/docs/)
- [Google SRE Book: service level objectives](https://sre.google/sre-book/service-level-objectives/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

## Equivalências em Java e .NET

Java pode combinar Spring Boot Actuator, Micrometer e OpenTelemetry Java para produzir sinais, mantendo gateway declarativo ou Spring Cloud Gateway como borda. .NET pode combinar ASP.NET Core, ActivitySource, OpenTelemetry .NET e YARP. As bibliotecas não são a política: owner, versão, controle de domínio, evidência e revisão devem sobreviver à troca de linguagem ou proxy.
