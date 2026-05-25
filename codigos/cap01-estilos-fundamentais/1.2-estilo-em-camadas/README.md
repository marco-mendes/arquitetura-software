# 1.2 — Estilo em Camadas: Sistema de Agendamento de Clínica

Demonstração completa do estilo arquitetural em Camadas com DDD aplicado a um
sistema de agendamento de consultas médicas.

## Conceitos demonstrados

- Separação em Camadas: Domínio → Dados → Negócios → Apresentação
- **OCP na camada de dados:** repositórios são interfaces (ABC); as implementações
  em memória podem ser trocadas por PostgreSQL sem alterar a camada de negócios
- **DDD:** Value Objects (`CPF`, `Horario`), Entidades com invariantes (`Consulta`),
  Repositórios como abstração de persistência
- **Controllers simulados:** `AgendaController` imita handlers HTTP sem framework

## Execução

```bash
python main.py
```

Sem dependências externas — apenas Python 3.10+.

## Estrutura

```
dominio.py      ← Value Objects, Entidades, interfaces de Repositório
repositorios.py ← Implementações em memória (trocáveis por BD real)
servicos.py     ← Regras de negócio: conflito de agenda, validação
apresentacao.py ← Controllers simulados (camada HTTP)
main.py         ← Demonstração ponta a ponta
```

## Saída esperada

O programa demonstra: agendamentos válidos, conflito de horário (HTTP 409),
cancelamento, realização de consulta, relatório de agenda e histórico de paciente.
