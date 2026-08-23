# Casos reais: Stripe e o contrato que não pode quebrar

O [estudo de caso deste módulo](estudo-de-caso.md) decide contratos de integração para uma plataforma hospitalar. Esta página traz a mesma decisão numa empresa cujo produto **é** a API. Leia antes o [protocolo de leitura de caso público](../referencia/como-ler-um-caso-publico.md).

O caso é a Stripe, e a fonte é um artigo assinado por Brandur Leach no blog de engenharia da empresa, publicado em 5 de agosto de 2017.

## A restrição

Quando a API é o produto, quebrar o contrato quebra o negócio do cliente. Uma integração de pagamento escrita em 2013 e nunca mais tocada continua rodando em produção, e o cliente que a escreveu talvez nem trabalhe mais na empresa dele.

Isso cria uma tensão que o módulo trata em [contrato verificável e sua evolução](conceitos.md#o-contrato-verificavel-e-a-sua-evolucao). A empresa precisa evoluir o modelo de dados, corrigir nomes ruins e mudar formatos de resposta. E precisa fazer isso sem que nenhuma integração existente pare.

A saída comum no mercado é o versionamento por caminho: `/v1`, `/v2`, `/v3`. Ela funciona e tem um efeito conhecido: a cada versão maior, o cliente precisa reescrever a integração inteira de uma vez, e a empresa passa a manter duas implementações completas em paralelo.

## A decisão

A Stripe adotou versões contínuas identificadas pela data de lançamento, como `2017-05-24`, cada uma contendo um conjunto pequeno de mudanças. O artigo descreve o efeito pretendido: tornar as atualizações incrementais relativamente fáceis.

O mecanismo de vinculação é automático. Segundo o artigo: *"The first time a user makes an API request, their account is automatically pinned to the most recent version available, and from then on, every API call they make is assigned that version implicitly."* O cliente pode sobrescrever isso pelo cabeçalho `Stripe-Version` ou atualizar pelo painel.

A parte estruturalmente interessante vem em seguida. A Stripe não mantém uma implementação por versão. Cada mudança incompatível é encapsulada num módulo que declara a documentação da mudança, a transformação correspondente e os tipos de recurso afetados. A resposta é sempre gerada na versão mais recente e então transformada para trás, aplicando os módulos em ordem até chegar à versão à qual a conta do cliente está vinculada.

## Por que isso é uma decisão arquitetural

O desenho separa duas coisas que costumam ficar coladas: o modelo interno e a representação exposta. Existe uma única implementação viva, na versão atual, e uma cadeia de transformações que reconstrói o passado sob demanda.

A consequência é que o custo de manter compatibilidade deixa de crescer com a quantidade de versões e passa a crescer com a quantidade de mudanças incompatíveis. Cada mudança é escrita uma vez, como transformação, e continua sendo aplicada indefinidamente.

O artigo declara a escala do compromisso: quase cem atualizações incompatíveis ao longo de seis anos, todas ainda alcançáveis a partir da versão corrente.

## O que a própria Stripe reconhece como custo

O autor não vende a solução como gratuita. O artigo registra que versionamento é sempre um compromisso entre melhorar a experiência de quem integra e o trabalho adicional de manter versões antigas.

Vale explicitar o que esse trabalho significa na prática. Toda mudança incompatível exige escrever a transformação reversa, e essa transformação precisa ser testada contra todas as combinações de versões anteriores. Uma transformação escrita errado corrompe respostas de clientes antigos de forma silenciosa, porque eles não têm como saber qual deveria ser a resposta correta.

## O que o caso não prova

A Stripe expõe recursos com semântica estável, em que uma mudança quase sempre pode ser expressa como renomear, acrescentar ou reformatar um campo. Nem toda mudança cabe nisso. Quando o próprio conceito de negócio muda, não existe transformação reversa possível, e aí a versão nova é realmente incompatível.

A abordagem também depende de disciplina de produto que uma equipe interna raramente tem. Se seus consumidores são três times da mesma empresa, negociar uma janela de migração é mais barato do que construir e testar a cadeia de transformações.

Para o hospital do módulo, o contrato externo obrigatório é o TISS, definido por terceiro e sem margem de negociação. A lição transferível não é a data como número de versão. É a separação entre o modelo interno, que você controla, e a representação exposta, que você deve ao consumidor.

## Leitura guiada

**1. Comparação de estratégias.** Compare versionamento por caminho (`/v1`, `/v2`) com versões contínuas por data. Indique como cada um distribui o esforço entre o provedor e o consumidor da API.

**2. Vinculação implícita.** A Stripe vincula a conta à versão corrente na primeira requisição. Descreva o comportamento surpreendente que essa escolha evita para um cliente que integrou há três anos.

**3. Custo que não cresce com versões.** Explique por que gerar sempre na versão atual e transformar para trás faz o custo crescer com a quantidade de mudanças em vez da quantidade de versões.

**4. Limite do mecanismo.** Descreva uma mudança de contrato que não pode ser expressa como transformação reversa e explique o que o provedor deve fazer nesse caso.

**5. Transferência.** Retome a [Decisão 2 do estudo de caso](estudo-de-caso.md#decisao-2-rest-interno-e-soaptiss-externo-podem-coexistir) e diga qual parte da estratégia da Stripe se aplica ao contrato interno do hospital, e qual não se aplica ao contrato TISS.

## Fontes

- Brandur Leach, [APIs as infrastructure: future-proofing Stripe with versioning](https://stripe.com/blog/api-versioning) — Stripe, 5 de agosto de 2017. Fonte primária das citações, do mecanismo de transformação e do número de atualizações incompatíveis.
- Stripe, [API versioning](https://docs.stripe.com/api/versioning) — documentação oficial corrente do cabeçalho `Stripe-Version` e do esquema de datas.
- Stripe, [API reference](https://docs.stripe.com/api) — o contrato público em si, útil para observar a granularidade das mudanças.
