# Recuperação do mapa e dos estilos do Módulo 1

## Objetivo

Restaurar a função de orientação conceitual dos materiais `1.1` a `1.4` no site da disciplina sem recriar um acervo legado literal nem acrescentar páginas ao Módulo 1. O resultado deve permitir que um profissional sem formação prévia em arquitetura compreenda as quatro famílias de decisões e aprofunde, na mesma página, Camadas, Pipes and Filters e Microkernel.

Também separar do fluxo principal do Módulo 1 o vocabulário preparatório que hoje antecede os estilos. Esse conteúdo continua público e acessível como referência, mas não deve adiar o mapa de estilos.

## Decisões aprovadas

- `conceitos.md` volta a apresentar as quatro famílias com a estrutura didática do original: problema que a família resolve, estilos que ela abrange, ideia central, quando ajuda e principais limites.
- O mindmap Mermaid denso será removido. Um SVG autoral e responsivo mostrará uma raiz e quatro famílias em blocos sem conectores cruzando texto.
- `padroes-e-decisoes.md` continua uma única página, mas ganha três seções com âncoras próprias: `#camadas`, `#pipes-and-filters` e `#microkernel`.
- As três seções recuperam conteúdo conceitual e decisório dos documentos de origem, reescrito para o caso e a linguagem do curso. Elas não reproduzem literalmente o acervo nem expõem o rótulo “legado”.
- Caso arquitetural e exercícios existentes permanecem. Eles passam a ligar, quando fizer sentido, para as âncoras restauradas.
- `conceitos.md` do Módulo 1 começa por estilos arquiteturais e pelo mapa das famílias.
- Definições curtas e transversais passam para o glossário; explicações com figuras sobre leitura de representações passam para um apêndice público de referência.

## Vocabulário preparatório fora do fluxo do módulo

### Glossário

`docs/referencia/glossario.md` absorve verbetes concisos para decisão arquitetural, restrição, premissa, configuração e visão arquitetural. Os verbetes de componente, conector, fronteira, contrato e atributo de qualidade permanecem e são refinados apenas se precisarem de coerência terminológica.

### Apêndice: Como ler uma arquitetura

Uma página pública em `docs/referencia/como-ler-uma-arquitetura.md` reúne o conteúdo explicativo que não cabe em verbetes:

- componente, conector e configuração aplicados a um exemplo simples;
- diferença entre estrutura e comportamento;
- leitura de uma visão estrutural e de uma sequência;
- ligação entre restrições, decisões e atributos de qualidade.

As duas figuras hoje no início de `conceitos.md` migram para esse apêndice, com seus textos alternativos, legendas, fontes e leituras textuais. A nova página entra em **Referências** na navegação, não no Módulo 1.

## Conteúdo por seção

### Mapa das famílias

O mapa visual e a narrativa devem cobrir:

| Família | Pergunta orientadora | Estilos principais |
| --- | --- | --- |
| Organização interna | Como responsabilidades colaboram dentro de uma aplicação? | Camadas, MVC, Hexagonal, Microkernel, monólito modular |
| Decomposição por domínio | Onde termina um modelo de negócio e começa outro? | DDD, microsserviços, macrosserviços |
| Integração e comunicação | Como componentes trocam intenções e fatos? | Pipes and Filters, APIs, eventos |
| Execução e operação | Onde e como a solução roda? | Nuvem, contêineres, orquestração, serverless |

Cada família recebe uma explicação própria de problema, força, limite e ligação para a unidade que a aprofunda. Camadas, Pipes and Filters e Microkernel recebem também um enlace para a seção aprofundada da mesma unidade.

### Camadas

Explicar responsabilidades de apresentação, aplicação, domínio e infraestrutura; dependências permitidas e proibidas; camadas abertas e fechadas; sumidouro; OCP; relação com MVC, DDD e camadas lógicas/físicas. Explicitar quando o estilo ajuda e quando não é adequado.

### Pipes and Filters

Explicar contrato de entrada/saída; pipe; produtor, transformador, validador e consumidor; filtros com e sem estado; rejeição, correlação, ordenação e estado entre filtros; throughput e limites de latência. Explicitar quando o estilo ajuda e quando não é adequado.

### Microkernel

Explicar núcleo mínimo; registro e contrato de extensão; plugin; modos de implantação; compatibilidade e versão; core creep; isolamento de dados internos. Explicitar quando o estilo ajuda e quando não é adequado.

## Figura do mapa

O SVG será um ativo local em `docs/assets/images/`. Deve usar a paleta Academia, layout vertical ou em grade que não dependa de algoritmo de layout e texto suficientemente curto para caber dentro de cada bloco. A figura deve ter:

- `alt` descritivo;
- legenda com número e fonte;
- leitura textual adjacente;
- dimensões responsivas garantidas pelo CSS existente;
- fonte identificada como “curso”.

O Mermaid mindmap correspondente será removido do documento e dos testes de conteúdo. Outros Mermaid do módulo permanecem quando comunicarem estrutura ou sequência de forma mais adequada.

## Integração e qualidade

- Toda referência interna usa âncoras reais ou links relativos válidos.
- Os números das figuras do Módulo 1 permanecem crescentes na ordem de navegação.
- O Glossário e o apêndice ficam disponíveis em Referências; o Módulo 1 não começa por vocabulário preparatório.
- Os testes verificam a presença do SVG, das quatro famílias e dos conteúdos decisórios mínimos de Camadas, Pipes and Filters e Microkernel.
- Os testes verificam que o antigo `mindmap` não está mais em `conceitos.md`.
- Os testes verificam que o apêndice contém as duas representações e que os novos verbetes do glossário existem.
- `python -m unittest tests.test_module_one tests.test_content_contract -v`, `python scripts/validate_content.py --module modulo-1-visao-geral` e `python -m mkdocs build --strict` devem passar.

## Fora de escopo

- Criar novas páginas na navegação.
- Criar novas páginas no Módulo 1; o apêndice pertence exclusivamente à seção Referências.
- Alterar a sequência de aulas, o caso hospitalar ou os exercícios Bloom sem uma necessidade direta de ligação.
- Recuperar literalmente o material legado ou publicar a matriz editorial interna.
