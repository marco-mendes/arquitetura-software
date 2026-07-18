# Task 6 — Recuperação editorial da Unidade 4

## Escopo entregue

- Reposicionei governança como contrato, política, fronteira, mediação e evidência verificável, sem apresentar gateway ou observabilidade como sinônimos da arquitetura.
- Explicitei versionamento, mediação e rastreabilidade em `conceitos.md` e `padroes-e-decisoes.md`; o gateway medeia controles comuns, enquanto Elegibilidade permanece dona da semântica clínica.
- Atualizei o caso e o exemplo para ligar contrato, configuração declarativa e execução observada, delimitando o que rota, `429`, `correlation_id` e trace comprovam — e o que não comprovam.
- A oficina agora nomeia, antes dos comandos, a demonstração **Plataforma Hospitalar Governada**, os arquivos `infra/compose.governanca.yml`, `infra/kong/kong.yml` e `infra/observabilidade/otel-collector.yml`, os cinco serviços, estados de preparação e as evidências esperadas.
- Mantive Kong, OpenTelemetry e Jaeger como implementação local e descartável da oficina; não são apresentados como definição de governança.
- Reescrevi Recordar e Compreender como perguntas numeradas com um bloco `<details>` por resposta. Aplicar, Analisar, Avaliar e Criar passaram a ter os nove campos do contrato de exercício, caminhos de entrega a partir da raiz do clone e a política, arquivo, serviço e saída observável explicitados.
- Acrescentei texto alternativo, legenda em itálico iniciada por *Figura* e leitura textual aos Mermaid da unidade.

## TDD

1. Adicionei `test_unit_four_explains_governance_as_contract_policy_and_evidence` a `tests/test_module_four.py`.
2. O ciclo vermelho foi executado com `python -m unittest tests.test_module_four.ModuleFourTest.test_unit_four_explains_governance_as_contract_policy_and_evidence -v`.
3. A falha esperada indicou a ausência literal de `versionamento` no corpus combinado e, após essa correção, também cobriu `mediação` e `rastreabilidade`.
4. A integração editorial fez o teste passar junto com os contratos existentes da unidade.
5. Uma verificação intermediária encontrou 8.720 palavras, acima do máximo de 8.500; a causa foi redundância entre leituras textuais de Mermaid. Consolidei cada leitura em uma única equivalência textual e revalidei, sem remover informação pedagógica exigida.

## Verificações finais

| Comando | Resultado |
| --- | --- |
| `python -m unittest tests.test_module_four tests.test_editorial_recovery -v` | 10 testes aprovados |
| `python scripts/validate_content.py --module modulo-4-governanca` | concluído sem erros |
| `docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml config --quiet` | configuração válida (código zero) |
| `git diff --check` | sem erros de espaço em branco |

## Limites e preocupações

- O Compose foi validado estaticamente; a tarefa não inicia contêineres. A oficina separa essa validação da evidência de rota, `429`, correlação e trace, que exigem execução local real.
- O rate limiting local do Kong é demonstrativo para uma instância e não representa limite distribuído entre réplicas.
- Jaeger local não deve receber dados clínicos nem representar retenção, auditoria ou conformidade de produção.
- A unidade permanece na faixa editorial de 5.000 a 8.500 palavras validada pelos testes.

## Correção da revisão editorial

- Em **Analisar**, substituí a atribuição incorreta ao Collector: `infra/kong/kong.yml` extrai e injeta o `traceparent` W3C no gateway, enquanto `src/hospital/telemetria.py` extrai o contexto recebido em Elegibilidade e cria o span filho. O Collector continua apenas recebendo, processando em lote e exportando a telemetria.
- Os quatro exercícios avançados agora indicam a entrega desde `<raiz-do-clone>/entregas/...`.
- O resumo inicial da oficina passou a antecipar observação por `ps`, HTTP, logs e API Jaeger, além do encerramento com `docker compose -f infra/compose.governanca.yml down -v`.
- Restaurei a numeração única das figuras: o Mermaid do estudo de caso passou a ser **Figura 6**; não havia referências cruzadas a atualizar.
- Para manter o teto editorial, removi redundâncias locais sem retirar instruções, critérios ou evidências da oficina. A contagem final é de 8.499 palavras.

| Comando | Resultado |
| --- | --- |
| `python -m unittest tests.test_module_four tests.test_editorial_recovery -v` | 10 testes aprovados |
| `git diff --check` | sem erros de espaço em branco |
