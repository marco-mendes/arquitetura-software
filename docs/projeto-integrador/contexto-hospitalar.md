# Contexto hospitalar

Este caso descreve uma operação administrativa e tecnológica simplificada. A turma não precisa conhecer medicina: quando um detalhe clínico não estiver definido, trate-o apenas como informação protegida que precisa circular com significado, autorização e rastreabilidade.

## Situação

Um grupo hospitalar quer unificar cadastro, agenda e acompanhamento administrativo. Hoje, equipes consultam sistemas separados para confirmar dados do paciente, verificar elegibilidade no plano de saúde, solicitar autorização à operadora, encaminhar exames a um laboratório e acompanhar resultados. Retrabalho e falhas de integração dificultam o faturamento e a auditoria.

A nova plataforma hospitalar deve coordenar essa jornada sem assumir que operadoras e laboratórios usam a mesma tecnologia ou permanecem disponíveis continuamente.

## Atores e sistemas externos

| Ator ou sistema | Responsabilidade no caso |
| --- | --- |
| Paciente | Mantém dados cadastrais, solicita atendimento e acompanha notificações permitidas |
| Profissional | Consulta a agenda e registra solicitações necessárias ao fluxo administrativo |
| Equipe administrativa | Organiza agenda, corrige pendências e acompanha autorização e faturamento |
| Operadora do plano de saúde | Responde por elegibilidade, autorização e retorno administrativo |
| Laboratório | Recebe pedidos de exames, informa andamento e disponibiliza resultados |
| Equipe de auditoria | Verifica quem realizou uma ação, quando ocorreu e qual informação foi usada |
| Equipe de plataforma | Opera integrações, observa falhas e evolui contratos e serviços |

## Capacidades em escopo

- **Cadastro:** identificar paciente e profissional e manter dados administrativos essenciais.
- **Agenda:** consultar disponibilidade, solicitar, confirmar, remarcar e cancelar atendimento.
- **Elegibilidade:** consultar se o vínculo com o plano de saúde está apto para a solicitação.
- **Autorização:** enviar uma solicitação à operadora e acompanhar sua decisão.
- **Exames e resultados:** encaminhar pedido ao laboratório, acompanhar estado e receber o resultado protegido.
- **Faturamento:** consolidar registros administrativos necessários ao ciclo financeiro com a operadora.
- **Notificações:** informar mudanças relevantes sem expor dados sensíveis desnecessários.
- **Auditoria:** registrar ações e correlações suficientes para investigação e prestação de contas.

Não estão em escopo recomendar tratamento, interpretar resultados, modelar protocolos clínicos nem substituir sistemas especializados do plano de saúde ou do laboratório.

## Jornada de referência

1. O paciente é identificado e solicita um horário.
2. A plataforma confirma agenda e elegibilidade com a operadora.
3. Quando necessário, solicita autorização e acompanha a resposta.
4. O profissional registra um pedido de exame, que é encaminhado ao laboratório.
5. O laboratório informa andamento e disponibiliza o resultado.
6. A plataforma notifica os participantes autorizados, prepara dados de faturamento e preserva a trilha de auditoria.

Esse fluxo orienta a conversa, mas não prescreve uma arquitetura. Respostas lentas, indisponibilidade externa, mensagens repetidas e divergência de dados devem ser tratadas como forças de projeto.

## Restrições arquiteturais

- **Privacidade:** cada participante acessa somente os dados necessários à sua responsabilidade; registros e notificações evitam conteúdo sensível desnecessário.
- **Rastreabilidade:** solicitações, respostas, alterações e ações humanas são correlacionáveis de ponta a ponta.
- **Interoperabilidade:** contratos preservam significado mesmo quando plano de saúde, operadora, laboratório e hospital usam modelos diferentes.
- **Disponibilidade:** falhas externas não devem indisponibilizar capacidades hospitalares sem relação direta; modos degradados precisam ser explícitos.
- **Consistência:** estados transitórios e reconciliação são visíveis quando uma operação atravessa mais de um sistema.
- **Evolução:** contratos e decisões podem mudar sem exigir substituição simultânea de todos os participantes.

Converta essas restrições em cenários verificáveis com a página de [atributos de qualidade](../referencia/atributos-de-qualidade.md). Registre escolhas relevantes usando o [template de ADR](../referencia/template-adr.md).
