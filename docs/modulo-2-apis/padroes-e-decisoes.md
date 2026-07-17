# Padrões e decisões para APIs

## Começar pelos consumidores e pelas forças

Uma agenda de arquitetura para APIs começa antes do desenho de endpoints. Identifique consumidores, tarefas, frequência, volume, latência tolerada, falhas esperadas, propriedade dos dados e ritmo de evolução. Uma interface administrativa usada por um navegador controlado pela mesma equipe enfrenta forças diferentes de um contrato consumido por vinte parceiros externos.

Três perguntas evitam decisões prematuras:

1. Qual resultado o consumidor precisa observar?
2. O consumidor precisa da resposta agora, pode acompanhar um protocolo ou pode receber uma notificação depois?
3. Que mudança do provedor não deveria obrigar o consumidor a mudar?

No laboratório, a plataforma não promete a decisão final da operadora no `POST`. Ela promete aceitar um pedido válido e fornecer um protocolo. `202` e `Location` tornam essa fronteira temporal explícita. Se a resposta externa puder levar segundos ou minutos, manter uma conexão aberta pode acoplar disponibilidade e tempo de resposta dos dois lados.

## Escolher estilo por interação

Uma arquitetura pode usar mais de um estilo sem virar uma coleção arbitrária. O critério deve ser explícito. Para leitura e manipulação de recursos por consumidores web diversos, REST/HTTP é uma opção forte. Para comandos internos tipados e de baixa latência, gRPC pode reduzir ambiguidade e gerar clientes. Para uma interface que compõe grafos de dados com campos variáveis, GraphQL pode reduzir múltiplas chamadas. Para uma operação de negócio naturalmente verbal, RPC pode ser mais honesto que inventar um recurso artificial.

Compare alternativas pelas mesmas dimensões:

| Dimensão | REST/HTTP | RPC | GraphQL | gRPC |
| --- | --- | --- | --- | --- |
| Unidade principal | recurso e representação | operação | tipo e seleção | serviço e mensagem |
| Descoberta | OpenAPI e documentação | descrição de métodos | introspecção e schema | arquivos `.proto` |
| Evolução | compatibilidade de recursos e schemas | compatibilidade de argumentos | depreciação de campos | regras de evolução do protobuf |
| Cache web | aproveita semântica HTTP | depende da convenção | exige estratégia própria | fora do modelo usual de cache web |
| Consumidores | amplo suporte HTTP | simples quando convenção é clara | clientes capazes de formular consultas | geração de código e suporte HTTP/2 |
| Risco típico | REST apenas nominal | proliferação de métodos | consultas caras e autorização granular | acoplamento a toolchain e operação |

A tabela orienta perguntas, não produz escolha automática. Uma API REST mal modelada pode ser pior que um RPC explícito. Um serviço gRPC interno pode coexistir com uma API REST externa. A fronteira e os consumidores determinam onde cada decisão se aplica.

## Contract-first e code-first

Em **contract-first**, a equipe modela e revisa OpenAPI antes da implementação. Isso antecipa feedback de consumidores, permite mocks e expõe incompatibilidades sem código de produção. O risco é manter um documento idealizado que se afasta da execução.

Em **code-first**, tipos e rotas geram o contrato. FastAPI faz isso naturalmente. O ciclo é rápido e a documentação acompanha boa parte do código, mas detalhes do framework podem virar decisões públicas sem revisão consciente.

O laboratório combina os dois: `openapi.yaml` preserva a intenção explícita; `app.openapi()` representa o que FastAPI gera; testes comparam operações, schemas obrigatórios e exemplos. A duplicação é deliberada para ensino. Em uma equipe, escolha uma fonte principal e automatize a detecção de deriva. Evite editar dois contratos manualmente sem uma verificação de concordância.

## Evolução compatível

Compatibilidade não é apenas validar JSON. Adicionar `prazo_estimado` opcional tende a ser compatível; reaproveitar `situacao: recebida` para significar “aprovada” preserva a forma e quebra a semântica.

Classifique a mudança como aditiva, restritiva, semântica ou remoção; identifique consumidores; preserve comportamento antigo na transição; publique depreciação e alternativa; observe adoção; remova apenas depois do critério acordado.

Versionar no caminho, como `/v2/elegibilidades`, deixa a linha visível e facilita roteamento, mas pode sugerir que toda a API muda em bloco. Versionar por cabeçalho mantém URIs estáveis, porém é menos óbvio para pessoas e algumas ferramentas. Versionar por mídia pode ser preciso e também mais complexo. Registre a escolha e não misture estratégias sem motivo.

## Idempotência como política

`GET`, `PUT` e `DELETE` têm semântica idempotente no protocolo, mas uma implementação ainda pode violá-la. Um `GET` que confirma definitivamente uma solicitação está usando o método de forma perigosa. Um `PUT` que soma um valor a cada tentativa também contradiz a intenção de substituição.

Para `POST`, uma chave pode associar consumidor, operação e conteúdo ao resultado. Repetição equivalente recebe o mesmo protocolo; corpo diferente, conflito. A política define retenção e concorrência. A API mínima não a implementa para não apresentar um dicionário local como solução distribuída confiável.

## Paginação e consistência de leitura

Paginação exige uma ordenação estável. `?offset=20&limit=10` sem ordenação definida não produz páginas reproduzíveis. Mesmo com ordenação, inserções antes do deslocamento movem itens. Um cursor pode incorporar a última chave observada e a ordenação; deve ser opaco para permitir evolução interna.

O contrato define limite padrão e máximo, continuação, cursor inválido, filtros e se a leitura é instantâneo ou coleção viva. A API mínima não lista elegibilidades, portanto não inventa paginação.

## API gateway: entrada central, não centro do domínio

Um **API gateway** é um intermediário que recebe chamadas, aplica políticas e encaminha para provedores. Pode centralizar roteamento, terminação TLS, limites de uso, autenticação técnica, correlação e observabilidade. Também pode adaptar detalhes de protocolo em fronteiras controladas.

O gateway não deve decidir regras centrais do domínio nem virar um novo monólito de transformações. Centralizar toda tradução ali aumenta acoplamento e dificulta testes. Diferenças semânticas entre a linguagem da plataforma e a operadora pedem um adaptador ou camada anticorrupção próximo à integração. O gateway pode encaminhar para esse adaptador, mas roteamento não resolve significado.

Introduzir gateway traz salto de rede, configuração, operação e risco de concentração. Em uma aplicação local com duas rotas, ele seria excesso. No módulo 4, políticas e operação justificarão uma avaliação mais concreta. Por enquanto, registre a decisão pendente e não instale infraestrutura sem força correspondente.

## Erros e observabilidade sem vazamento

Um mapa de erros deve separar falha do consumidor, ausência de recurso, conflito de estado, indisponibilidade externa e defeito interno. Códigos públicos são estáveis e poucos; logs internos podem guardar diagnóstico técnico. Não devolva stack trace, consulta interna ou segredo na resposta.

Um identificador de correlação ajuda a seguir a interação por gateway, API e adaptador. Ele não substitui protocolo de negócio: `protocolo` permite ao consumidor consultar a elegibilidade; correlação ajuda a operação a investigar uma execução. Misturar os dois expõe decisões operacionais e dificulta retenções diferentes.

## ADR-002: o que registrar

O registro contém contexto, forças, alternativas, decisão, consequências, evidência e revisão. “Escolhemos FastAPI porque é rápido” mistura tecnologia e afirmação não medida. Delimite REST/HTTP, aceitação com `202`, OpenAPI, compatibilidade e testes; framework permanece mecanismo substituível.

Gatilhos possíveis incluem novo consumidor com suporte restrito, necessidade de streaming, volume que exige paginação, operação que precisa de idempotência forte ou custo de manter duas versões. Um ADR é uma prática de documentação de decisões; não é uma garantia de que a decisão permanecerá correta.
