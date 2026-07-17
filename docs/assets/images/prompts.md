# Prompts dos infográficos

Os infográficos deste diretório foram gerados para apoiar leitura e discussão em sala. Eles não substituem o texto alternativo e a leitura textual imediatamente abaixo de cada figura nas páginas conceituais.

## Prompt-base

> Infográfico acadêmico editorial, proporção 16:9, fundo claro, azul-marinho `#16243A`, cobalto `#254DB8`, ciano `#5FC0D1` e âmbar `#F2B84B`, texto curto em português brasileiro, hierarquia legível, sem logotipos comerciais, sem aparência fotográfica.

## Variações por arquivo

| Arquivo | Complemento do prompt |
| --- | --- |
| `capa-arquitetura-software.png` | Capa que sintetiza a progressão dos seis encontros: estilos, APIs, serviços, governança, eventos e nuvem, convergindo para uma plataforma hospitalar. |
| `m01-mapa-estilos.png` | Mapa comparativo de estilos arquiteturais: camadas, pipes e filtros, microkernel e monólito modular; explicitar forças de modificabilidade, vazão e extensibilidade. |
| `m02-anatomia-api.png` | Anatomia de contrato de API: consumidor, contrato OpenAPI, serviço, requisição e resposta `202 Accepted` com `Location`. |
| `m03-fronteiras-servicos.png` | Limites e dados de serviços: Elegibilidade e Exames, contratos de API, banco por serviço e acesso direto ao banco alheio explicitamente bloqueado. |
| `m04-governanca-observavel.png` | Gateway, política, identificador de correlação, serviço, logs estruturados, traces e medida de limite; não usar dado clínico identificável. |
| `m05-fluxo-eventos.png` | Publicação de resultado laboratorial, broker, consumidor de Faturamento, verificação de idempotência e dead-letter queue para mensagem inválida. |
| `m06-resiliencia-nuvem.png` | Regiões, cluster local, duas réplicas, probes de readiness e liveness, atualização gradual e rollback. |

Os textos inseridos nas imagens são deliberadamente curtos. Definições, limites e consequências ficam no conteúdo em Markdown, que pode ser pesquisado, ampliado e lido por tecnologias assistivas.
