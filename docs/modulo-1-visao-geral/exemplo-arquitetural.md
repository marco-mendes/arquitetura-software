# Exemplo arquitetural: processamento de documentos

## O que este exemplo aplica

Esta página não apresenta conceito novo. Ela mostra em uso o vocabulário das duas páginas anteriores, na ordem em que um arquiteto o usaria. Se algum termo da tabela ainda parecer vago, abra o link antes de continuar.

| Conceito | Onde foi definido | Onde ele aparece nesta página |
| --- | --- | --- |
| Estilo como elementos, conectores e restrições | [Estilos arquiteturais](conceitos.md#estilos-arquiteturais) | cada estrutura nomeia seus elementos, o que os liga e o que fica proibido |
| Família "organização interna" | [Organização interna](conceitos.md#organizacao-interna) | camadas na submissão, microkernel nos leitores de formato e monólito modular como limite de implantação |
| Família "integração e comunicação" | [Integração e comunicação](conceitos.md#integracao-e-comunicacao) | pipes and filters no processamento |
| Cenário de atributo de qualidade | [Atributos de qualidade](../referencia/atributos-de-qualidade.md#como-usar-na-decisao) | a seção seguinte, que vem antes de qualquer caixa desenhada |
| Camada fechada e anti-padrão do sumidouro | [Camadas](padroes-e-decisoes.md#camadas) | figura 19 e o parágrafo logo abaixo dela |
| Filtro, pipe e rejeição explícita | [Pipes and Filters](padroes-e-decisoes.md#pipes-and-filters) | figuras 20 e 21 |
| Núcleo, contrato de extensão e core creep | [Microkernel](padroes-e-decisoes.md#microkernel) | figura 22 |
| ADR como decisão revisável | [ADR](padroes-e-decisoes.md#adr-o-mecanismo-para-escolher-estilos) | seção "Decisão provisória" |

A ordem das seções é a cadeia de raciocínio da unidade: o contexto e a força priorizada vêm antes de qualquer caixa desenhada; as alternativas, antes da escolha; a evidência, antes da decisão — que por sua vez registra o custo aceito e o gatilho de revisão.

Quem lê de trás para frente escolhe a figura de que gostou e procura a justificativa depois.

## Contexto antes da estrutura

Uma organização recebe JSON, CSV e XML para validação, normalização, enriquecimento e publicação. Espera duzentos mil documentos por hora; novos formatos entram poucas vezes por ano; uma equipe pequena opera um único ambiente. Chamaremos a solução de **plataforma de remessas**: parceiros enviam remessas, cada remessa contém documentos, e a plataforma devolve o que foi publicado e o que foi rejeitado.

Prioridades são throughput e rastreabilidade; modificabilidade é média. Durante a carga, a solução deve processar sessenta itens por segundo e identificar a etapa de cada rejeição.

Os dois parágrafos acima são um cenário de atributo de qualidade escrito em prosa. Nas seis partes de [atributos de qualidade](../referencia/atributos-de-qualidade.md#como-usar-na-decisao): a **fonte** são os sistemas parceiros; o **estímulo** é a chegada de documentos em três formatos; o **ambiente** é a carga esperada de duzentos mil documentos por hora; o **artefato** é a capacidade de processamento; a **resposta** é transformar e identificar a etapa de cada rejeição; a **medida** são sessenta itens por segundo com etapa registrada. O exercício começa aqui porque nenhuma das estruturas seguintes pode ser comparada sem uma medida comum.

## Alternativas comparadas

Camadas separariam entrada, aplicação, regra e infraestrutura. Isso ajuda a testar validações, mas não torna a sequência de transformações explícita. Microkernel isolaria leitores por formato, porém não organiza sozinho as etapas comuns. Monólito modular manteria implantação simples e limites por capacidade. Pipes and filters modelaria diretamente o fluxo e permitiria medir cada transformação.

A comparação usou a mesma grade para os quatro: a tabela de características avaliadas de 1 a 5 e os blocos "quando usar" e "quando não usar" de [padrões e decisões](padroes-e-decisoes.md). Camadas saem atrás aqui porque não tornam visível a sequência de transformações, que é o que a força priorizada exige. Priorize outra força e o resultado muda.

A escolha inicial combina um monólito modular como limite de implantação, pipes and filters na capacidade de processamento e pequenos adapters para os formatos. Combinar estilos é aceitável quando cada um resolve uma escala declarada. O risco é usar muitos nomes sem restrições verificáveis.

## A mesma plataforma, três estruturas deliberadas

A plataforma de remessas tem quatro capacidades. **Submissão** recebe e aceita ou recusa a remessa de um parceiro; **Processamento** transforma os documentos de uma remessa aceita; **Leitores de formato** interpretam JSON, CSV e XML e variam por parceiro; **Trilha** recebe fatos mínimos para rastreabilidade. Não há integração real: os nomes permitem enxergar a responsabilidade de cada fronteira.

Cada capacidade recebe o estilo cuja força corresponde à sua: consistência na submissão, fluxo no processamento, variação nos leitores.

### Submissão em camadas: uma remessa não pula a regra

```mermaid
flowchart TB
    C["Parceiro"] --> H["Interface HTTP\nrecebe a remessa"]
    H --> U["Caso de uso\naceitar remessa"]
    U --> R["Regra de Submissão\njanela contratada e duplicidade"]
    U --> P["Repositório de Remessas\ngrava a remessa aceita"]
    P --> D[("Dados de remessas")]
    H -. "não consulta" .-> D
    U --> A["Trilha\nregistra fato mínimo"]
```

**Texto alternativo:** fluxo de submissão em camadas: a interface chama o caso de uso, que aplica as regras de janela e duplicidade antes de persistir; a interface não acessa os dados diretamente.

*Figura 19 — Uma remessa atravessa fronteiras de camadas antes de ser persistida. Fonte: curso.*

**Leitura textual da figura:** o Parceiro envia a remessa à Interface HTTP. A interface chama o Caso de uso, que consulta a Regra de Submissão — janela contratada e remessa duplicada — antes de pedir ao Repositório que grave os Dados de remessas. O Caso de uso também registra um fato mínimo na Trilha. A ligação pontilhada mostra que a interface não consulta os dados diretamente; a regra de duplicidade não pode ser ignorada por uma tela.

Esse arranjo favorece consistência local e teste das regras sem banco. Se quase toda leitura apenas atravessar todas as camadas sem validação ou decisão, a equipe mede o custo e registra um caminho de leitura justificado; não cria atalhos silenciosos.

**Conceito aplicado:** a ligação pontilhada é a *camada fechada* de [Camadas](padroes-e-decisoes.md#camadas) — a interface não pula a camada seguinte para ler dados. A camada de negócios decide: recusa remessa fora da janela contratada e remessa repetida. Sem essas duas decisões o desenho cairia no *sumidouro* da figura 6, cobrando uma chamada extra sem devolver nada.

[Aprofundar Camadas](padroes-e-decisoes.md#camadas)

### Processamento como fluxo: cada transformação deixa uma pista

```mermaid
flowchart LR
    I["Adaptador de entrada"] -->|"Documento bruto"| V["Filtro: validar"]
    V -->|"Documento válido"| N["Filtro: normalizar"]
    N -->|"Documento canônico"| E["Filtro: enriquecer"]
    E -->|"Documento enriquecido"| P["Filtro: publicar"]
    V -->|"Rejeição identificada"| Q[("Registro de rejeições")]
    N -->|"Rejeição identificada"| Q
    E -->|"Rejeição identificada"| Q
```

**Texto alternativo:** pipeline de processamento no qual validar, normalizar, enriquecer e publicar recebem documentos em sequência; rejeições seguem para um registro com etapa identificada.

*Figura 20 — Transformações independentes conservam o contexto de uma rejeição. Fonte: curso.*

**Leitura textual da figura:** o Adaptador de entrada entrega um documento bruto ao filtro de validação. Documentos válidos atravessam normalização, enriquecimento e publicação; uma rejeição em validação, normalização ou enriquecimento é registrada com sua etapa. Nenhum filtro consulta o estado interno de outro filtro.

As setas nomeiam o contrato de cada pipe. Cada filtro recebe um valor e devolve sucesso com um novo valor ou rejeição com identificador, etapa e causa. Os filtros não consultam o estado interno uns dos outros. Essa restrição permite testar cada etapa e compor o fluxo.

**Conceito aplicado:** cada caixa é um dos quatro tipos canônicos de filtro de [Pipes and Filters](padroes-e-decisoes.md#pipes-and-filters). O adaptador de entrada é o *producer*, validar é um *tester*, normalizar e enriquecer são *transformers*, publicar é o *consumer*. A premissa de ausência de estado compartilhado vira aqui a proibição de um filtro ler o estado de outro; é ela que permite trocar uma etapa sem reescrever as demais.

[Aprofundar Pipes and Filters](padroes-e-decisoes.md#pipes-and-filters)

### O mesmo fluxo em execução: uma falha parcial

```mermaid
sequenceDiagram
    participant Entrada
    participant Validar
    participant Normalizar
    participant Enriquecer
    participant Publicar
    Entrada->>Validar: bruto, correlação
    Validar->>Normalizar: válido, correlação
    Normalizar->>Enriquecer: canônico, correlação
    Enriquecer-->>Entrada: rejeição, etapa, causa
    Entrada-->>Entrada: registra duração e rejeição
```

**Texto alternativo:** sequência de processamento em que a correlação acompanha o documento e uma falha no enriquecimento retorna com etapa e causa.

*Figura 21 — Uma falha parcial preserva correlação, etapa e causa. Fonte: curso.*

**Leitura textual da figura:** a Entrada envia um documento com correlação a Validar, que passa um valor válido para Normalizar e depois para Enriquecer. A falha de enriquecimento retorna à Entrada com etapa e causa; a Entrada registra duração e rejeição. A sequência evidencia que a correlação acompanha o fluxo, inclusive na falha.

A sequência mostra uma falha no enriquecimento. A correlação atravessa os pipes, permitindo relacionar o documento à etapa. Uma versão que apenas lança uma mensagem genérica atenderia à transformação, mas não à rastreabilidade.

### Leitores como núcleo e plugins: variar sem reescrever o comum

```mermaid
flowchart LR
    I["Remessa aceita"] --> N["Núcleo de leitura\nidentidade, estados e autorização"]
    N --> C["Contrato de extensão"]
    C --> P1["Plugin\nleitor CSV do parceiro A"]
    C --> P2["Plugin\nvalidação de esquema XML"]
    P1 --> N
    P2 --> N
    N --> AU["Trilha\nfato e correlação"]
    P1 -. "não acessa" .-> DB[("Dados internos do núcleo")]
    P2 -. "não acessa" .-> DB
```

**Texto alternativo:** núcleo de leitura mantém estados, autorização e contrato; plugins de formato devolvem documentos canônicos pelo contrato sem acessar dados internos.

*Figura 22 — O núcleo oferece o contrato; plugins devolvem resultados sem acessar seus dados internos. Fonte: curso.*

**Leitura textual da figura:** uma Remessa aceita chega ao Núcleo de leitura, que controla identidade, estados e autorização. O Núcleo expõe um Contrato de extensão usado por dois plugins: um leitor CSV específico do parceiro A e uma validação de esquema XML. Os plugins devolvem resultados ao Núcleo, que produz fato com correlação para a Trilha. As ligações pontilhadas indicam que plugins não leem os dados internos do núcleo diretamente.

Essa é a capacidade em que a mudança chega: um formato novo entra poucas vezes por ano, mas entra sempre pela mesma fronteira. Para a estrutura ser honesta, o contrato deve especificar entrada, resultado, erros e versão. Se um plugin precisa editar tabelas internas ou se o núcleo conhece regras particulares de todos os plugins, a equipe encontrou core creep e deve revisar a fronteira em vez de chamar o acoplamento de extensibilidade.

**Conceito aplicado:** núcleo, contrato de extensão e *core creep* vêm de [Microkernel](padroes-e-decisoes.md#microkernel). Um plugin que precisa do banco do núcleo continua sendo parte do núcleo, ainda que resida em outra pasta.

[Aprofundar Microkernel](padroes-e-decisoes.md#microkernel)

## Do cenário à evidência

Cada teste desta seção devolve uma parte do cenário declarado no início da página. O teste funcional usa exemplos pequenos para verificar ordem e transformação; o de desempenho mede a duração de um lote representativo e calcula throughput; o de falha injeta um documento sem referência de enriquecimento e verifica etapa e correlação. O resultado precisa informar ambiente e massa utilizada — um número sem condições não sustenta decisão.

Também há limites não resolvidos. Se o enriquecimento depender de um serviço remoto lento, o filtro pode dominar toda a vazão. Paralelizar exige decidir ordenação e concorrência. Persistir resultados intermediários melhora recuperação, mas acrescenta estado. Esses aspectos viram forças de um ADR posterior, em vez de serem ocultados pelo desenho inicial.

## Estrutura de Projeto

Uma implementação da capacidade de processamento pode separar o coordenador `Pipeline`, os filtros puros e os adaptadores de formato — que são os plugins do núcleo de leitura da figura 22. A árvore indica **responsabilidades**, não dependências automaticamente garantidas:

```text
processamento/
├── aplicacao/
│   └── pipeline.py       ← ordena filtros; não conhece seus detalhes
├── dominio/
│   ├── documento.py      ← modelo canônico
│   └── resultado.py      ← sucesso ou rejeição explícita
├── filtros/
│   ├── validar.py
│   ├── normalizar.py
│   └── enriquecer.py
└── adaptadores/
    ├── json.py
    ├── csv.py
    └── xml.py
```

Uma árvore de diretórios não prova isolamento: teste imports proibidos e substitua um filtro para verificar composição.

## Decisão provisória

O ADR deste exemplo aceitaria pipes and filters para explicitar transformações e manteria uma implantação única. Registraria o custo de contratos intermediários, correlação e eventual controle de concorrência. A evidência inicial seria o teste de throughput e rejeição. O gatilho de revisão seria a entrada de uma etapa com escala ou disponibilidade muito diferente das demais.

O exemplo demonstra o método sem depender do domínio hospitalar: começar pelo cenário, comparar alternativas, desenhar restrições, observar comportamento e declarar limites. Nada aqui foi inventado nesta página; tudo veio de [conceitos](conceitos.md) e de [padrões e decisões](padroes-e-decisoes.md).

No [estudo de caso](estudo-de-caso.md) você percorre a mesma sequência produzindo os artefatos. Não copie os módulos desta página para lá: as forças da plataforma hospitalar são outras.
