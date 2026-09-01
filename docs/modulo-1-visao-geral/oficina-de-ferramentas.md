# Oficina de ferramentas: três estilos em código executável

Reserve aproximadamente **120 minutos**. Você executará três programas já presentes no capítulo 1, observará a saída e conectará o que ela mostra às responsabilidades de cada estilo arquitetural. Os exemplos usam somente a biblioteca padrão do Python; não crie ambiente virtual e não instale pacotes.

## Ferramenta

Python 3.10+ executa os três programas; um editor permite ler e alterar somente as cópias de entrega. A oficina não requer pacotes, contêineres ou ferramentas adicionais.

## Pré-requisitos

**Objetivo**

Executar e observar três exemplos reais do capítulo 1.

**Pré-requisito**

Ter o repositório clonado e acesso a um terminal e editor.

## Instalação

Não instale dependências do projeto. Apenas confirme ou instale Python 3.10+ pelo canal do seu sistema quando ele não estiver disponível.

## Preparação do laboratório (10 minutos)

Abra a raiz do seu clone, indicada abaixo por `<raiz-do-clone>`. Confirme Python 3.10 ou mais recente antes de começar. Cada programa é independente: execute `main.py` dentro do diretório do exemplo, para que seus imports locais funcionem.

### Windows

No PowerShell, a partir de `<raiz-do-clone>`:

```powershell
py --version
Set-Location codigos\cap01-estilos-fundamentais\1.2-estilo-em-camadas
py main.py
```

### macOS

No Terminal, a partir de `<raiz-do-clone>`:

```bash
python3 --version
cd codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas
python3 main.py
```

### Linux

No Terminal, a partir de `<raiz-do-clone>`:

```bash
python3 --version
cd codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas
python3 main.py
```

Se `py` (Windows) ou `python3` (macOS/Linux) não for reconhecido, instale Python 3.10+ pelo canal de instalação do seu sistema operacional, feche e reabra o terminal e repita a verificação. Se a versão exibida for anterior a 3.10, atualize-a pelo mesmo canal. Não há dependências adicionais para instalar.

## Execução

## Experimento 1 — Camadas: agenda clínica (30 minutos)

**Objetivo:**

Observar como apresentação, serviço, domínio e repositório colaboram para criar, conflitar, realizar e cancelar agendamentos.

**Artefato:**

`<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas`

**Pré-condição:**

Terminal aberto na raiz do clone e Python 3.10+ confirmado com `py --version` (Windows) ou `python3 --version` (macOS/Linux).

Leia os arquivos na ordem que fizer mais sentido para você; os links permitem comparar o clone com a fonte do capítulo:

- [apresentacao.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/apresentacao.py)
- [servicos.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/servicos.py)
- [dominio.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/dominio.py)
- [repositorios.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/repositorios.py)

| O que abrir | O que executar | O que observar | Se algo sair diferente |
| --- | --- | --- | --- |
| `main.py` e os quatro arquivos acima | Windows: `Set-Location .; Set-Location ".\codigos\cap01-estilos-fundamentais\1.2-estilo-em-camadas"; py main.py`<br>macOS/Linux: `cd . && cd "./codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas" && python3 main.py` | Os agendamentos válidos retornam HTTP 201; a sobreposição de horário retorna HTTP 409; a agenda muda após realizar e cancelar consultas. | Confirme que o terminal está no diretório deste exemplo e que executou `main.py`, não um arquivo isolado. Releia a mensagem exibida e compare o cenário em `main.py` com a regra em `servicos.py`. |

**Execute**

Execute o comando da tabela acima, a partir do diretório do exemplo.

**Observe**

O programa imprime três blocos. No primeiro, três agendamentos válidos retornam `HTTP 201 CREATED`:

```text
HTTP 201 CREATED → {'id': 1, 'medico': 'Dra. Ana Silva', 'paciente': 'Maria Santos', 'horario': '09:00–09:30', 'status': 'agendada'}
```

No segundo, uma tentativa de marcar consulta em horário já ocupado retorna:

```text
HTTP 409 CONFLICT → {'erro': 'Dr(a). Dra. Ana Silva já tem consulta das 09:00 às 09:30.'}
```

O detalhe que interessa não é o `409` em si, e sim **onde ele nasce**. A regra que detecta a sobreposição está em `dominio.py`, junto do conceito de horário. Quem a traduz para um código HTTP é `apresentacao.py`, na borda. O domínio não sabe o que é HTTP, e a apresentação não sabe o que faz dois horários conflitarem.

**Compare**

Compare a trajetória de uma chamada bem-sucedida com a de um conflito, e verá que ambas atravessam as mesmas quatro camadas na mesma ordem: apresentação recebe, serviço coordena, domínio decide, repositório guarda. Essa disciplina de sentido único é o que o módulo chama de [camadas](padroes-e-decisoes.md#camadas). Se a apresentação pudesse consultar o repositório diretamente para "otimizar", a camada de serviço deixaria de ser o lugar único onde o caso de uso está descrito.

Repare também no que o repositório entrega: uma lista em memória. Trocá-la por um banco real exigiria alterar `repositorios.py` e mais nada — nem o domínio, nem o serviço, nem a apresentação. É a promessa do estilo sendo verificável em três minutos de leitura.

Questões exploratórias:

1. Onde a entrada é convertida em uma chamada ao serviço e onde a resposta HTTP é formatada?
2. Qual regra impede o conflito de agenda? Que objeto do domínio ajuda a expressá-la?
3. Que dependência precisaria mudar para substituir o armazenamento em memória, e qual camada deveria permanecer estável?

Antes de alterar qualquer condição, copie o exemplo para sua entrega. No PowerShell, a partir de `<raiz-do-clone>`:

```powershell
Set-Location .
New-Item -ItemType Directory -Force entregas\unidade-1 | Out-Null
Copy-Item -Recurse codigos\cap01-estilos-fundamentais\1.2-estilo-em-camadas entregas\unidade-1\camadas
Set-Location entregas\unidade-1\camadas
py main.py | Tee-Object -FilePath saida-antes.txt
```

No macOS/Linux:

```bash
cd .
mkdir -p entregas/unidade-1
cp -R codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas entregas/unidade-1/camadas
cd entregas/unidade-1/camadas
python3 main.py | tee saida-antes.txt
```

Altere uma condição já existente no cenário ou em uma regra. Ainda no diretório da cópia local `entregas/unidade-1/camadas`, capture a execução posterior. No Windows PowerShell:

```powershell
py main.py | Tee-Object -FilePath saida-depois.txt
```

No macOS/Linux:

```bash
python3 main.py | tee saida-depois.txt
```

Descreva o que mudou na saída e qual responsabilidade foi afetada. Não há uma alteração canônica: escolha uma hipótese que você consiga explicar. Para reverter, exclua a cópia em `entregas/unidade-1/camadas` e faça a cópia novamente; o exemplo original não deve ser modificado.

## Experimento 2 — Pipes and Filters: triagem de currículos (35 minutos)

**Objetivo:**

Rastrear como dados percorrem filtros de produção, validação, transformação e consumo até formar o ranking.

**Artefato:**

`<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters`

**Pré-condição:**

Terminal aberto na raiz do clone e Python 3.10+ confirmado com `py --version` (Windows) ou `python3 --version` (macOS/Linux).

Abra o orquestrador e os quatro tipos de filtro:

- [framework.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/framework.py)
- [filtros/producer.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/producer.py)
- [filtros/testers.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/testers.py)
- [filtros/transformers.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/transformers.py)
- [filtros/consumer.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/consumer.py)

| O que abrir | O que executar | O que observar | Se algo sair diferente |
| --- | --- | --- | --- |
| `main.py`, `framework.py` e os filtros producer, tester, transformer e consumer | Windows: `Set-Location .; Set-Location ".\codigos\cap01-estilos-fundamentais\1.3-pipes-and-filters"; py main.py`<br>macOS/Linux: `cd . && cd "./codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters" && python3 main.py` | Mensagens de descarte ou reprovação surgem antes do relatório; campos são normalizados e os aprovados aparecem ranqueados por score. | Confirme o diretório e revise a sequência de `.adicionar(...)` em `main.py`. Um resultado diferente pode decorrer de ordem, critérios ou dados de entrada: localize qual filtro produz a linha inesperada. |

**Observe**

Logo no início, o programa imprime a composição do fluxo, e essa linha é o mapa do estilo inteiro:

```text
Pipeline: Pipeline(LeitorDeCurriculos → ValidadorDeCurriculo → NormalizadorDeCampos →
          FiltroPorExperienciaMinima → FiltroPorPretensaoSalarial → CalculadorDeScore → RelatorioDeTriagem)
```

Depois vêm as saídas dos seis currículos processados:

```text
  [DESCARTADO] Currículo id=3: nome ausente
  [REPROVADO] Bruno Rocha: 1 ano(s) < mínimo 3
  [REPROVADO] Clara Mendes: pretensão R$22,000 > máximo R$18,000

════════════════════════════════════════════════════════════
  TRIAGEM CONCLUÍDA — 3 candidato(s) aprovado(s)
════════════════════════════════════════════════════════════
```

Repare na diferença entre `[DESCARTADO]` e `[REPROVADO]`. O primeiro sai por dado ausente, no validador; o segundo sai por critério de negócio, nos filtros seguintes. Cada item sai do fluxo no estágio que sabe julgá-lo, e nenhum estágio precisa conhecer os critérios dos outros.

**Compare**

Compare esta arquitetura com a de camadas do experimento anterior. Lá, uma chamada atravessava as quatro camadas e voltava; o desenho era vertical e de ida e volta. Aqui o dado atravessa uma sequência e **não volta**: cada filtro recebe, decide e passa adiante. É a diferença entre organizar por responsabilidade técnica e organizar por etapa de transformação, tratada em [pipes and filters](padroes-e-decisoes.md#pipes-and-filters).

A propriedade que dá nome ao estilo aparece na linha da composição: os filtros são independentes o bastante para serem reordenados, removidos ou acrescentados sem tocar nos vizinhos, porque todos falam o mesmo formato de dado. Trocar a ordem de dois filtros muda o resultado sem quebrar o programa — e é justamente esse experimento que a extensão adiante propõe.

Questões exploratórias:

1. Qual parte recebe dados brutos e qual parte apresenta o resultado final?
2. Em que etapas itens deixam de seguir pelo pipe? Em que etapa eles são transformados sem descarte?
3. Por que o ranking pertence ao fim do fluxo? Que efeito teria reorganizar filtros?

Copie antes de experimentar. No PowerShell, a partir de `<raiz-do-clone>`:

```powershell
Set-Location .
New-Item -ItemType Directory -Force entregas\unidade-1 | Out-Null
Copy-Item -Recurse codigos\cap01-estilos-fundamentais\1.3-pipes-and-filters entregas\unidade-1\pipes-and-filters
Set-Location entregas\unidade-1\pipes-and-filters
py main.py | Tee-Object -FilePath saida-antes.txt
```

No macOS/Linux:

```bash
cd .
mkdir -p entregas/unidade-1
cp -R codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters entregas/unidade-1/pipes-and-filters
cd entregas/unidade-1/pipes-and-filters
python3 main.py | tee saida-antes.txt
```

Altere uma condição observável da cópia — dados de entrada, um critério ou a composição do fluxo. Ainda no diretório da cópia local `entregas/unidade-1/pipes-and-filters`, capture a execução posterior. No Windows PowerShell:

```powershell
py main.py | Tee-Object -FilePath saida-depois.txt
```

No macOS/Linux:

```bash
python3 main.py | tee saida-depois.txt
```

Registre o efeito sobre descarte, transformação ou ranking. Evite buscar uma saída “certa”: a entrega deve explicar sua hipótese e a evidência. Para desfazer, exclua a cópia e repita a cópia a partir do código original.

## Experimento 3 — Microkernel: faturamento por plugins (35 minutos)

**Objetivo:**

Identificar o contrato estável do núcleo, o registro de plugins e a contribuição de cada extensão ao faturamento.

**Artefato:**

`<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.4-microkernel`

**Pré-condição:**

Terminal aberto na raiz do clone e Python 3.10+ confirmado com `py --version` (Windows) ou `python3 --version` (macOS/Linux).

Observe o núcleo e extensões concretas:

- [nucleo.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/nucleo.py)
- [dominio.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/dominio.py)
- [plugins/impostos_sp.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/impostos_sp.py)
- [plugins/impostos_rj.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/impostos_rj.py)
- [plugins/frete.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/frete.py)
- [plugins/notificacao.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/notificacao.py)

| O que abrir | O que executar | O que observar | Se algo sair diferente |
| --- | --- | --- | --- |
| `main.py`, `nucleo.py` e os plugins listados | Windows: `Set-Location .; Set-Location ".\codigos\cap01-estilos-fundamentais\1.4-microkernel"; py main.py`<br>macOS/Linux: `cd . && cd "./codigos/cap01-estilos-fundamentais/1.4-microkernel" && python3 main.py` | O registro mostra plugins por categoria; o núcleo executa impostos, frete e notificação nessa ordem; cada regra só contribui quando seu contexto se aplica. | Verifique se está usando o `main.py` do microkernel. Compare `ORDEM_CATEGORIAS` em `nucleo.py`, os plugins registrados e os dados da fatura que ativam cada regra. |

**Observe**

A primeira coisa que o programa faz é registrar os plugins, e a saída torna esse momento visível:

```text
Registrando plugins...
  [Registry] Plugin 'ICMS-SP' registrado em 'impostos'
  [Registry] Plugin 'ISS-SP' registrado em 'impostos'
  [Registry] Plugin 'ICMS-RJ' registrado em 'impostos'
  [Registry] Plugin 'Frete-Padrão' registrado em 'frete'
  [Registry] Plugin 'Notificação-Email' registrado em 'notificacao'

Plugins ativos: {'impostos': ['ICMS-SP', 'ISS-SP', 'ICMS-RJ'], 'frete': ['Frete-Padrão'], 'notificacao': ['Notificação-Email']}
```

Esse registro é o mecanismo central do estilo. O núcleo não tem nenhuma menção a ICMS, ISS ou São Paulo no seu código: ele conhece apenas as categorias e a ordem em que executá-las. Quem sabe calcular imposto paulista é o plugin, que se anuncia ao núcleo em tempo de execução.

Em seguida, ao processar cada fatura, apenas os plugins cujo contexto se aplica contribuem. Uma fatura de São Paulo ativa `ICMS-SP` e `ISS-SP`; uma do Rio ativa `ICMS-RJ`. Nenhum `if` sobre estado aparece no núcleo.

**Compare**

Compare o custo de uma mudança nos três estilos que você acabou de rodar. Para atender um novo estado, o microkernel pede um arquivo novo de plugin e uma linha de registro, sem tocar no núcleo. Na versão em camadas, uma regra nova entraria no domínio, que é código compartilhado por todos os casos. E no fluxo de filtros, entraria um estágio novo na sequência.

É essa a propriedade que o módulo atribui ao [microkernel](padroes-e-decisoes.md#microkernel): o sistema cresce por adição, e não por modificação. O preço aparece na mesma saída — existe um contrato de extensão a manter, e o núcleo precisa de um mecanismo de registro que os outros dois estilos dispensam. Quando esse contrato precisa mudar, todos os plugins mudam junto.

Os três experimentos, juntos, sustentam a tese central de [comparar sem eleger um vencedor](conceitos.md#comparar-nao-eleger-um-vencedor-universal): o mesmo domínio hospitalar poderia ser escrito em qualquer um dos três, e o que muda é onde a mudança futura vai doer.

Questões exploratórias:

1. Que contrato o núcleo conhece e quais detalhes ele deixa para os plugins?
2. Como a ordem por categoria afeta o total e a notificação?
3. Quais regras contribuem para uma fatura de SP, uma de RJ e uma de valor alto? Onde a saída mostra isso?

Crie uma cópia antes de investigar. No PowerShell, a partir de `<raiz-do-clone>`:

```powershell
Set-Location .
New-Item -ItemType Directory -Force entregas\unidade-1 | Out-Null
Copy-Item -Recurse codigos\cap01-estilos-fundamentais\1.4-microkernel entregas\unidade-1\microkernel
Set-Location entregas\unidade-1\microkernel
py main.py | Tee-Object -FilePath saida-antes.txt
```

No macOS/Linux:

```bash
cd .
mkdir -p entregas/unidade-1
cp -R codigos/cap01-estilos-fundamentais/1.4-microkernel entregas/unidade-1/microkernel
cd entregas/unidade-1/microkernel
python3 main.py | tee saida-antes.txt
```

Na cópia, modifique uma condição de uma regra, do registro ou de uma fatura. Ainda no diretório da cópia local `entregas/unidade-1/microkernel`, capture a execução posterior. No Windows PowerShell:

```powershell
py main.py | Tee-Object -FilePath saida-depois.txt
```

No macOS/Linux:

```bash
python3 main.py | tee saida-depois.txt
```

Explique como a ordem de categorias e a contribuição das regras tornaram a mudança visível. Não existe uma modificação prescrita. Para retornar ao estado inicial, apague a cópia em `entregas/unidade-1/microkernel` e copie novamente o diretório original.

## Resultado esperado

Cada `main.py` termina sem erro e imprime a demonstração descrita em sua tabela: respostas HTTP e conflito em Camadas; descarte, transformação e ranking em Pipes and Filters; categorias e contribuições de plugins em Microkernel.

## Interpretação

**Compare**

Uma saída observável mostra o comportamento deste cenário didático; ela não demonstra que um estilo é universalmente melhor. Use as perguntas e sua nota para justificar a relação entre código, responsabilidade e evidência.

## Limpeza e contingência

Se o comando falhar, confira o diretório atual e a versão de Python, depois registre a mensagem completa. Para desfazer uma extensão, exclua apenas a cópia correspondente em `<raiz-do-clone>/entregas/unidade-1/` e copie o exemplo original novamente.

## Evidência a entregar

## Entrega e fechamento (10 minutos)

Em `<raiz-do-clone>/entregas/unidade-1/`, entregue as três cópias, cada uma com `saida-antes.txt`, `saida-depois.txt` e uma breve nota (por exemplo, `observacoes.md`) contendo: a condição alterada, o que a saída revelou e qual responsabilidade arquitetural você relacionou à evidência. A saída deve sustentar a explicação; ela não precisa coincidir com a de outro grupo.

Se algum experimento não executar, registre o comando, a mensagem completa e o diretório atual na nota. Isso é evidência suficiente para retomar a investigação sem alterar o código original.
