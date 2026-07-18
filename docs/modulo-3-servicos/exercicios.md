# Exercícios: decidir antes de distribuir

Tente responder antes de abrir cada feedback. Nas atividades avançadas não há gabarito: os nove campos tornam explícitos o contexto, a entrega e a forma de avaliar uma decisão justificável.

## Recordar

1. Defina capacidade de negócio e dê um exemplo hospitalar.

<details>
<summary>Ver resposta</summary>

É um resultado que a organização sabe produzir, como verificar elegibilidade.
</details>

2. Diferencie bounded context de microsserviço em duas frases.

<details>
<summary>Ver resposta</summary>

Bounded context delimita significado. Microsserviço é uma possível implantação física dessa fronteira.
</details>

3. Liste quatro formas de acoplamento apresentadas no módulo.

<details>
<summary>Ver resposta</summary>

Contrato, tempo, dados, implantação e organização.
</details>

4. Explique o que banco por serviço proíbe.

<details>
<summary>Ver resposta</summary>

Proíbe acesso direto de outro serviço; a integração usa contrato, evento ou cópia projetada.
</details>

5. Nomeie as três formas de implantação comparadas.

<details>
<summary>Ver resposta</summary>

Monólito modular, macrosserviço e microsserviço.
</details>

6. Defina falha parcial.

<details>
<summary>Ver resposta</summary>

Uma parte segue saudável enquanto outra indisponibilidade impede uma capacidade.
</details>

7. Indique o papel de timeout em uma chamada síncrona.

<details>
<summary>Ver resposta</summary>

Limita a espera pela dependência e impede que a lentidão se espalhe.
</details>

8. Declare a condição em que CAP força uma escolha.

<details>
<summary>Ver resposta</summary>

Durante uma partição: preservar consistência ou responder aceitando divergência.
</details>

9. Resuma SAGA sem usar a expressão “rollback global”.

<details>
<summary>Ver resposta</summary>

Coordena transações locais e pode exigir compensações para efeitos confirmados.
</details>

10. Resuma CQRS sem pressupor bancos separados.

<details>
<summary>Ver resposta</summary>

Separa comando e consulta quando suas necessidades diferem; pode começar no mesmo processo.
</details>

## Compreender

1. Explique por que mover duas funções para processos diferentes não reduz automaticamente acoplamento.

<details>
<summary>Ver resposta</summary>

A chamada vira contrato e rede; se mudanças continuam conjuntas, o acoplamento só mudou de forma.
</details>

2. Descreva como alta coesão pode ser prejudicada por serviços pequenos demais.

<details>
<summary>Ver resposta</summary>

Regras que mudam juntas passam a exigir contratos e implantações coordenadas.
</details>

3. Compare propriedade de dados com localização física do banco.

<details>
<summary>Ver resposta</summary>

Propriedade define autoridade; localização pode ser schema, instância ou servidor e só protege com permissões reais.
</details>

4. Explique por que `503 dependencia_indisponivel` comunica melhor a falha do laboratório do que um `500` genérico.

<details>
<summary>Ver resposta</summary>

Expõe uma dependência indisponível sem atribuir a Exames um erro interno genérico.
</details>

5. Mostre por que consistência eventual ainda exige regras de convergência.

<details>
<summary>Ver resposta</summary>

Exige identidade, ordenação quando necessária, idempotência, repetição e reconciliação para convergir.
</details>

6. Dê um cenário em que monólito modular seja preferível e outro em que implantação independente seja necessária.

<details>
<summary>Ver resposta</summary>

Mudanças conjuntas e transação comum favorecem módulos; equipes e cargas independentes podem justificar serviços.
</details>

7. Explique por que uma compensação de SAGA não apaga fatos já observados.

<details>
<summary>Ver resposta</summary>

O efeito pode ter sido observado; compensar cria outro fato, não apaga o anterior.
</details>

8. Descreva a diferença de propósito entre SAGA e CQRS.

<details>
<summary>Ver resposta</summary>

SAGA coordena mudança distribuída; CQRS separa leitura e escrita. Um não exige o outro.
</details>

## Aplicar

### Delimitar o fluxo de laudos

**Objetivo**

Propor uma primeira fronteira lógica que preserve a transação clínica e permita notificação atrasada.

**Situação**

Uma clínica possui um sistema único. Laudos recebe o resultado técnico, aplica assinatura profissional e publica o documento; Notificações envia aviso depois da publicação. Ambos usam tabelas sem proprietário e a equipe quer melhorar limites sem distribuir agora.

**Seu papel**

Você é a pessoa arquiteta responsável pela proposta inicial.

**Artefato que você irá usar**

Crie `entregas/modulo-3/aplicar-laudos.md`, a partir da raiz do clone, e use as descrições de `docs/modulo-3-servicos/conceitos.md` e `docs/modulo-3-servicos/padroes-e-decisoes.md`.

**Antes de executar**

Crie o diretório `entregas/modulo-3/`; não é necessário iniciar serviços nem alterar o laboratório. Considere uma equipe, implantação semanal conjunta, transação local para assinatura/publicação, atraso aceitável de cinco minutos para avisos e volume estável.

**Insumos disponíveis**

As capacidades, restrições e referências indicadas acima.

**Como conduzir**

**O que fazer**

1. Nomeie contexts e termos centrais.
2. Aloque tabelas e operações a um proprietário.
3. Desenhe interfaces internas e dependências permitidas.
4. Indique um evento interno e sua semântica.
5. Escolha a forma de implantação inicial e um sinal de revisão.

**Evidência esperada**

O artefato mostra capacidade, regra, dono do dado, direção de dependência e a razão contextual da escolha.

**Entrega esperada**

Envie o arquivo `entregas/modulo-3/aplicar-laudos.md` com uma página, um mapa de contexto, duas guardas automatizáveis, uma suposição e um risco.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Limites alinhados às capacidades e invariantes | 30% | Evidência: capacidade e regra; insuficiente: limite técnico arbitrário. |
| Propriedade de dados explícita | 25% | Evidência: dono do dado; insuficiente: banco compartilhado sem regra. |
| Dependências e contratos coerentes | 20% | Evidência: direção e contrato; insuficiente: acesso direto oculto. |
| Decisão ligada aos insumos | 15% | Evidência: insumo citado; insuficiente: decisão sem contexto. |
| Riscos e sinais de revisão | 10% | Evidência: risco e sinal; insuficiente: revisão sem condição. |

## Analisar

### Diagnosticar um monólito distribuído

**Objetivo**

Separar fatos, inferências e hipóteses ao analisar dependências que parecem serviços autônomos.

**Situação**

Cadastro, Agenda, Atendimento e Faturamento usam o mesmo schema. Atendimento chama os três em sequência; uma mudança de campo exige quatro implantações. Cada serviço anuncia 99,9% de disponibilidade, mas o fluxo tem incidentes frequentes.

**Seu papel**

Você lidera a análise antes de qualquer reestruturação.

**Artefato que você irá usar**

Crie `entregas/modulo-3/analisar-monolito-distribuido.md` a partir da raiz do clone; use a tabela comparativa de `docs/modulo-3-servicos/padroes-e-decisoes.md`.

**Antes de executar**

Registre como fatos que 70% das mudanças em Cadastro e Atendimento ocorrem juntas, Agenda escala dez vezes nos horários de entrada, Faturamento pertence a outro time, cadastro válido é obrigatório e faturamento não precisa confirmar no caminho crítico. Não há eventos nem idempotência.

**Insumos disponíveis**

Mapa de chamadas e fatos declarados na situação.

**Como conduzir**

**O que fazer**

1. Classifique os acoplamentos.
2. Identifique dependências críticas dispensáveis.
3. Relacione coevolução e escala a limites candidatos.
4. Compare duas alternativas de consolidação ou extração.
5. Modele uma falha parcial visível ao consumidor.

**Evidência esperada**

O texto associa cada conclusão a um fato e marca claramente o que é inferência ou hipótese.

**Entrega esperada**

Envie `entregas/modulo-3/analisar-monolito-distribuido.md`, com no máximo duas páginas e dois diagramas (atual e candidato).

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Classificação precisa dos acoplamentos | 25% | Evidência: tipo e causa; insuficiente: dependência genérica. |
| Uso consistente dos dados do caso | 25% | Evidência: fatos referenciados; insuficiente: dado inventado. |
| Comparação de alternativas | 20% | Evidência: consequências contrastadas; insuficiente: opção só listada. |
| Análise de falha parcial | 20% | Evidência: parte saudável e falha; insuficiente: sistema tratado como inteiro. |
| Separação entre fato e hipótese | 10% | Evidência: hipótese rotulada; insuficiente: suposição como fato. |

## Avaliar

### Escolher consistência para autorização prévia

**Objetivo**

Escolher uma resposta à indisponibilidade que preserve a regra clínica e não esconda seus custos.

**Situação**

Uma rede quer receber solicitações durante até quinze minutos de indisponibilidade do provedor de autorizações. A autorização pode mudar a qualquer momento; executar sem ela é arriscado e perder a solicitação também é inaceitável.

**Seu papel**

Você participa do comitê que decide entre falha explícita, recepção pendente, cache ou outro desenho fundamentado.

**Artefato que você irá usar**

Crie `entregas/modulo-3/avaliar-autorizacao.md`, a partir da raiz do clone, usando CAP, SAGA e CQRS conforme explicados em `docs/modulo-3-servicos/padroes-e-decisoes.md`.

**Antes de executar**

Considere identificador único por solicitação, estado pendente aceito por até trinta minutos, consulta HTTP sem eventos do provedor, equipe operacional em horário comercial e ausência de transação distribuída.

**Insumos disponíveis**

As garantias e limitações declaradas na situação.

**Como conduzir**

**O que fazer**

1. Defina recebimento e execução.
2. Compare três alternativas por segurança, disponibilidade, consistência e operação.
3. Avalie SAGA e CQRS apenas se resolverem uma necessidade concreta.
4. Escolha, declare estados, timeout, repetição, idempotência e sinal de revisão.

**Evidência esperada**

A decisão mostra por que a promessa de consistência protege o risco do domínio e como a equipe observará pendências.

**Entrega esperada**

Envie `entregas/modulo-3/avaliar-autorizacao.md` com contexto, alternativas, decisão, consequências, fluxo de estados e plano de observação.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Critérios ligados ao risco do domínio | 30% | Evidência: risco orienta critério; insuficiente: critério técnico solto. |
| Comparação equilibrada | 25% | Evidência: custo e ganho; insuficiente: padrão sem contraste. |
| Tratamento de estados e falhas | 20% | Evidência: transição e falha; insuficiente: fluxo só feliz. |
| Uso criterioso de SAGA e CQRS | 15% | Evidência: necessidade justifica padrão; insuficiente: sigla sem problema. |
| Revisão e observação | 10% | Evidência: sinal e revisão; insuficiente: monitoramento sem decisão. |

## Criar

### Projetar uma evolução verificável

**Objetivo**

Desenhar uma evolução mínima para Agendamento que declare fronteiras, falhas e gatilhos de mudança.

**Situação**

A plataforma hospitalar ganhará Agendamento: consulta Elegibilidade, reserva horário e pede preparo de sala. Agenda muda com frequência e recebe picos; Preparo de Sala pertence a outra equipe e aceita dois minutos de atraso.

**Seu papel**

Você cria uma proposta que comece simples e continue verificável ao evoluir.

**Artefato que você irá usar**

Crie o diretório `entregas/modulo-3/criar-agendamento/` a partir da raiz do clone e entregue `proposta.md`, `fluxo-nominal.md` e `falhas-parciais.md`; use os contratos de `laboratorios/plataforma-hospitalar/` apenas como referência, sem alterar o código.

**Antes de executar**

Considere resposta inicial em três segundos, identificador fornecido pelo consumidor, PostgreSQL disponível, mensageria permitida porém não instalada e no máximo três novas unidades implantáveis neste semestre.

**O que fazer**

1. Modele capacidades, contexts, comandos, consultas e proprietários.
2. Escolha a implantação inicial.
3. Desenhe o fluxo nominal e três falhas parciais.
4. Declare consistência, compensações, contratos, idempotência e telemetria.
5. Planeje duas etapas com gatilhos de extração ou consolidação e testes de contrato, fronteira e recuperação.

**Evidência esperada**

Cada componente tem proprietário, razão de existir, contrato verificável e consequência explícita para falha e atraso.

**Entrega esperada**

Envie `entregas/modulo-3/criar-agendamento/` com dois diagramas, registro de decisão, tabela de estados, contratos de exemplo, estratégia de testes e roteiro de evolução.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Coerência entre domínio, dados e implantação | 25% | Evidência: mesmos limites; insuficiente: topologia contradiz domínio. |
| Falhas e consistência explícitas | 25% | Evidência: falha e efeito; insuficiente: consistência presumida. |
| Contratos e verificações executáveis | 20% | Evidência: teste ou comando; insuficiente: contrato sem verificação. |
| Evolução orientada por sinais | 15% | Evidência: sinal aciona mudança; insuficiente: evolução sem gatilho. |
| Viabilidade operacional | 15% | Evidência: recursos considerados; insuficiente: componente sem operação possível. |
