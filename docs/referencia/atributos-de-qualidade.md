# Atributos de qualidade

Atributos de qualidade tornam expectativas não funcionais verificáveis. Uma afirmação útil descreve fonte do estímulo, estímulo, ambiente, elemento afetado, resposta e medida da resposta.

| Atributo | Pergunta de projeto | Exemplo de medida |
| --- | --- | --- |
| Desempenho | A resposta chega no tempo necessário sob carga conhecida? | Latência por percentil e vazão em um intervalo |
| Disponibilidade | A capacidade permanece utilizável diante de uma falha? | Tempo de recuperação e proporção de solicitações bem-sucedidas |
| Segurança | Identidade, dados e ações recebem proteção adequada? | Tentativas indevidas bloqueadas e eventos auditáveis |
| Modificabilidade | Uma mudança pode ser localizada e implantada com risco controlado? | Elementos alterados, esforço e tempo de implantação |
| Testabilidade | O comportamento pode ser controlado e observado em teste? | Tempo de preparação, isolamento e diagnóstico de falha |
| Interoperabilidade | Sistemas distintos trocam informações com significado preservado? | Conformidade de contrato e erros de transformação |
| Operabilidade | A equipe consegue compreender e controlar o sistema em execução? | Tempo de detecção, diagnóstico e recuperação |

## Como usar na decisão

1. Escreva um cenário concreto para o atributo relevante.
2. Compare alternativas usando a mesma medida e o mesmo ambiente.
3. Registre tensões: melhorar disponibilidade pode aumentar complexidade; reduzir latência pode alterar consistência ou custo operacional.
4. Defina uma evidência que permita revisar a decisão depois.

O nome do atributo sozinho não determina uma arquitetura. Cenário, prioridade e medida conectam a necessidade à decisão.
