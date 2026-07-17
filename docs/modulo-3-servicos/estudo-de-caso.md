# Estudo de caso: quando a fragmentação supera a autonomia

Considere a empresa fictícia Saúde Ágil. Após uma meta corporativa de “migrar para microsserviços”, o fluxo de autorização foi dividido em onze processos: cadastro, vínculo, vigência, plano, procedimento, regra contratual, rede, autorização, protocolo, notificação e auditoria. Cada processo tinha seu repositório e pipeline, mas uma única equipe mantinha todos.

## Sintomas

Adicionar uma nova regra de autorização exigia alterar contratos de quatro processos e implantar seis na mesma janela. Os serviços de vínculo, vigência e plano nunca eram escalados separadamente. Em incidentes, o time precisava correlacionar logs de vários componentes para descobrir que um campo havia mudado de significado. Uma tela fazia oito chamadas sequenciais e apresentava erros genéricos quando qualquer dependência atrasava.

Embora existissem muitos contêineres, a autonomia era pequena. O desenho possuía acoplamento de implantação, temporal, de contrato e organizacional. A separação física havia ocorrido antes de uma separação semântica estável.

## Diagnóstico por capacidades

O time mapeou linguagem, regras, mudanças conjuntas e propriedade dos dados. Vínculo, vigência, categoria de plano e regras contratuais formavam o contexto Elegibilidade: todas participavam da mesma decisão e mudavam sob políticas relacionadas. Protocolo e autorização pertenciam ao contexto Autorizações. Auditoria recebia fatos dos demais, mas não deveria controlar o fluxo nominal.

Esse mapa não obrigava três microsserviços. Ele indicava três limites lógicos. A equipe comparou alternativas:

- manter onze processos e investir em automação não corrigiria a fronteira incoerente;
- reunir tudo em um único módulo reduziria rede, mas misturaria autoridades;
- consolidar processos coevolutivos em macrosserviços com módulos internos preservaria limites e reduziria coordenação;
- extrair Auditoria assincronamente poderia isolar uma carga com comportamento distinto.

## Decisão

Saúde Ágil consolidou vínculo, vigência, plano e regra contratual no macrosserviço Elegibilidade. Internamente, módulos e testes de arquitetura impediram dependências circulares. O banco permaneceu sob uma credencial do macrosserviço, com schemas internos definidos pela equipe. Autorizações consumia uma API documentada e não acessava essas tabelas.

Auditoria passou a receber eventos depois que a equipe definiu identidade, retenção e repetição segura. A mudança não foi feita para “usar eventos”, mas para que uma indisponibilidade analítica não bloqueasse atendimento. O fluxo que precisava de decisão imediata permaneceu síncrono.

## Consequências observadas

A quantidade de implantações coordenadas caiu porque mudanças coesas voltaram à mesma unidade. A latência diminuiu ao substituir viagens de rede internas por chamadas locais. Por outro lado, o impacto potencial de uma implantação de Elegibilidade cresceu; testes, liberação gradual e rollback receberam maior atenção. A equipe não declarou sucesso pelo número de serviços. Acompanhou frequência de implantação independente, tempo de diagnóstico, taxa de erro nas dependências e alterações que atravessavam limites.

## Discussão de consistência

Antes da consolidação, processos diferentes escreviam estados que pareciam uma única autorização. Falhas deixavam registros contraditórios e não havia compensação. A equipe poderia introduzir uma SAGA, mas primeiro questionou se a distribuição era necessária. Ao reunir regras fortemente transacionais, manteve consistência local. Para o fluxo restante entre Elegibilidade e Autorizações, a consulta síncrona era deliberada: nenhuma autorização era gravada sem resposta válida.

Um painel gerencial precisava juntar autorização e dados agregados. Em vez de consulta direta a bancos operacionais, recebeu uma projeção atualizada por eventos. Essa decisão se aproxima de CQRS porque a leitura gerencial tem modelo e escala diferentes. A defasagem passou a ser exibida no painel. A equipe não separou todos os comandos e consultas do sistema.

## Evidência para revisar a decisão

A arquitetura seria revista se equipes diferentes assumissem partes do macrosserviço, se uma regra exigisse isolamento próprio, se cargas divergissem de forma material ou se a unidade voltasse a impedir entregas independentes. Também seria revista se a projeção não atendesse ao frescor necessário. Uma decisão arquitetural saudável contém seus sinais de validade e de expiração.

O caso ensina que consolidar não é fracassar e distribuir não é modernizar. O objetivo é alinhar coesão do software, propriedade do dado, comunicação e organização. Macroserviços podem ser uma etapa estável ou um estágio de evolução; monólito modular pode ser destino adequado; microsserviços podem ser necessários em limites específicos.

## Equivalências em Java e .NET

Uma consolidação em Java pode usar módulos Maven ou Gradle, pacotes de domínio e ArchUnit para impedir referências proibidas. Spring Modulith oferece recursos adicionais de verificação e eventos internos. Em .NET, projetos por módulo, modificadores de visibilidade e testes de dependência cumprem papel semelhante.

Em ambos, a consolidação deve preservar contratos externos durante migração. Um roteador pode encaminhar chamadas antigas ao novo macrosserviço enquanto consumidores são atualizados. O padrão de estrangulamento é uma estratégia de transição, não uma razão para manter indefinidamente duas fontes de verdade.
