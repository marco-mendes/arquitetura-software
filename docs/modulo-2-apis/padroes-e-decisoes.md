# Padrões e decisões para APIs

## Começar pelos consumidores e pelas forças

Antes dos endpoints, identifique consumidores, tarefas, volume, latência, falhas, propriedade dos dados e evolução. Pergunte qual resultado deve ser observado, quando ele é necessário e quais mudanças internas não deveriam afetar o consumidor. No laboratório, `202` e `Location` prometem aceitação e acompanhamento, não decisão final da operadora.

## Escolher estilo por interação

Uma arquitetura pode combinar estilos por critério explícito: REST/HTTP para recursos web, gRPC para comandos internos tipados, GraphQL para grafos com seleções variáveis e RPC para operações naturalmente verbais.

Compare alternativas pelas mesmas dimensões:

| Dimensão | REST/HTTP | RPC | GraphQL | gRPC |
| --- | --- | --- | --- | --- |
| Unidade principal | recurso e representação | operação | tipo e seleção | serviço e mensagem |
| Descoberta | OpenAPI e documentação | descrição de métodos | introspecção e schema | arquivos `.proto` |
| Evolução | compatibilidade de recursos e schemas | compatibilidade de argumentos | depreciação de campos | regras de evolução do protobuf |
| Cache web | aproveita semântica HTTP | depende da convenção | exige estratégia própria | fora do modelo usual de cache web |
| Consumidores | amplo suporte HTTP | simples quando convenção é clara | clientes capazes de formular consultas | geração de código e suporte HTTP/2 |
| Risco típico | REST apenas nominal | proliferação de métodos | consultas caras e autorização granular | acoplamento a toolchain e operação |

## Contract-first e code-first

**Contract-first** antecipa revisão e mocks, mas pode se afastar da execução. **Code-first** gera o contrato de tipos e rotas rapidamente, mas pode publicar detalhes do framework sem decisão consciente. O laboratório compara `openapi.yaml` com `app.openapi()` e testa exemplos. Em uma equipe, escolha uma fonte principal e automatize a detecção de deriva.

## Evolução compatível

Compatibilidade não é apenas validar JSON. Adicionar `prazo_estimado` opcional tende a ser compatível; reaproveitar `situacao: recebida` para significar “aprovada” preserva a forma e quebra a semântica.

Classifique a mudança como aditiva, restritiva, semântica ou remoção; identifique consumidores; preserve comportamento antigo na transição; publique depreciação e alternativa; observe adoção; remova apenas depois do critério acordado.

Versão no caminho é visível, mas pode agrupar mudanças demais; cabeçalho preserva URI, porém é menos óbvio; negociação de mídia é precisa e mais complexa. Registre uma estratégia.

## Idempotência como política

`GET`, `PUT` e `DELETE` têm semântica idempotente, mas a implementação pode violá-la: `GET` não deve confirmar uma ação e `PUT` não deve somar a cada tentativa.

Para `POST`, uma chave pode associar consumidor, operação e conteúdo ao resultado. Repetição equivalente recebe o mesmo protocolo; corpo diferente, conflito. A política define retenção e concorrência. A API mínima não a implementa para não apresentar um dicionário local como solução distribuída confiável.

## Paginação e consistência de leitura

Paginação exige uma ordenação estável. `?offset=20&limit=10` sem ordenação definida não produz páginas reproduzíveis. Mesmo com ordenação, inserções antes do deslocamento movem itens. Um cursor pode incorporar a última chave observada e a ordenação; deve ser opaco para permitir evolução interna.

O contrato define limite padrão e máximo, continuação, cursor inválido, filtros e se a leitura é instantâneo ou coleção viva. A API mínima não lista elegibilidades, portanto não inventa paginação.

## API gateway: entrada central, não centro do domínio

Um **API gateway** encaminha chamadas e pode centralizar roteamento, TLS, limites, autenticação técnica, correlação e observabilidade. Regras do domínio e tradução semântica pertencem a componentes próprios; roteamento não resolve significado. Como traz salto de rede, configuração e operação, seria excesso no laboratório local. O módulo 4 retomará essa decisão.

## Erros e observabilidade sem vazamento

Separe erro do consumidor, recurso ausente, conflito, indisponibilidade e defeito interno. Códigos públicos são estáveis; diagnóstico fica em logs. Correlação segue uma execução, enquanto `protocolo` acompanha o negócio; não misture finalidades.

## ADR-002: o que registrar

Registre contexto, alternativas, decisão, consequências, evidência e revisão. Delimite REST/HTTP, `202`, OpenAPI, compatibilidade e testes; framework é mecanismo. Novo consumidor, streaming, paginação, idempotência forte ou duas versões podem disparar revisão.
