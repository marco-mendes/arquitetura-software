# Workspace da plataforma hospitalar

Este workspace é a base executável comum dos seis encontros. Neste ponto, ele contém apenas o pacote Python `hospital` e um teste de importação. APIs, serviços, eventos e infraestrutura serão acrescentados pelos módulos sem criar projetos paralelos.

Requer Python 3.11 ou mais recente. Execute os comandos dentro desta pasta.

## Preparação

### PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest tests
```

### Shells POSIX

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest tests
```

## Resultado esperado

O teste confirma que o pacote `hospital` pode ser importado a partir do ambiente editável. O modo editável faz com que alterações futuras em `src/hospital/` sejam usadas sem reinstalar o projeto.

## Estrutura inicial

```text
plataforma-hospitalar/
├── pyproject.toml
├── src/
│   └── hospital/
│       └── __init__.py
└── tests/
    └── test_package.py
```
