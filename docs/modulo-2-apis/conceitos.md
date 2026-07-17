# Conceitos fundamentais de APIs

## Interface, contrato e implementação

Uma **interface de programação de aplicações**, ou API, é uma fronteira pela qual um software oferece capacidades a outros softwares. A interface descreve o que pode ser pedido e observado. O **contrato** torna essa descrição precisa: operações, dados, regras, respostas, erros e expectativas relevantes. A **implementação** é o código que cumpre o contrato. Consumidores deveriam depender do contrato, não da organização interna do provedor.

A equipe pode trocar algoritmo, biblioteca ou armazenamento sem coordenar consumidores se preservar promessas observáveis. Renomear campo obrigatório ou mudar o significado de um código, porém, atravessa a fronteira. FastAPI, Spring Boot e ASP.NET Core implementam e documentam APIs; ainda cabe à arquitetura decidir significado, compatibilidade e limites.

## HTTP como protocolo de aplicação

HTTP define semântica para mensagens de requisição e resposta. Uma requisição combina método, alvo, cabeçalhos e, quando aplicável, conteúdo. Uma resposta combina status, cabeçalhos e conteúdo. Tratar HTTP apenas como transporte para “chamar funções remotas” desperdiça vocabulário que clientes, proxies, caches e ferramentas já compreendem.

Considere `POST /elegibilidades`. O método `POST` comunica que o cliente envia uma representação para que o recurso de destino a processe segundo sua própria semântica. A resposta `202 Accepted` informa que o pedido foi aceito, mas não afirma conclusão do processamento. O cabeçalho `Location: /elegibilidades/{protocolo}` indica onde o cliente pode observar o recurso criado para acompanhamento. Cada parte tem significado próprio.

Os métodos mais frequentes são:

| Método | Intenção comum | Propriedade relevante |
| --- | --- | --- |
| `GET` | recuperar uma representação | seguro e idempotente |
| `POST` | submeter dados ou criar sob uma coleção | não é idempotente por definição |
| `PUT` | substituir o estado conhecido de um recurso | idempotente |
| `PATCH` | aplicar uma alteração parcial | depende do formato da alteração |
| `DELETE` | remover a associação do recurso | idempotente na intenção |

**Seguro** significa que o cliente não pede mudança de estado; efeitos como log e métricas ainda podem ocorrer. **Idempotente** significa que repetir a mesma intenção produz o mesmo efeito pretendido no servidor, embora respostas ou metadados possam variar. Idempotência não significa “a resposta é sempre idêntica” e não equivale a deduplicação automática.

## Recurso, identificador e representação

Em REST, um **recurso** é algo que pode ser identificado e manipulado por representações. A URI identifica; o JSON é uma representação em um instante. O recurso “elegibilidade aceita” não é o dicionário Python guardado em memória. Esse dicionário é uma escolha interna. Amanhã o mesmo recurso poderia vir de um banco ou de outro serviço sem mudar o identificador público.

Nomes de recurso tendem a expressar substantivos do vocabulário do consumidor: `/elegibilidades`, `/agendamentos`, `/autorizacoes`. Verbos continuam existindo nos métodos e nas transições de estado. Rotas como `/criarElegibilidadeAgora` podem ser adequadas em um estilo RPC, mas misturam duas convenções se o restante da API pretende explorar semântica de recursos.

Uma representação deve incluir dados suficientes para a tarefa do consumidor, não uma cópia automática das tabelas internas. Expor colunas e chaves técnicas cria acoplamento ao armazenamento. O contrato do laboratório retorna `protocolo`, `situacao` e `criado_em`; ele não revela a estrutura do dicionário nem o nome de uma classe interna.

## Status e erros

Famílias de status orientam a primeira leitura: `2xx` indica que a requisição foi recebida e tratada com sucesso segundo a semântica específica; `4xx` aponta um problema atribuível à requisição ou ao estado conhecido do cliente; `5xx` indica que o servidor falhou ao cumprir uma requisição aparentemente válida.

Escolha o código mais específico que o consumidor usa com consistência. `200` serve a uma leitura concluída; `201` comunica criação; `202`, aceitação ainda não concluída; `204`, sucesso sem corpo. Entre erros, `400` é amplo, `404` indica recurso não encontrado, `409` expressa conflito e `422` sinaliza conteúdo que viola o contrato.

Um erro de API é parte do contrato. Texto livre obriga cada consumidor a interpretar frases. O schema `ErroAPI` separa `codigo` estável, `mensagem` legível e `detalhes` por campo. O consumidor pode reagir a `dados_invalidos` sem depender da tradução da mensagem. O provedor pode melhorar a explicação sem quebrar essa automação.

## Cabeçalhos e metadados

Cabeçalhos transportam metadados da interação. `Content-Type` descreve a representação enviada; `Accept` expressa formatos aceitos; `Location` aponta outro recurso; `ETag` identifica uma versão da representação e pode apoiar concorrência ou cache; um identificador de correlação conecta registros entre componentes.

Dados do recurso pertencem normalmente à representação; transporte, negociação, cache, condição ou rastreamento são candidatos a cabeçalho. Considere visibilidade em ferramentas e comportamento de intermediários.

## OpenAPI e contrato verificável

OpenAPI é uma especificação para descrever APIs HTTP. Paths, operações, parâmetros, corpos, respostas e schemas podem ser escritos em YAML ou JSON. Ferramentas usam essa descrição para documentação, clientes, mocks, testes e análise estática. No laboratório, `contratos/openapi.yaml` é um contrato explícito versionado.

Um arquivo válido sintaticamente ainda pode ser pobre. `type: string` não explica significado; ausência de erro documentado não elimina o erro real; um exemplo incompatível engana o leitor. Spectral aplica regras automáticas ao documento. Bruno importa o contrato e permite executá-lo como consumidor. `TestClient` chama a aplicação FastAPI sem iniciar uma porta de rede. São três perspectivas complementares: forma, uso e comportamento.

## Paginação, idempotência e evolução

Coleções crescem. Retornar todos os registros funciona em uma demonstração e falha quando volume, latência e memória aumentam. **Paginação** limita cada resposta e fornece uma forma de continuar. Paginação por deslocamento (`offset` e `limit`) é simples, mas pode repetir ou omitir itens quando a coleção muda entre chamadas. Paginação por cursor usa uma posição opaca e tende a lidar melhor com mudanças, ao custo de maior complexidade e menor liberdade de salto.

Pedidos repetidos também acontecem: o usuário tenta novamente, um proxy repete ou a conexão cai após o servidor agir. Para uma operação naturalmente não idempotente, uma chave de idempotência pode associar tentativas equivalentes ao mesmo resultado durante uma janela definida. O contrato deve dizer escopo, duração, comparação de conteúdo e resposta para reutilização divergente. Apenas aceitar um cabeçalho chamado `Idempotency-Key` sem política explícita não resolve o problema.

**Versionamento** identifica uma linha de evolução quando mudanças incompatíveis são inevitáveis. A versão pode aparecer no caminho, em cabeçalho ou em negociação de mídia. Nenhuma localização elimina o custo de manter consumidores. Antes de criar uma nova versão, prefira evolução compatível: acrescentar campo opcional, aceitar valor antigo, preservar significado e observar uso. Remover campo, torná-lo obrigatório, restringir valores ou alterar unidade costuma ser incompatível.

O consumidor antigo precisa ler respostas novas, e o servidor novo precisa compreender requisições antigas dentro do compromisso. Além de testes, mantenha inventário de consumidores, transição e telemetria de uso.

## Restrições REST de Fielding

REST é um estilo definido por um conjunto de restrições, não um sinônimo de JSON sobre HTTP. **Cliente-servidor** separa responsabilidades de interface e dados. **Sem estado (stateless)** exige que cada requisição leve o contexto necessário; o servidor pode preservar recursos, mas não depende de uma sessão conversacional oculta. **Cache** permite marcar respostas reutilizáveis ou não reutilizáveis para reduzir interações.

A **interface uniforme** inclui quatro partes. A identificação de recursos usa identificadores estáveis; a manipulação acontece por representações, sem expor a estrutura interna; mensagens autodescritivas carregam semântica suficiente para serem interpretadas; e hipermídia orienta transições possíveis em tempo de execução. Em outras palavras, o cliente não deveria conhecer cada próxima ação apenas por documentação externa fixa.

O **sistema em camadas** permite intermediários sem exigir que o cliente conheça toda a topologia. **Código sob demanda** é opcional: o servidor pode enviar código executável para ampliar o cliente, mas um sistema continua avaliável como REST sem essa restrição.

Uma rota com substantivo pode continuar sendo **RPC com aparência de recurso** quando funciona como chamada de procedimento, ignora a semântica dos métodos e obriga o cliente a montar todas as transições fora das respostas. No sentido inverso, um comando explícito não se torna defeituoso apenas por ser RPC. Classifique o sistema pelo conjunto de restrições e consequências, não pela estética da URL. **Uma API HTTP não é automaticamente REST**. O laboratório aplica identificação de recurso, representações e mensagens HTTP, mas não usa sua pequena escala para afirmar conformidade completa com todas as restrições.

## REST não é a única alternativa

REST favorece recursos, interface uniforme e uso explícito da semântica HTTP. **RPC** modela operações como chamadas nomeadas e pode representar ações complexas diretamente. **GraphQL** oferece um schema tipado e permite ao cliente selecionar campos e percorrer relações em uma consulta. **gRPC** define serviços e mensagens, normalmente com Protocol Buffers, e oferece geração de código e comunicação eficiente entre processos.

Não existe vencedor universal. REST costuma ser acessível para integrações web e ecossistemas heterogêneos. RPC pode expressar comandos sem forçá-los a parecer recursos. GraphQL atende interfaces com necessidades variáveis de leitura, mas transfere desafios de custo, autorização e cache para resolvers e consultas. gRPC favorece comunicação interna tipada e streaming, mas requer suporte de ferramentas e consumidores. A escolha parte de consumidores, topologia, latência, evolução e operação, não de popularidade.
