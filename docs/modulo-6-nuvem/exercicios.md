# Exercícios: decidir e operar capacidade

As atividades usam a plataforma hospitalar e dados sintéticos. Não existe resposta única: declare contexto, limite e evidência necessária. Não inclua identificadores de pacientes, credenciais ou informação clínica em capturas e entregas.

## Recordar

### Nomear fronteiras de serviço

**Situação**

Uma equipe usa “nuvem”, “Kubernetes” e “PaaS” como sinônimos ao discutir a API de elegibilidade.

**Seu papel**

Você prepara um glossário de revisão.

1\. Defina IaaS, PaaS, SaaS e on-premise.

<details>
<summary>Ver resposta</summary>

IaaS entrega infraestrutura virtualizada; PaaS entrega runtime operado; SaaS entrega produto configurável; on-premise mantém infraestrutura sob maior responsabilidade interna. Nenhum modelo elimina o owner de dados, configuração e continuidade.
</details>

2\. Diferencie região, zona, contêiner, imagem e orquestração.

<details>
<summary>Ver resposta</summary>

Região e zona delimitam localização e falha; imagem é o pacote versionado; contêiner é sua execução; orquestração reconcilia execuções com o estado declarado.
</details>

3\. Explique readiness, liveness, elasticidade, resiliência e rollback. Para cada termo, relacione uma decisão ou arquivo do caso.

<details>
<summary>Ver resposta</summary>

Readiness controla tráfego, liveness permite reiniciar processo travado, elasticidade ajusta capacidade, resiliência mede continuidade e rollback retorna uma revisão compatível. Os manifests e a oficina fornecem as evidências locais.
</details>

## Compreender

### Explicar probes sem analogia enganosa

**Situação**

Alguém propõe usar a mesma chamada ao banco para liveness e readiness porque “se o banco cair, a API morreu”.

**Seu papel**

Você explica o efeito dessa proposta a quem opera o cluster.

1\. Descreva o que acontece quando readiness falha.

<details>
<summary>Ver resposta</summary>

O Pod pode continuar em execução, mas o Service deixa de encaminhar tráfego a ele; isso não confirma que a regra de negócio está correta.
</details>

2\. Descreva o que acontece quando liveness falha e quando a dependência compartilhada está indisponível.

<details>
<summary>Ver resposta</summary>

Falha de liveness permite reinício do contêiner. Se uma dependência remota cai, usá-la como liveness pode reiniciar todas as réplicas e ampliar o incidente; ela deve orientar readiness ou degradação conforme o contrato.
</details>

3\. Diferencie processo vivo, pronto para tráfego e resposta de negócio correta. Explique por que reiniciar todas as réplicas pode piorar o incidente.

<details>
<summary>Ver resposta</summary>

Vivo significa processo executando; pronto significa elegível ao tráfego; correto requer validação de negócio. Reinícios coletivos removem capacidade enquanto a dependência externa ainda está indisponível.
</details>

## Aplicar
### Recomendar o modelo de execução para uma carga em rajada

**Objetivo**

Recomendar um entre quatro modelos de execução em nuvem para uma carga concentrada, declarando ganho, custo e a restrição que encarece a escolha.

**Situação**

Uma operadora emite a segunda via da carteirinha do beneficiário. O beneficiário pede pelo aplicativo, o sistema monta um documento e devolve um endereço para baixar.

O uso é concentrado. No primeiro dia útil de cada mês, quando o boleto chega, a procura sobe por cerca de duas horas. No resto do mês, o serviço fica praticamente parado. Hoje ele roda numa máquina virtual ligada o tempo inteiro, dimensionada para o pico, e a conta mensal incomoda a diretoria.

A área de infraestrutura pediu uma recomendação de modelo de execução.

Seis fatos foram apurados na operadora:

1. A rajada dura cerca de duas horas por mês; no restante, o uso é quase nulo.
2. Cada emissão leva de três a quarenta segundos, porque depende de um serviço externo lento.
3. A equipe tem duas pessoas e nenhuma experiência com orquestração de contêineres.
4. O documento gerado é gravado em armazenamento de objetos, e o processo não guarda estado local.
5. A área de segurança exige que o tráfego de saída use um endereço fixo conhecido pelo parceiro.
6. Nenhuma outra carga da operadora precisa de orquestração hoje.

As quatro alternativas em avaliação:

| Alternativa | Como a carga executa |
| --- | --- |
| **A. Máquina maior** | Uma máquina virtual dimensionada para o pico, ligada o mês inteiro. |
| **B. Grupo com escala automática** | Um conjunto de máquinas virtuais que cresce e encolhe conforme a fila de pedidos. |
| **C. Contêineres orquestrados** | A aplicação roda em contêineres num serviço gerenciado de orquestração, com escala por métrica. |
| **D. Função sob demanda** | Cada emissão executa numa função sem servidor, cobrada por invocação e por tempo de execução. |

**Seu papel**

Você é a pessoa arquiteta responsável pela recomendação. A equipe de infraestrutura implementa depois, e espera de você a escolha e a restrição que ela encarece.

**O que fazer**

Escreva em texto corrido, uma resposta por item. Não é preciso desenhar nada.

1. Recomende um dos quatro modelos, em uma frase.
2. Sobre cada um dos quatro, escreva duas frases: o que ele resolve do problema descrito e o que ele cobra em troca.
3. O fato 5 exige endereço fixo de saída. Diga se ele encarece a sua recomendação e o que precisaria ser montado para atendê-lo.
4. Aponte o modelo que você descartaria de imediato e diga quais fatos o derrubam.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que faria rever a decisão.

**Evidência esperada**

O artefato traz o quadro comparativo completo, a recomendação em uma frase, o fato que encarece a escolha com o que precisa ser montado, a relação entre ausência de estado local e as alternativas elásticas, a alternativa descartada, o risco aceito e o sinal de revisão observável.

## Analisar
### Investigar uma atualização que não termina

**Objetivo**

Separar sinal, hipótese e contenção durante um incidente de implantação, sem tocar em ambiente compartilhado.

**Situação**

Na sexta-feira à tarde, a equipe publicou uma versão nova da API de elegibilidade num cluster gerenciado. Trinta minutos depois, a atualização não terminou.

O painel mostra duas réplicas antigas ainda atendendo normalmente e duas réplicas novas presas num estado de espera, com a mensagem `ImagePullBackOff`. A verificação de prontidão das réplicas antigas continua respondendo com sucesso.

A revisão anterior da aplicação continua registrada e disponível. Nada foi alterado no banco de dados, e o esquema é o mesmo das duas versões.

São 17h30 de sexta-feira. A equipe de plantão termina às 18h.

Cinco fatos valem para a análise:

1. Duas réplicas antigas atendem normalmente; duas novas não iniciam.
2. A mensagem apresentada é `ImagePullBackOff`.
3. A revisão anterior continua registrada e pode ser restabelecida.
4. Nenhuma alteração de banco acompanhou a versão nova.
5. São 17h30 de sexta-feira e o plantão termina às 18h.

**Seu papel**

Você conduz a resposta ao incidente. A decisão precisa sair antes das 18h, e ela será revista na segunda-feira.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Explique por que o serviço continua no ar mesmo com metade das réplicas presas, e diga que configuração de atualização produz esse comportamento.
2. Escreva duas hipóteses diferentes para a mensagem `ImagePullBackOff`, e diga que verificação separaria uma da outra.
3. O fato 4 elimina uma classe inteira de hipóteses. Diga qual, e por quê.
4. Escolha entre restabelecer a revisão anterior agora ou investigar antes de agir, e justifique usando o fato 5. Diga o que você perde na opção que descartou.
5. Descreva a barreira que impediria esse incidente de acontecer de novo, e diga em que momento da esteira ela agiria.

**Evidência esperada**

O arquivo entregue explica o mecanismo que manteve o serviço no ar, apresenta duas hipóteses com a verificação que as separa, usa o fato 4 para reduzir o espaço de busca, justifica a decisão de contenção pelo horário e nomeia a barreira preventiva com o momento em que ela age.

## Avaliar
### Escolher o modelo de serviço para uma capacidade nova

**Objetivo**

Julgar três modelos de serviço de nuvem contra critérios declarados, incluindo uma exigência regulatória que nenhum deles resolve sozinho.

**Situação**

O hospital vai lançar um portal de consulta para pacientes. São poucas telas e três APIs: buscar exame, baixar laudo e agendar retorno.

A equipe tem três pessoas. Nenhuma opera cluster hoje, e o hospital não tem nenhuma outra carga que precise de orquestração.

O tráfego é previsível: sobe entre 8h e 10h e entre 18h e 20h, e cai quase a zero de madrugada.

Há uma exigência que não se negocia. Dado de paciente precisa permanecer em território nacional, com comprovação por escrito do provedor, e o jurídico do hospital audita isso uma vez por ano.

Existe também a possibilidade de contratar um serviço pronto de mensagens para o portal, em vez de construir.

Três modelos estão sobre a mesa, e as descrições abaixo bastam para julgá-los.

No primeiro, o hospital aluga máquinas virtuais e opera sistema, atualização e rede por conta própria.

No segundo, o hospital publica a aplicação num ambiente de execução gerenciado, no qual o provedor cuida de sistema e de escala, e a equipe entrega apenas o código.

No terceiro, o hospital contrata um portal pronto de terceiro e configura, sem construir a aplicação.

Cinco fatos valem para a decisão:

1. Três pessoas na equipe, nenhuma com experiência em orquestração.
2. Nenhuma outra carga do hospital precisa de orquestração hoje.
3. O tráfego tem dois picos diários previsíveis e cai a quase zero de madrugada.
4. Dado de paciente precisa ficar em território nacional, com comprovação por escrito.
5. O jurídico audita a comprovação de residência uma vez por ano.

**Seu papel**

Você emite o parecer que a diretoria vai usar para aprovar o orçamento.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Declare de três a quatro critérios de julgamento e diga qual pesa mais, justificando pela exigência de residência de dado.
2. Avalie os três modelos contra os seus critérios, um parágrafo por modelo, dizendo o que cada um transfere ao provedor e o que permanece com o hospital.
3. O fato 4 vale para os três modelos, e nenhum o resolve sozinho. Diga o que o hospital precisa exigir do provedor em cada um deles.
4. Emita o parecer e descreva o que aconteceria se o hospital precisasse trocar de provedor em dois anos: o que sairia fácil e o que sairia caro.
5. Escreva o sinal que indicaria que o modelo escolhido deixou de servir.

**Evidência esperada**

O parecer traz critérios escritos antes da escolha, os três modelos julgados com a divisão de responsabilidade explicitada, a exigência de residência tratada modelo a modelo, o custo de saída estimado e o sinal de revisão observável.

## Criar
### Propor a evolução resiliente da elegibilidade

**Objetivo**

Propor a evolução de um serviço que passa a guardar estado, escolhendo entre três desenhos e declarando o que a proposta promete e o que ela ainda não garante.

**Situação**

A API de elegibilidade do hospital hoje é simples: recebe uma consulta, calcula e responde. Nada é guardado entre uma chamada e outra, e por isso qualquer réplica atende qualquer requisição.

Duas mudanças foram aprovadas. A primeira é guardar o histórico de consultas, para auditoria e para responder mais rápido em casos repetidos. A segunda é avisar o sistema de recepção quando uma elegibilidade muda de situação, sem que ele precise perguntar.

A equipe quer continuar publicando versões novas sem derrubar o serviço, como faz hoje.

O hospital opera numa única região. A diretoria fala em abrir uma segunda região no ano que vem, e ninguém testou recuperação em outra região até agora.

Três desenhos estão sobre a mesa, e as descrições abaixo bastam para escolher.

No primeiro, cada réplica guarda o histórico em disco próprio, e o aviso à recepção é uma chamada direta feita no fim do cálculo.

No segundo, o histórico vai para um banco gerenciado compartilhado pelas réplicas, e o aviso à recepção continua sendo chamada direta.

No terceiro, o histórico vai para o banco gerenciado e o aviso é registrado numa tabela de saída, entregue por um processo separado.

Quatro restrições valem para a proposta:

1. A publicação de versões novas não pode derrubar o serviço.
2. O hospital opera numa região só hoje, e a segunda é intenção, não projeto.
3. Recuperação em outra região nunca foi testada.
4. A recepção tolera até um minuto de atraso no aviso de mudança.

**Seu papel**

Você propõe o desenho da evolução. A proposta será lida por quem opera o serviço, e prometer recuperação não testada é o erro mais caro que ela pode conter.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escolha um dos três desenhos e defenda a escolha citando pelo menos duas das quatro restrições.
2. Explique por que o primeiro desenho entra em conflito com a restrição 1, detalhando o que acontece com o histórico quando uma réplica é substituída.
3. Sobre o desenho que você não escolheu entre o segundo e o terceiro, escreva duas frases: o que ele ganharia e o que custaria.
4. Descreva o que acontece com um aviso à recepção quando o sistema dela está fora do ar por dez minutos, na sua proposta.
5. A restrição 3 diz que recuperação em outra região nunca foi testada. Escreva o que a sua proposta promete hoje sobre isso, e o teste que precisaria existir antes de prometer mais.

**Evidência esperada**

O arquivo entregue traz o desenho escolhido com duas restrições citadas, o conflito entre estado local e publicação sem interrupção explicado, a alternativa restante avaliada, o comportamento do aviso durante indisponibilidade e a fronteira explícita entre o que é prometido e o que ainda não foi testado.
