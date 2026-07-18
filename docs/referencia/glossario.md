# Glossário

## Estrutura e decisão

**Estilo arquitetural:** conjunto reconhecível de tipos de elemento, relações e restrições que orienta a organização de uma solução.

**Decisão arquitetural:** escolha de organização difícil de reverter que atende forças relevantes e restringe escolhas posteriores.

**Restrição:** limite que reduz as alternativas admissíveis para a arquitetura, como ambiente, tecnologia ou regra de dependência.

**Premissa:** condição considerada verdadeira para decidir, mas que deve ser revista quando surgirem evidências contrárias.

**Componente:** unidade com responsabilidade identificável que realiza computação ou armazena dados.

**Conector:** mecanismo pelo qual componentes colaboram, como chamada, mensagem, evento ou fluxo de dados.

**Configuração:** arranjo de componentes, conectores e restrições que descreve como uma arquitetura é organizada em uma visão.

**Visão arquitetural:** representação de uma arquitetura para uma preocupação específica, como módulos, execução ou implantação.

**Fronteira:** limite de responsabilidade, mudança ou propriedade que separa partes da solução.

**Contrato:** acordo explícito sobre dados, comportamento, condições e evolução de uma interação.

**Atributo de qualidade:** propriedade observável usada para avaliar como uma solução responde a um cenário, além de suas funções.

## Relações internas

**Acoplamento:** grau de dependência entre elementos. Dependências numerosas, implícitas ou instáveis aumentam o custo de mudança conjunta.

**Coesão:** grau em que responsabilidades de um elemento contribuem para um propósito comum. Alta coesão favorece compreensão e evolução localizada.

## Sistemas distribuídos

**Idempotência:** propriedade de uma operação cujo efeito observável permanece equivalente quando a mesma solicitação válida é repetida.

**Consistência eventual:** modelo no qual réplicas podem divergir temporariamente, mas convergem quando as atualizações cessam e são propagadas.

**Telemetria:** sinais produzidos pelo sistema — como logs, métricas e rastros — para compreender estado, comportamento e falhas.

## Governança e infraestrutura

**Plano de dados:** caminho que processa o tráfego e os dados da aplicação conforme regras já distribuídas.

**Plano de controle:** conjunto de mecanismos que define, distribui e acompanha configuração e políticas aplicadas ao plano de dados.
