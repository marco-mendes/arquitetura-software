# Task 5 — Relatório de recuperação da Unidade 3

## Escopo entregue

- Recuperada a narrativa da Unidade 3 em `docs/modulo-3-servicos/`, mantendo o caso hospitalar como fio condutor para fronteiras, dados, falhas, consistência e evolução.
- Integrados persistência poliglota, consistência eventual, CAP, SAGA, CQRS, event sourcing, chassi arquitetural e padrão estrangulador como respostas condicionais, não como catálogo de adoção.
- Acrescentada uma leitura de Netflix e Uber por consequências de escala, isolamento e reversibilidade, sem copiar a topologia de fornecedores.
- Convertidos Recordar e Compreender em 18 perguntas com resposta expansível individual.
- Reescritas Aplicar, Analisar, Avaliar e Criar com os nove campos do contrato e caminhos de entrega inequívocos a partir da raiz do clone, em `entregas/modulo-3/`.
- Reestruturada a oficina para identificar, antes de cada comando Compose, a demonstração local, arquivos, serviços, bases, estado, comportamento/health checks, portas e encerramento.
- Complementados os três Mermaid alterados com texto alternativo, legenda de Figura e leitura textual.

## TDD

1. Adicionado `test_unit_three_covers_distributed_service_consequences` a `tests/test_module_three.py`.
2. Ciclo vermelho executado com `python -m unittest tests.test_module_three.ModuleThreeTest.test_unit_three_covers_distributed_service_consequences -v`.
3. A falha esperada ocorreu por ausência de `persistência` no corpus da Unidade 3.
4. Após a integração editorial, o teste passou junto com a suíte da unidade e os testes de recuperação.

## Verificações finais

| Comando | Resultado |
| --- | --- |
| `python -m unittest tests.test_module_three tests.test_editorial_recovery -v` | 14 testes aprovados |
| `python scripts/validate_content.py --module modulo-3-servicos` | concluído sem erros |
| `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml config --quiet` | configuração válida (código zero) |
| Validação direta dos contratos de exercício | respostas expansíveis e nove campos sem erros |
| `git diff --check` | sem erros de espaço em branco |

## Limites e observações

- O Compose foi validado estaticamente; a Task 5 não inicia contêineres. A oficina deixa claro que health checks só podem ser afirmados após execução local real.
- A Unidade 3 contém 8.496 palavras, dentro da faixa exigida de 5.000 a 8.500.
- Nenhuma alteração foi feita nos serviços ou na infraestrutura: o trabalho é editorial e de teste de regressão de conteúdo.

## Correção da revisão P1 — trilha PowerShell

- A oficina passou a identificar explicitamente os blocos PowerShell de health check, criação bem-sucedida (`201`) e indisponibilidade (`503`).
- Esses blocos usam `$env:ELEGIBILIDADE_PORT` e `$env:EXAMES_PORT`; usam `curl.exe` para evitar que o alias PowerShell `curl` acione `Invoke-WebRequest` e altere a interpretação dos parâmetros cURL.
- Foi adicionado `test_workshop_has_powershell_http_calls_with_overrideable_ports`, que exige os dois health checks e duas chamadas POST com a sintaxe PowerShell.

| Verificação da correção | Resultado |
| --- | --- |
| Teste vermelho: `python -m unittest tests.test_module_three.ModuleThreeTest.test_workshop_has_powershell_http_calls_with_overrideable_ports -v` | falhou como esperado antes da documentação dos comandos PowerShell |
| `python -m unittest tests.test_module_three tests.test_editorial_recovery -v` | 15 testes aprovados |
| `git diff --check` | sem erros de espaço em branco |
