# Padrões, tecnologias e decisões

## Três categorias que não são sinônimas

Discussões arquiteturais perdem precisão quando estilo, padrão e tecnologia são tratados como nomes intercambiáveis. As três categorias se relacionam, mas respondem a perguntas em escalas diferentes.

Um **estilo arquitetural** impõe um vocabulário de elementos, conectores e restrições para organizar a solução. Camadas e microkernel são estilos. Um **padrão** descreve uma solução recorrente para um problema contextualizado, com consequências conhecidas. Repository, Adapter, Circuit Breaker e ADR são padrões em escalas diferentes. Uma **tecnologia** oferece mecanismos concretos: Python, Java, .NET, PostgreSQL, RabbitMQ e Structurizr Lite.

Escolher Spring Boot não escolhe automaticamente camadas. Um projeto Spring pode ser um monólito modular bem delimitado ou uma coleção sem fronteiras. Adotar FastAPI não define onde as regras residem. Usar ASP.NET Core não garante dependências voltadas ao domínio. A tecnologia habilita construções; a arquitetura declara responsabilidades e restrições.

| Pergunta | Categoria mais útil | Exemplo |
| --- | --- | --- |
| Como organizar o sistema completo? | Estilo | monólito modular |
| Como adaptar uma interface externa? | Padrão | Adapter |
| Com qual mecanismo executar a interface? | Tecnologia | FastAPI |
| Como registrar a escolha e suas consequências? | Padrão de decisão | ADR |

O [catálogo de padrões](../referencia/catalogo-de-padroes.md) conecta soluções recorrentes aos encontros em que serão aprofundadas. Neste primeiro encontro, o objetivo é reconhecer a escala da escolha e impedir que uma marca de ferramenta substitua o raciocínio.

## Forças orientam alternativas

Uma força é uma necessidade ou pressão que diferencia alternativas: frequência de mudança, throughput, experiência da equipe, simplicidade operacional, integração legada ou necessidade de extensão. A força deve ser específica o bastante para produzir consequências diferentes.

Considere “facilidade de manutenção”. A expressão pode significar modificar regras sem tocar na interface, localizar defeitos, atualizar uma dependência ou permitir trabalho independente. Cada interpretação favorece evidências diferentes. Transforme a força em cenário antes de atribuir valor ao estilo.

Uma matriz ajuda a evitar argumentos assimétricos:

| Alternativa | Força favorecida | Limite aceito | Evidência proposta |
| --- | --- | --- | --- |
| Camadas | testar regras separadas da infraestrutura | travessias podem adicionar custo | teste de domínio sem banco |
| Pipes and filters | elevar throughput de transformações | contratos intermediários precisam ser estáveis | medição de itens por segundo |
| Microkernel | incluir variações por extensão | núcleo e plugins exigem compatibilidade | adicionar plugin sem mudar o núcleo |
| Monólito modular | preservar implantação simples e limites internos | módulos compartilham processo | teste de dependência entre módulos |

A matriz não produz uma resposta automática. Ela torna visível onde faltam dados e permite discutir compromissos com o mesmo conjunto de critérios.

## Racional arquitetural

O racional explica por que uma decisão faz sentido nas condições conhecidas. Inclui alternativas rejeitadas e consequências desfavoráveis, não somente benefícios. Sem racional, uma equipe futura encontra uma estrutura, mas não sabe quais mudanças de contexto autorizam substituí-la.

Um bom encadeamento contém:

1. contexto delimitado e envolvidos afetados;
2. forças e restrições, preferencialmente mensuráveis;
3. alternativas reais comparadas pelos mesmos critérios;
4. decisão com consequências favoráveis e desfavoráveis;
5. evidência que sustenta a hipótese;
6. gatilho de revisão.

“Escolhemos microkernel porque é flexível” é circular. Uma justificativa melhor seria: “as regras variam por parceiro a cada mês; manteremos validações comuns no núcleo e variações em plugins; aceitamos testar compatibilidade; adicionaremos uma extensão piloto sem alterar o núcleo; revisaremos se plugins passarem a compartilhar estado”.

## ADR: uma decisão por registro

Um **Architecture Decision Record (ADR)** é um documento curto, versionado com os artefatos da solução. Cada registro aborda uma decisão significativa. Ele não precisa contar toda a história do sistema nem congelar a escolha para sempre.

O [template de ADR](../referencia/template-adr.md) usado na disciplina contém título, estado, contexto, forças, alternativas, decisão, consequências, evidências e gatilho de revisão. Estados comuns são proposto, aceito, rejeitado e substituído. Quando o contexto muda, crie novo ADR e conecte os registros; não apague o motivo histórico.

### Exemplo reduzido

**Título**

ADR-001 — Organizar variações por plugins.

**Contexto**

Regras variam com frequência e compartilham uma validação mínima.

**Alternativas**

Condicionais em um único módulo; camadas; núcleo com plugins.

**Decisão**

Adotar microkernel para isolar variações atrás de um contrato.

**Consequências**

Novas extensões ficam localizadas; compatibilidade passa a exigir testes dedicados.

**Evidência**

Implementar uma extensão e repetir a suíte com outra extensão desabilitada.

O exemplo é pequeno, mas contém tensão e verificação. O mini-ADR da oficina ampliará essa estrutura com resultados reais.

## Decisões são hipóteses testáveis

Uma arquitetura não se torna correta por estar documentada. O ADR declara a hipótese; código, testes, modelos e medições fornecem sinais. pytest pode comparar saídas; ArchUnit e NetArchTest podem impedir dependências proibidas; Structurizr Lite pode revelar conectores e responsabilidades; OpenTelemetry pode observar latência e falhas. O resultado pode confirmar, enfraquecer ou refutar o racional.

Essa postura torna a decisão revisável sem torná-la arbitrária. Mudanças exigem nova evidência e atualização explícita do histórico. Assim, arquitetura se aproxima de uma prática contínua: decidir, materializar, observar e aprender.
