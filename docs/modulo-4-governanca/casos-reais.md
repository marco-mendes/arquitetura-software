# Casos reais: Zalando e a governança que roda na esteira

O [estudo de caso deste módulo](estudo-de-caso.md) trata governança como evidência observável, e corrige uma centralização que produziu atrito sem produzir controle. Esta página traz uma organização que publicou o próprio instrumento de governança e o mantém aberto. Leia antes o [protocolo de leitura de caso público](../referencia/como-ler-um-caso-publico.md).

O caso tem uma vantagem rara: a fonte primária não é um relato sobre a decisão. É o artefato em si. As *RESTful API Guidelines* da Zalando estão publicadas na íntegra e recebem contribuição por *pull request*.

## A restrição

A Zalando descreve o contexto no próprio documento: equipes pequenas de engenharia possuem, implantam e operam microsserviços em contas AWS próprias.

Essa autonomia produz um efeito previsível. Cada equipe resolve paginação de um jeito, nomeia campos à sua maneira, escolhe um formato de data e inventa a própria convenção de erro. Individualmente, todas as escolhas são defensáveis. No conjunto, quem consome três APIs da mesma empresa aprende três dialetos.

O documento declara o objetivo em uma frase que serve como critério de aceitação: *"Ideally, all Zalando APIs will look like the same author created them."*

## A decisão

A Zalando escreveu as regras, classificou cada uma por força normativa e construiu ferramenta para verificá-las.

**Classificação por obrigatoriedade.** As regras usam **MUST**, **SHOULD** e **MAY** com a interpretação da RFC 2119. Uma regra MUST é condição de aceitação; uma MAY é orientação. A distinção evita o problema clássico de um guia de estilo em que tudo tem o mesmo peso e, por isso, nada é cobrado.

**Escopo por audiência.** As diretrizes reconhecem cinco níveis de exposição: interna ao componente, interna à unidade de negócio, interna à empresa, para parceiro externo e pública. A exigência varia conforme o nível, o que evita aplicar rigor de API pública a um contrato entre dois módulos do mesmo time.

**API como produto.** O documento instrui: *"Treat your API as product and act like a product owner."* O princípio API-First exige definir a API antes de implementá-la, usando linguagem de especificação padrão, e obter revisão antecipada de pares e de quem vai consumir.

**Verificação automatizada.** A Zalando mantém um serviço de análise estática de API chamado Zally, e o documento afirma que as equipes devem usá-lo para checagem automática das regras.

## Por que isso é arquitetura, e não papelada

Este módulo insiste que política sem mecanismo de verificação é intenção. O caso Zalando mostra a cadeia completa, e vale ver os quatro elos separados.

| Elo | Artefato na Zalando | Falha se ausente |
| --- | --- | --- |
| Regra escrita | as diretrizes publicadas | cada equipe inventa a própria convenção |
| Força normativa | MUST, SHOULD, MAY da RFC 2119 | tudo vira recomendação e nada é cobrado |
| Verificação | Zally na esteira de integração | conformidade depende de revisor humano disponível |
| Manutenção | API Guild e contribuição por *pull request* | o guia envelhece e passa a ser ignorado |

A propriedade também é declarada. A API Guild mantém o documento, as equipes são responsáveis por cumpri-lo durante o desenvolvimento e são incentivadas a contribuir com a evolução por *pull request*. O texto reconhece que permanecerá, em alguma medida, trabalho em andamento.

Essa última frase é o detalhe mais honesto do caso. Um guia de governança que se declara terminado já começou a envelhecer.

## O que o caso não prova

Publicar as diretrizes não demonstra que elas são cumpridas. O documento descreve o processo pretendido; ele não mede adesão, não informa quantas exceções foram concedidas nem quantas APIs em produção violam regras MUST. Trate o caso como evidência de desenho de governança, e não como evidência de resultado.

O modelo também pressupõe uma organização com dezenas de equipes autônomas e uma guilda com tempo dedicado. Numa empresa com três equipes, o mesmo efeito se obtém com um arquivo de convenções no repositório compartilhado e uma verificação na esteira. O elemento transferível é a cadeia dos quatro elos, e não o organograma.

Por fim, análise estática captura forma. Ela verifica se o recurso está no plural, se o erro segue o formato definido, se a paginação usa os parâmetros combinados. Ela não verifica se a API modela a capacidade de negócio certa. Essa continua sendo revisão humana, e o documento a exige antes da implementação.

## Leitura guiada

**1. Custo da autonomia.** Explique o mecanismo pelo qual equipes autônomas produzem inconsistência de contrato mesmo quando cada decisão isolada é razoável.

**2. Força normativa.** Justifique por que separar MUST de SHOULD é condição para que um guia seja cobrável, e descreva o que acontece com um guia em que tudo é recomendação.

**3. Escopo por audiência.** A Zalando aplica exigências diferentes conforme a exposição da API. Aplique essa graduação às APIs do hospital e diga qual delas mereceria o rigor de API pública.

**4. Os quatro elos.** Escolha uma política de governança discutida em [padrões e decisões](padroes-e-decisoes.md#registro-de-decisao-enxuto) e escreva os quatro elos correspondentes: regra, força, verificação e manutenção.

**5. Limite da verificação automática.** Descreva um defeito de contrato que o Zally aprovaria e que ainda assim comprometeria a integração. Indique qual instrumento pega esse defeito.

## Fontes

- Zalando, [RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) — o artefato de governança em si. Fonte de todas as citações, da classificação RFC 2119, dos níveis de audiência e do papel da API Guild.
- Zalando, [Zally](https://github.com/zalando/zally) — repositório oficial do serviço de análise estática citado nas diretrizes.
- Zalando, [restful-api-guidelines](https://github.com/zalando/restful-api-guidelines) — repositório do documento, onde o histórico de contribuições mostra a manutenção em funcionamento.
- IETF, [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — definição normativa de MUST, SHOULD e MAY adotada pelas diretrizes.
