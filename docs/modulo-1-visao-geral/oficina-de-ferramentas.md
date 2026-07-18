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

### Essencial em aula

## Experimento 1 — Camadas: agenda clínica (30 minutos)

Diretório local: `<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas`

Leia os arquivos na ordem que fizer mais sentido para você; os links permitem comparar o clone com a fonte do capítulo:

- [apresentacao.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/apresentacao.py)
- [servicos.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/servicos.py)
- [dominio.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/dominio.py)
- [repositorios.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas/repositorios.py)

| O que abrir | O que executar | O que observar | Se algo sair diferente |
| --- | --- | --- | --- |
| `main.py` e os quatro arquivos acima | Windows: `py main.py`<br>macOS/Linux: `python3 main.py` | Os agendamentos válidos retornam HTTP 201; a sobreposição de horário retorna HTTP 409; a agenda muda após realizar e cancelar consultas. | Confirme que o terminal está no diretório deste exemplo e que executou `main.py`, não um arquivo isolado. Releia a mensagem exibida e compare o cenário em `main.py` com a regra em `servicos.py`. |

**Execute**

Execute o comando indicado na tabela.

**Observe**

Registre as linhas de agendamento e conflito.

**Compare**

Relacione cada resultado às responsabilidades dos arquivos.

### Exploração em dupla

Questões exploratórias:

1. Onde a entrada é convertida em uma chamada ao serviço e onde a resposta HTTP é formatada?
2. Qual regra impede o conflito de agenda? Que objeto do domínio ajuda a expressá-la?
3. Que dependência precisaria mudar para substituir o armazenamento em memória, e qual camada deveria permanecer estável?

### Extensão reversível

Antes de alterar qualquer condição, copie o exemplo para sua entrega. No PowerShell, a partir de `<raiz-do-clone>`:

```powershell
New-Item -ItemType Directory -Force entregas\unidade-1 | Out-Null
Copy-Item -Recurse codigos\cap01-estilos-fundamentais\1.2-estilo-em-camadas entregas\unidade-1\camadas
Set-Location entregas\unidade-1\camadas
py main.py | Tee-Object -FilePath saida-antes.txt
```

No macOS/Linux:

```bash
mkdir -p entregas/unidade-1
cp -R codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas entregas/unidade-1/camadas
cd entregas/unidade-1/camadas
python3 main.py | tee saida-antes.txt
```

Altere uma condição já existente no cenário ou em uma regra, execute de novo e guarde `saida-depois.txt`. Descreva o que mudou na saída e qual responsabilidade foi afetada. Não há uma alteração canônica: escolha uma hipótese que você consiga explicar. Para reverter, exclua a cópia em `entregas/unidade-1/camadas` e faça a cópia novamente; o exemplo original não deve ser modificado.

## Experimento 2 — Pipes and Filters: triagem de currículos (35 minutos)

Diretório local: `<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters`

Abra o orquestrador e os quatro tipos de filtro:

- [framework.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/framework.py)
- [filtros/producer.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/producer.py)
- [filtros/testers.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/testers.py)
- [filtros/transformers.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/transformers.py)
- [filtros/consumer.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters/filtros/consumer.py)

| O que abrir | O que executar | O que observar | Se algo sair diferente |
| --- | --- | --- | --- |
| `main.py`, `framework.py` e os filtros producer, tester, transformer e consumer | No Windows: `Set-Location <raiz-do-clone>\codigos\cap01-estilos-fundamentais\1.3-pipes-and-filters; py main.py`<br>macOS/Linux: `cd <raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters && python3 main.py` | Mensagens de descarte ou reprovação surgem antes do relatório; campos são normalizados e os aprovados aparecem ranqueados por score. | Confirme o diretório e revise a sequência de `.adicionar(...)` em `main.py`. Um resultado diferente pode decorrer de ordem, critérios ou dados de entrada: localize qual filtro produz a linha inesperada. |

Questões exploratórias:

1. Qual parte recebe dados brutos e qual parte apresenta o resultado final?
2. Em que etapas itens deixam de seguir pelo pipe? Em que etapa eles são transformados sem descarte?
3. Por que o ranking pertence ao fim do fluxo? Que efeito teria reorganizar filtros?

### Extensão reversível

Copie antes de experimentar. No PowerShell, a partir de `<raiz-do-clone>`:

```powershell
New-Item -ItemType Directory -Force entregas\unidade-1 | Out-Null
Copy-Item -Recurse codigos\cap01-estilos-fundamentais\1.3-pipes-and-filters entregas\unidade-1\pipes-and-filters
Set-Location entregas\unidade-1\pipes-and-filters
py main.py | Tee-Object -FilePath saida-antes.txt
```

No macOS/Linux:

```bash
mkdir -p entregas/unidade-1
cp -R codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters entregas/unidade-1/pipes-and-filters
cd entregas/unidade-1/pipes-and-filters
python3 main.py | tee saida-antes.txt
```

Altere uma condição observável da cópia — dados de entrada, um critério ou a composição do fluxo — e gere `saida-depois.txt`. Registre o efeito sobre descarte, transformação ou ranking. Evite buscar uma saída “certa”: a entrega deve explicar sua hipótese e a evidência. Para desfazer, exclua a cópia e repita a cópia a partir do código original.

## Experimento 3 — Microkernel: faturamento por plugins (35 minutos)

Diretório local: `<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.4-microkernel`

Observe o núcleo e extensões concretas:

- [nucleo.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/nucleo.py)
- [dominio.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/dominio.py)
- [plugins/impostos_sp.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/impostos_sp.py)
- [plugins/impostos_rj.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/impostos_rj.py)
- [plugins/frete.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/frete.py)
- [plugins/notificacao.py](https://github.com/marco-mendes/arquitetura-software/blob/main/codigos/cap01-estilos-fundamentais/1.4-microkernel/plugins/notificacao.py)

| O que abrir | O que executar | O que observar | Se algo sair diferente |
| --- | --- | --- | --- |
| `main.py`, `nucleo.py` e os plugins listados | No Windows: `Set-Location <raiz-do-clone>\codigos\cap01-estilos-fundamentais\1.4-microkernel; py main.py`<br>macOS/Linux: `cd <raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.4-microkernel && python3 main.py` | O registro mostra plugins por categoria; o núcleo executa impostos, frete e notificação nessa ordem; cada regra só contribui quando seu contexto se aplica. | Verifique se está usando o `main.py` do microkernel. Compare `ORDEM_CATEGORIAS` em `nucleo.py`, os plugins registrados e os dados da fatura que ativam cada regra. |

Questões exploratórias:

1. Que contrato o núcleo conhece e quais detalhes ele deixa para os plugins?
2. Como a ordem por categoria afeta o total e a notificação?
3. Quais regras contribuem para uma fatura de SP, uma de RJ e uma de valor alto? Onde a saída mostra isso?

### Extensão reversível

Crie uma cópia antes de investigar. No PowerShell, a partir de `<raiz-do-clone>`:

```powershell
New-Item -ItemType Directory -Force entregas\unidade-1 | Out-Null
Copy-Item -Recurse codigos\cap01-estilos-fundamentais\1.4-microkernel entregas\unidade-1\microkernel
Set-Location entregas\unidade-1\microkernel
py main.py | Tee-Object -FilePath saida-antes.txt
```

No macOS/Linux:

```bash
mkdir -p entregas/unidade-1
cp -R codigos/cap01-estilos-fundamentais/1.4-microkernel entregas/unidade-1/microkernel
cd entregas/unidade-1/microkernel
python3 main.py | tee saida-antes.txt
```

Na cópia, modifique uma condição de uma regra, do registro ou de uma fatura e capture `saida-depois.txt`. Explique como a ordem de categorias e a contribuição das regras tornaram a mudança visível. Não existe uma modificação prescrita. Para retornar ao estado inicial, apague a cópia em `entregas/unidade-1/microkernel` e copie novamente o diretório original.

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
