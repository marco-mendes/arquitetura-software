# Oficina de ferramentas: comparar, observar e registrar

Esta oficina é local e usa ferramentas de código aberto. Python executa a comparação explícita; pytest preserva o comportamento esperado; Structurizr Lite apresenta a estrutura como texto versionável. Reserve aproximadamente setenta minutos para a trilha essencial e mais quarenta para exploração.

Use somente dados sintéticos. O laboratório trata decisões administrativas e não precisa de informações reais de pacientes, profissionais ou parceiros.

## O que existe antes de você abrir o terminal

Você trabalhará no repositório desta disciplina, dentro da pasta `laboratorios/plataforma-hospitalar`. Ela contém uma aplicação didática local, e não uma integração com hospital, plano de saúde ou banco de dados real. Nesta unidade, o artefato principal é `src/hospital/estilos.py`: uma tabela legível que relaciona quatro estilos a forças, limites e evidências possíveis. A função `comparar_estilos` recebe prioridades declaradas, ordena alternativas compatíveis e devolve a explicação usada nessa ordenação.

O arquivo `tests/test_estilos.py` não mede a qualidade de uma arquitetura em produção. Ele verifica o **contrato do comparador**: se alternativas retornam força, limite e evidência, e se prioridades distintas produzem comparações diferentes. Você vai executar o teste, alterar um cenário local e interpretar o que mudou. A condição inicial verificável é simples: a pasta do repositório existe no seu computador e você consegue abrir um terminal nela. Antes de instalar qualquer coisa, localize a raiz do repositório e entre na pasta do laboratório:

```text
arquitetura-software/
└── laboratorios/
    └── plataforma-hospitalar/   ← execute os comandos desta oficina aqui
```

Ao final da preparação, a condição de início da prática será: existe uma pasta `.venv`, `python --version` mostra o interpretador do ambiente virtual e `python -m pytest tests/test_estilos.py -q` termina com `3 passed`.

## Ferramenta

Python executa `comparar_estilos`; pytest verifica seu contrato; Structurizr Lite e Podman renderizam o modelo; o editor registra o ADR. Resultado verde não substitui interpretação.

## Pré-requisitos

**Objetivo**

Preparar um ambiente descartável capaz de executar o comparador de estilos, seus testes e, na extensão, um modelo de arquitetura.

**Pré-requisito**

Tenha o repositório local, terminal, editor e permissão para instalar pacotes. Execute em `laboratorios/plataforma-hospitalar`.

**O que cada verificação significa**

Ao final, `python --version`, `python -m pytest --version` e `podman --version` mostram versões. Em macOS/Linux, use `python3` antes da ativação; Podman é só para extensão.

## Instalação

### Windows

Antes de qualquer `Set-Location` relativo, o terminal começa na raiz do clone `arquitetura-software`.

Abra PowerShell. Instale Python e Podman com o gerenciador do Windows:

```powershell
winget install --exact --id Python.Python.3.12
winget install --exact --id RedHat.Podman
```

Feche e abra PowerShell para atualizar os comandos disponíveis. Inicie a máquina Linux usada pelo Podman:

```powershell
podman machine init
podman machine start
```

Se a máquina já existir, ignore apenas a mensagem de existência e execute `podman machine start`. Entre no laboratório e crie o ambiente, sem ativá-lo ainda:

```powershell
Set-Location laboratorios\plataforma-hospitalar
py -m venv .venv
```

Se a execução de scripts for bloqueada nesse computador, aplique agora a contingência somente à sessão atual, antes de qualquer ativação ou instalação:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

O escopo `Process` termina ao fechar PowerShell; se bloqueado, use a rota sem ativação.

#### Ativação opcional

Tente ativar a venv executando somente o script de ativação:

```powershell
.venv\Scripts\Activate.ps1
```

Confirme `(.venv)` no prompt; se não aparecer, use a rota sem ativação.

#### Rota sem ativação e continuação comum

Com ou sem `(.venv)` no prompt, continue pelos mesmos comandos explícitos. Assim, a instalação e os testes não dependem da ativação nem do Python global:

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m pytest --version
.venv\Scripts\python.exe -m pytest tests -q
.venv\Scripts\python.exe -m pytest tests/test_estilos.py -q
podman --version
```

Os demais comandos PowerShell usam `.venv\Scripts\python.exe`, sem Python global.

### macOS

Antes de qualquer `cd` relativo, o terminal começa na raiz do clone `arquitetura-software`.

Abra Terminal. Com Homebrew disponível, instale Python e Podman, inicie a máquina e prepare o workspace:

```bash
brew install python@3.12 podman
podman machine init
podman machine start
cd laboratorios/plataforma-hospitalar
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python --version
python -m pytest --version
podman --version
```

Se a máquina já existir, execute só `podman machine start`; se necessário, use `python3`.

### Linux

Antes de qualquer `cd` relativo, o terminal começa na raiz do clone `arquitetura-software`.

Os comandos abaixo usam Debian ou Ubuntu. Em outra distribuição, instale os pacotes equivalentes pelo gerenciador do sistema.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip podman
cd laboratorios/plataforma-hospitalar
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python --version
python -m pytest --version
podman --version
```

Em Linux, não execute `podman machine init`.

## Preparação do laboratório

### Essencial em aula

**Execute**

Confirme a pasta e `(.venv)`. O primeiro arquivo contém a tabela; o segundo, as verificações:

```text
src/hospital/estilos.py
tests/test_estilos.py
```

Crie a pasta `evidencias`. No PowerShell:

```powershell
New-Item -ItemType Directory -Force evidencias
```

Em macOS ou Linux:

```bash
mkdir -p evidencias
```

Em `src/hospital/estilos.py`, `_ESTILOS` declara estilo, força, limite e evidência; a função apenas filtra e ordena prioridades.

**Observe**

Saída é uma lista com `estilo`, `forcas`, `limites` e `evidencias`. `evidencias` guarda suas saídas, sem alterar código.

### Exploração em dupla

**Execute**

Crie `evidencias/comparacao.py` com o conteúdo abaixo:

```python
from pprint import pprint

from hospital.estilos import comparar_estilos


cenario = {
    "dominio": "triagem administrativa",
    "prioridades": ["modificabilidade", "extensibilidade"],
}

pprint(comparar_estilos(cenario))
```

Uma pessoa descreve a força; outra confere limite e evidência. Troquem papéis.

**Compare**

Antes de editar, prevejam o primeiro estilo e registrem sem alterar o teste.

### Extensão

**Execute**

Crie a pasta `structurizr` e, dentro dela, o arquivo `workspace.dsl`:

```structurizr
workspace "Plataforma hospitalar" "Estrutura inicial do módulo 1" {
    model {
        equipe = person "Equipe administrativa"
        plataforma = softwareSystem "Plataforma hospitalar" {
            aplicacao = container "Aplicação hospitalar" "Monólito modular implantado como uma unidade" "Python 3.12 e FastAPI" {
                agenda = component "Agenda" "Módulo em camadas para reservas consistentes" "Python" {
                    tags "Camadas"
                }
                triagem = component "Triagem" "Núcleo administrativo com extensões por plugin" "Python" {
                    tags "Microkernel"
                }
                faturamento = component "Faturamento" "Módulo com fluxo de validação e transformação" "Python" {
                    tags "Pipes and filters"
                }
                auditoria = component "Auditoria" "Módulo de correlação administrativa" "Python" {
                    tags "Módulo"
                }
            }
        }
        equipe -> agenda "Solicita e remarca horários" "HTTPS/JSON"
        agenda -> auditoria "Registra alterações"
        triagem -> auditoria "Registra etapas"
        faturamento -> auditoria "Registra rejeições"
    }
    views {
        container plataforma "Aplicacao" {
            include *
            autolayout lr
        }
        component aplicacao "Modulos" {
            include *
            autolayout lr
        }
        styles {
            element "Person" {
                shape person
            }
        }
    }
}
```

O arquivo modela uma única aplicação implantável, coerente com o monólito modular decidido no estudo de caso. Agenda, Triagem, Faturamento e Auditoria são componentes internos, não unidades de implantação. O campo de tecnologia contém apenas mecanismos concretos (`Python 3.12 e FastAPI` ou `Python`); os estilos aparecem nas descrições e tags. O arquivo usa nomes e relações, não coordenadas fixas, e pode ser versionado como qualquer outro texto.

## Execução

Contexto de terminal: abra na raiz `arquitetura-software`, entre em `laboratorios/plataforma-hospitalar` e mantenha essa pasta nos blocos seguintes.

### Essencial em aula

**Execute**

Rode primeiro toda a suíte. Em seguida, execute `test_estilos.py` e capture em `evidencias/testes-estilos.txt`.

#### Windows / PowerShell — captura

```powershell
.venv\Scripts\python.exe -m pytest tests -q
.venv\Scripts\python.exe -m pytest tests/test_estilos.py -q 2>&1 | Tee-Object -FilePath evidencias\testes-estilos.txt
```

#### macOS ou Linux — captura

```bash
python -m pytest tests -q
python -m pytest tests/test_estilos.py -q 2>&1 | tee evidencias/testes-estilos.txt
```

**Observe**

O teste `test_alternativas_explicam_forcas_limites_e_evidencias` impede respostas vazias. O terceiro teste compara duas prioridades distintivas: modificabilidade com extensibilidade, depois throughput com processamento incremental. Leia o nome do teste e as asserções antes de concluir o que foi demonstrado.

### Exploração em dupla

**Execute**

No mesmo terminal aberto na raiz e posicionado no laboratório, execute o roteiro e capture a primeira saída.

#### Windows / PowerShell — captura

```powershell
.venv\Scripts\python.exe evidencias\comparacao.py 2>&1 | Tee-Object -FilePath evidencias\comparacao-modificabilidade.txt
```

#### macOS ou Linux — captura

```bash
python evidencias/comparacao.py 2>&1 | tee evidencias/comparacao-modificabilidade.txt
```

Depois altere somente o domínio e as prioridades:

```python
cenario = {
    "dominio": "ingestão em fluxo",
    "prioridades": ["throughput", "processamento incremental"],
}
```

No mesmo diretório, execute novamente e capture outro arquivo.

#### Windows / PowerShell — captura

```powershell
.venv\Scripts\python.exe evidencias\comparacao.py 2>&1 | Tee-Object -FilePath evidencias\comparacao-fluxo.txt
```

#### macOS ou Linux — captura

```bash
python evidencias/comparacao.py 2>&1 | tee evidencias/comparacao-fluxo.txt
```

Não mude a tabela para forçar uma preferência. A alteração deve representar novas forças do contexto.

**Compare**

Na primeira execução, microkernel combina modificabilidade e extensibilidade, com duas evidências correspondentes. Na segunda, pipes and filters combina throughput e processamento incremental. Compare também os limites; mudar apenas o nome vencedor produziria uma análise pobre.

### Extensão

**Execute**

Abra outro terminal em `laboratorios/plataforma-hospitalar`. No PowerShell, descubra o caminho completo e inicie Structurizr Lite:

```powershell
$workspace = (Resolve-Path .\structurizr).Path
podman run --rm --interactive --tty --publish 8080:8080 --volume "${workspace}:/usr/local/structurizr" docker.io/structurizr/lite
```

Em macOS ou Linux:

```bash
podman run --rm --interactive --tty --publish 8080:8080 --volume "$PWD/structurizr:/usr/local/structurizr:Z" docker.io/structurizr/lite
```

Abra `http://localhost:8080` no navegador. Na visão de containers, localize uma única Aplicação hospitalar. Na visão de componentes, localize os quatro módulos e os conectores com Auditoria. Confira que tecnologias e estilos ocupam campos diferentes.

**Observe**

Altere a descrição de `Triagem`, salve `workspace.dsl` e atualize o navegador. A mudança deve aparecer sem reconstruir uma imagem. Isso demonstra modelo como código, não adequação do estilo. Copie então a versão executada para as evidências. No PowerShell:

```powershell
Copy-Item .\structurizr\workspace.dsl .\evidencias\workspace.dsl
```

Em macOS ou Linux:

```bash
cp structurizr/workspace.dsl evidencias/workspace.dsl
```

## Resultado esperado

A suíte completa do laboratório possui quatro testes e deve encerrar sem falhas:

```text
....                                                                     [100%]
4 passed
```

Uma execução típica do arquivo focado possui três testes:

```text
...                                                                      [100%]
3 passed
```

Para modificabilidade e extensibilidade, a primeira alternativa é `microkernel`; para throughput e processamento incremental, `pipes and filters`. Structurizr Lite renderiza uma aplicação com quatro componentes internos.

## Interpretação

**Observe**

O comparador usa conhecimento declarado; força ausente revela limite do instrumento.

**Compare**

Teste, execução e diagrama são complementares; nenhum mede carga real ou prova segurança.

### Questões exploratórias

1. Por que throughput diferencia faturamento de agenda neste cenário?
2. Qual limite do microkernel teria maior impacto se os plugins compartilhassem estado?
3. Que teste impediria um módulo do monólito de importar detalhes internos de outro?
4. Qual evento levaria a substituir o ADR em vez de apenas atualizar o diagrama?

Preencha um mini-ADR. Copie o modelo para `evidencias/ADR-001-estilo-inicial.md`. No PowerShell:

```powershell
Copy-Item ..\..\docs\referencia\template-adr.md evidencias\ADR-001-estilo-inicial.md
```

Em macOS ou Linux:

```bash
cp ../../docs/referencia/template-adr.md evidencias/ADR-001-estilo-inicial.md
```

Registre contexto, duas alternativas, decisão provisória, uma consequência favorável, uma desfavorável, o resultado do teste e um gatilho de revisão.

## Limpeza e contingência

**Execute**

Interrompa Structurizr Lite com `Ctrl+C`; `--rm` remove o contêiner de execução. Preserve `evidencias`, pois ela contém a entrega. Para sair do ambiente virtual, execute:

```bash
deactivate
```

Se precisar reconstruir completamente o ambiente, remova apenas `.venv` e repita a instalação. No PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
```

Em macOS ou Linux:

```bash
rm -rf .venv
```

Se a porta 8080 estiver ocupada, troque `--publish 8080:8080` por `--publish 8081:8080` e abra `http://localhost:8081`. Se `hospital` não puder ser importado, confirme a pasta atual e repita `python -m pip install -e ".[dev]"`. Se o modelo não renderizar, leia a linha indicada pelo Structurizr Lite e compare chaves, nomes e relações com o arquivo fornecido.

## Evidência a entregar

**Objetivo**

Demonstrar uma cadeia curta entre força, comparação, estrutura e decisão.

**Execute**

Entregue a pasta `evidencias` com exatamente os artefatos criados no roteiro: `comparacao.py`, `comparacao-modificabilidade.txt`, `comparacao-fluxo.txt`, `testes-estilos.txt`, `workspace.dsl` e `ADR-001-estilo-inicial.md`. Os arquivos de texto preservam os comandos observados; `workspace.dsl` preserva o modelo que foi renderizado.

**Compare**

Revise se o ADR cita a força alterada, se a consequência desfavorável aparece e se a evidência realmente observa a promessa. Declare limites: a oficina usa uma tabela didática e dados sintéticos. A entrega deve permitir que outra pessoa repita os comandos e compreenda por que a decisão permanece provisória.
