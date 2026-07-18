# Oficina do Módulo 1 com os códigos existentes

## Objetivo

Substituir a oficina genérica baseada em `laboratorios/plataforma-hospitalar` por uma prática executável com os três exemplos já existentes do Capítulo 1. O aluno deve executar, observar e relacionar a implementação a Camadas, Pipes and Filters e Microkernel.

## Fonte de código

Os exemplos existem sob a raiz do clone:

```text
<raiz-do-clone>/codigos/cap01-estilos-fundamentais/
├── 1.2-estilo-em-camadas/
├── 1.3-pipes-and-filters/
└── 1.4-microkernel/
```

Cada diretório contém `main.py` e não requer dependências externas: Python 3.10 ou superior é suficiente. O site deve apresentar tanto o caminho local quanto links para os arquivos no GitHub, a fim de o aluno entender o que abrir antes de executar.

## Percurso essencial

### Preparação

- Começar na raiz do clone `arquitetura-software`.
- Confirmar `Python 3.10+` com comandos equivalentes para Windows, macOS e Linux.
- Explicar que cada experimento é independente, imprime dados sintéticos no terminal e não exige ambiente virtual, Podman, Docker, pytest ou Structurizr.

### Experimento A — Camadas

- Diretório: `<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.2-estilo-em-camadas`.
- Executar `main.py`.
- Antes do comando, identificar `apresentacao.py`, `servicos.py`, `dominio.py` e `repositorios.py`, com links GitHub para cada arquivo.
- Observar o fluxo de agendamento e o conflito de agenda; relacionar a saída à responsabilidade de cada camada e à dependência por interface.
- Extensão reversível: alterar uma condição de agenda em cópia local, executar novamente, registrar efeito e desfazer a mudança.

### Experimento B — Pipes and Filters

- Diretório: `<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.3-pipes-and-filters`.
- Executar `main.py`.
- Antes do comando, identificar `framework.py`, `filtros/producer.py`, `filtros/testers.py`, `filtros/transformers.py` e `filtros/consumer.py`, com links GitHub.
- Observar registros descartados, transformações e ranking; relacionar a saída a producer, tester, transformer e consumer.
- Extensão reversível: ajustar um critério de triagem em cópia local, executar novamente, comparar evidência e desfazer.

### Experimento C — Microkernel

- Diretório: `<raiz-do-clone>/codigos/cap01-estilos-fundamentais/1.4-microkernel`.
- Executar `main.py`.
- Antes do comando, identificar `nucleo.py`, `plugins/impostos_sp.py`, `plugins/impostos_rj.py`, `plugins/frete.py` e `plugins/notificacao.py`, com links GitHub.
- Observar a ordem de aplicação de regras e a contribuição dos plugins; relacionar a saída ao núcleo, registro e contrato de extensão.
- Extensão reversível: criar ou alterar uma regra fiscal em cópia local, executar, registrar a evidência e desfazer.

## Roteiro de cada experimento

Cada bloco deve declarar: objetivo, artefato, caminho local, arquivos a abrir, pré-condição, comando por sistema operacional, saída a observar, perguntas de exploração e contingência quando `python` não for encontrado. Não usar referências vagas como “o laboratório” ou “rode isto”.

## Extensões e segurança

As extensões ocorrem em cópias locais, não exigem commit e não possuem resposta canônica. O estudante deve registrar a alteração, a saída anterior, a saída posterior e a restauração. Todos os dados dos exemplos são sintéticos.

## Qualidade e testes

- A oficina não pode orientar o aluno a usar `laboratorios/plataforma-hospitalar`, pytest, Podman ou Structurizr como prática principal desta unidade.
- Deve citar os três diretórios reais e `main.py` de cada exemplo.
- Deve conter links GitHub para os arquivos-chave de cada estilo.
- Deve declarar Python 3.10+ e comandos equivalentes Windows/macOS/Linux.
- Os testes do Módulo 1 devem proteger essas referências e os links relativos/externos válidos.
- `python -m unittest tests.test_module_one -v`, `python scripts/validate_content.py --module modulo-1-visao-geral` e `python -m mkdocs build --strict` precisam passar.
