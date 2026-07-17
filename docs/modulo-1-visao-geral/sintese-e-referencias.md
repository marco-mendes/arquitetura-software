# Síntese e referências

## O que deve permanecer

Arquitetura de software conecta estruturas, decisões e atributos de qualidade. Componentes têm responsabilidades; conectores materializam colaboração; fronteiras restringem dependências. Diagramas ajudam a comunicar essas relações, mas precisam de semântica, cenários de comportamento e correspondência com a implementação.

Estilos arquiteturais oferecem famílias de organização. Camadas separam níveis de responsabilidade. Pipes and filters compõe transformações. Microkernel mantém núcleo e extensões. Monólito modular combina unidade de implantação e módulos internos. Nenhum é vencedor universal, e estilos podem ser combinados quando cada um resolve uma escala explícita.

Estilo não é padrão nem tecnologia. Padrões resolvem problemas recorrentes contextualizados; tecnologias oferecem mecanismos. Python, Java e .NET podem implementar os mesmos limites. pytest, ArchUnit, NetArchTest e Structurizr Lite observam propriedades diferentes, mas não escolhem a arquitetura.

Uma decisão responsável compara alternativas pelas mesmas forças, aceita consequências e propõe evidência. O ADR preserva o racional e o gatilho de revisão. A fórmula prática do módulo é simples:

> nomeie o contexto, formule cenários, compare estilos, declare limites, execute evidências e registre uma decisão revisável.

## Checklist de revisão

- O sistema e o que está fora dele estão delimitados?
- Cada componente possui responsabilidade compreensível?
- Cada conector informa o mecanismo ou o dado trocado?
- As restrições do estilo aparecem no texto e no código?
- Atributos de qualidade foram escritos como cenários mensuráveis?
- Todas as alternativas foram comparadas pelas mesmas forças?
- Consequências desfavoráveis e premissas estão explícitas?
- A evidência realmente observa a promessa feita?
- O ADR possui gatilho de revisão?
- Diagramas, testes e decisão contam uma história consistente?

Se uma resposta for negativa, isso não invalida o trabalho inteiro. Ela identifica a próxima melhoria da baseline.

## Conexão com o projeto integrador

O produto deste encontro é a versão inicial da arquitetura da plataforma hospitalar: contexto, capacidades, cenários, estrutura, comparação e ADR-001. O [incremento 2](../projeto-integrador/incrementos.md#incremento-2-contratos-de-apis-e-integracoes-externas) usará as fronteiras para definir contratos de integração. Evite antecipar soluções; preserve questões abertas como hipóteses.

Mantenha os artefatos pequenos e conectados. Um cenário deve apontar para a decisão que o atende; o ADR deve apontar para a evidência; o diagrama deve usar os mesmos nomes das responsabilidades. Quando uma escolha mudar, crie novo registro e atualize as relações sem apagar o histórico.

## Referências essenciais

- BASS, Len; CLEMENTS, Paul; KAZMAN, Rick. *Software Architecture in Practice*. 4. ed. Addison-Wesley, 2021. Apresenta estruturas, atributos de qualidade, táticas e métodos de avaliação.
- CLEMENTS, Paul et al. *Documenting Software Architectures: Views and Beyond*. 2. ed. Addison-Wesley, 2010. Orienta escolha de visões e documentação de elementos, relações e racional.
- RICHARDS, Mark; FORD, Neal. *Fundamentals of Software Architecture*. O'Reilly, 2020. Compara características e compromissos de estilos contemporâneos.
- ROZANSKI, Nick; WOODS, Eóin. *Software Systems Architecture*. 2. ed. Addison-Wesley, 2011. Relaciona interesses, perspectivas e decisões significativas.
- SHAW, Mary; GARLAN, David. *Software Architecture: Perspectives on an Emerging Discipline*. Prentice Hall, 1996. Consolida componentes, conectores e estilos como tema próprio de projeto.
- NYGARD, Michael. [“Documenting Architecture Decisions”](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 2011. Registro original da prática enxuta de Architecture Decision Record.

## Documentação pública para a prática

- O site oficial do [C4 Model — tipos de diagrama](https://c4model.com/diagrams) distingue contexto, containers, componentes e código.
- A documentação oficial da [Structurizr DSL](https://docs.structurizr.com/dsl) apresenta modelos textuais baseados no C4; o guia de [execução local](https://docs.structurizr.com/local) explica a ferramenta usada na oficina.
- O [tutorial oficial de Python](https://docs.python.org/3/tutorial/) apoia a leitura do código, e o guia [Get Started do pytest](https://docs.pytest.org/en/stable/getting-started.html) documenta instalação, descoberta e asserções.
- O relatório público do Software Engineering Institute sobre [Quality Attributes](https://www.sei.cmu.edu/library/quality-attributes/) relaciona atributos, arquitetura e compromissos de projeto.

A [bibliografia da disciplina](../referencia/bibliografia.md) reúne as referências dos demais encontros. Para consulta rápida, use também o [glossário](../referencia/glossario.md), os [atributos de qualidade](../referencia/atributos-de-qualidade.md), o [catálogo de padrões](../referencia/catalogo-de-padroes.md) e o [guia de ferramentas](../referencia/guia-de-ferramentas.md).

## Próximo passo

Execute a oficina, conclua um exercício compatível com sua trilha e incorpore a entrega ao projeto integrador. Na revisão, apresente primeiro a força e a evidência; só então mostre o estilo escolhido. Essa ordem reduz debates baseados em preferência e prepara a turma para discutir contratos de APIs no módulo seguinte.
