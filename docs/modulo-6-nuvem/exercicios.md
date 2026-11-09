# Exercícios: decidir e operar capacidade

As atividades usam a plataforma hospitalar e dados sintéticos. Não existe resposta única: declare contexto, limite e evidência necessária. Não inclua identificadores de pacientes, credenciais ou informação clínica em capturas e entregas.

## Recordar

### Nomear fronteiras de serviço

**Situação**

A reunião de abertura do projeto durou quinze minutos e produziu uma ata com quatro frases que ninguém corrigiu na hora.

A primeira foi da liderança técnica: *"a gente vai para a nuvem, então é só subir tudo no Kubernetes"*.

A segunda veio de uma pessoa do time de produto: *"PaaS é quando o fornecedor cuida de tudo, né?"*.

A terceira foi de quem opera a infraestrutura hoje: *"se a gente tiver duas réplicas, já está em alta disponibilidade"*.

A quarta encerrou o assunto: *"imagem e contêiner é a mesma coisa, é só jeito de falar"*.

A ata registrou as quatro como decisões. A reunião seguinte, que vai definir orçamento, acontece em três dias.

**Seu papel**

Você prepara o glossário de revisão que acompanha a correção da ata. Ele precisa caber em uma página e ser lido por quem não é da área técnica.

1\. Defina IaaS, PaaS, SaaS e on-premise, dizendo em cada um quem opera o sistema operacional.

<details>
<summary>Ver resposta</summary>

IaaS entrega infraestrutura virtualizada, e o sistema operacional fica com a equipe. PaaS entrega runtime operado, e o sistema operacional fica com o provedor. SaaS entrega produto configurável, e a equipe não opera camada nenhuma. On-premise mantém a pilha inteira sob responsabilidade interna. Nenhum modelo elimina o owner de dados, configuração e continuidade, o que desfaz a segunda frase da ata.
</details>

2\. Diferencie região, zona, imagem, contêiner e orquestração.

<details>
<summary>Ver resposta</summary>

Região e zona delimitam localização e domínio de falha. Imagem é o pacote imutável e versionado. Contêiner é uma execução dessa imagem, e a mesma imagem produz muitos contêineres, o que desfaz a quarta frase da ata. Orquestração reconcilia as execuções com o estado declarado.
</details>

3\. Defina readiness, liveness, elasticidade, resiliência e rollback.

<details>
<summary>Ver resposta</summary>

Readiness decide se a instância recebe tráfego agora. Liveness decide se o processo precisa ser reiniciado. Elasticidade é ajustar capacidade conforme a demanda. Resiliência é continuar ou recuperar o serviço dentro de um objetivo declarado. Rollback retorna o Deployment a uma revisão anterior compatível.
</details>

4\. Diferencie máquina virtual e contêiner pelo que cada um carrega acima da infraestrutura.

<details>
<summary>Ver resposta</summary>

A máquina virtual carrega aplicação, dependências e um sistema operacional completo por instância, sobre um hipervisor. O contêiner carrega aplicação e dependências, sobre um motor de contêineres e um único sistema operacional compartilhado. A diferença são as cópias de sistema operacional que desaparecem.
</details>

5\. Defina estado futuro desejado e reconciliação, e diga qual das quatro frases da ata os ignora.

<details>
<summary>Ver resposta</summary>

Estado futuro desejado é o destino declarado em arquivo, em vez da sequência de passos para chegar lá. Reconciliação é o laço em que um agente compara esse destino com o estado observado e age para fechar a diferença. A primeira frase da ata os ignora, porque tratar a nuvem como lugar onde se sobe o que já existe deixa de fora tanto a declaração do destino quanto quem o mantém.
</details>

6\. Nomeie os seis Rs da modernização e diga em uma linha o que cada um significa.

<details>
<summary>Ver resposta</summary>

Rehost move sem alterar código. Replatform move com alteração mínima, trocando a plataforma de execução. Refactor altera o código existente sem mudar o comportamento externo. Rebuild recomeça a aplicação. Retire desativa e desliga. Retain mantém como está, por decisão registrada.
</details>

## Compreender

### Explicar probes sem analogia enganosa

**Situação**

Durante a revisão do manifesto, alguém propôs simplificar as duas verificações de saúde da API de elegibilidade.

A proposta é esta: fazer `/health/live` e `/health/ready` executarem a mesma consulta ao banco de dados, com o argumento de que *"se o banco cair, a API morreu de qualquer jeito"*. Um dos endpoints deixaria de existir.

O contexto que a proposta desconsidera: o serviço roda com quatro réplicas, o banco é compartilhado pelas quatro, e o mesmo banco atende outros dois serviços da casa. No mês passado ele ficou indisponível por sete minutos durante uma manutenção, e as quatro réplicas continuaram no ar respondendo erro tratado.

Quem opera o cluster nunca viu o comportamento dessa configuração sob falha e pediu uma explicação antes de aprovar.

**Seu papel**

Você explica o efeito da proposta a quem opera o cluster, usando a indisponibilidade de sete minutos do mês passado como cenário de teste mental.

1\. Descreva o que acontece com um Pod e com o tráfego quando readiness falha.

<details>
<summary>Ver resposta</summary>

O Pod pode continuar em execução, mas o Service deixa de encaminhar tráfego a ele, porque ele sai da lista de endpoints. O processo segue vivo, e nada é reiniciado. Esse comportamento não confirma que a regra de negócio está correta, apenas que a instância se declarou inelegível ao tráfego.
</details>

2\. Descreva o que aconteceria nos sete minutos do mês passado se a proposta já estivesse valendo.

<details>
<summary>Ver resposta</summary>

A falha de liveness leva ao reinício do contêiner. Como as quatro réplicas consultam o mesmo banco, as quatro falhariam a verificação ao mesmo tempo e seriam reiniciadas juntas, repetidamente, enquanto a manutenção durasse. O serviço perderia a capacidade que ainda tinha para responder erro tratado, e o incidente do banco viraria também um incidente da API. A dependência remota pertence à readiness ou a uma resposta degradada, conforme o contrato.
</details>

3\. Diferencie processo vivo, pronto para tráfego e resposta de negócio correta, e diga qual das três nenhuma probe consegue verificar.

<details>
<summary>Ver resposta</summary>

Vivo significa que o processo está executando e responde ao endpoint de vitalidade. Pronto significa elegível a receber tráfego agora. Correto significa que a resposta de negócio está certa, e é a única das três que nenhuma probe verifica, porque ela depende de regra de domínio e de dados, que nenhum sinal de processo expõe. Uma versão logicamente errada responde saúde normalmente.
</details>

### Explicar por que o cluster desfez a alteração manual

**Situação**

Na madrugada de sábado, com o serviço sob pressão, a pessoa de plantão executou `kubectl scale deployment web --replicas=8` e o serviço estabilizou. Ela registrou a ação no canal do time e foi dormir.

Na manhã de segunda-feira, o Deployment estava de volta em três réplicas. Ninguém tinha mexido nele desde sábado. O time usa Argo CD, com o repositório de manifestos como fonte da verdade e `selfHeal` ativado.

A pessoa de plantão está convencida de que alguém reverteu a mudança dela sem avisar, e abriu uma discussão sobre confiança no time.

**Seu papel**

Você explica o que aconteceu de fato, e depois explica o que deveria ter sido feito naquela madrugada.

1\. Explique o mecanismo que devolveu o Deployment a três réplicas, sem atribuir a ação a uma pessoa.

<details>
<summary>Ver resposta</summary>

O estado desejado do serviço vive no repositório Git, que continua declarando três réplicas. O Argo CD compara continuamente esse destino declarado com o estado observado no cluster, e o comando manual criou uma divergência. Com `selfHeal` ativado, a sincronização desfez a divergência restaurando o valor do repositório. A reversão foi executada pelo laço de reconciliação, conforme a configuração, sem ação de nenhuma pessoa.
</details>

2\. Explique por que o registro no canal do time não impediu o desfazimento, e o que teria impedido.

<details>
<summary>Ver resposta</summary>

O agente de reconciliação consulta apenas o repositório. A alteração ficou fora da única fonte que o sistema consulta. O que teria persistido é a mudança do número de réplicas no manifesto versionado, aprovada e sincronizada. Em situação de urgência, a alternativa é suspender a sincronização automática do serviço enquanto dura o incidente, deixando registro dessa suspensão.
</details>

3\. Diferencie o papel de Terraform, Ansible e Argo CD neste cenário, dizendo qual deles teria agido e quais não.

<details>
<summary>Ver resposta</summary>

O Argo CD é o que agiu, porque cuida do estado das aplicações dentro do cluster e mantém o repositório como fonte da verdade. O Terraform não agiria, porque o escopo dele é provisionar a infraestrutura em que o cluster existe, e o número de réplicas de um Deployment não está no arquivo de estado dele. O Ansible também não agiria, porque ele executa tarefas quando é chamado e não guarda estado nem observa o cluster continuamente.
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

1. A rajada dura cerca de duas horas por mês. No restante do tempo, o uso é quase nulo.
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

1. Duas réplicas antigas atendem normalmente. Duas novas não iniciam.
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

### Escolher o R de cada aplicação do portfólio

**Objetivo**

Aplicar o vocabulário dos seis Rs a três aplicações reais de um mesmo portfólio, escolhendo uma estratégia por aplicação e defendendo a escolha com fatos do caso.

**Situação**

O contrato do data center do hospital vence em dezoito meses e não será renovado. A diretoria pediu uma decisão por aplicação, e três delas chegaram primeiro.

A primeira é o **sistema de faturamento**. Ele roda em dois servidores físicos, foi escrito há dezoito anos numa linguagem que ninguém da equipe atual domina, e não recebe mudança funcional há quatro anos. Ele funciona. A auditoria externa exige que o histórico permaneça consultável por mais dois anos, e nenhum outro sistema sabe produzir os relatórios que ele produz.

A segunda é o **portal de agendamento**. É um monolito Java que atende bem no dia a dia, mas satura no pico das manhãs de segunda-feira e derruba requisições. A publicação de uma versão nova leva seis horas e acontece de madrugada, uma vez por mês. A equipe conhece o código, e o banco relacional que ele usa é padrão de mercado.

A terceira é o **controle de estoque da farmácia**. Quatro pessoas o usam. O ERP corporativo implantado no ano passado já cobre a entrada de notas, a contagem e o inventário, que são três das cinco funções do sistema antigo. As duas funções restantes são relatórios que a farmácia imprime uma vez por mês.

Três restrições valem para as três decisões:

1. O data center precisa ser esvaziado em dezoito meses.
2. A equipe tem cinco pessoas e opera as três aplicações ao mesmo tempo.
3. Nenhuma das três pode ficar indisponível durante horário de atendimento.

As seis estratégias, resumidas de [Padrões e decisões](padroes-e-decisoes.md), bastam para decidir:

| Estratégia | O que significa | Esforço |
| --- | --- | --- |
| **Rehost** | mover sem alterar código, também chamado de *lift and shift* | baixo |
| **Replatform** | mover para uma plataforma de execução nova com alterações mínimas de código, como trocar o banco por um gerenciado ou o servidor de aplicação por um runtime operado | baixo a médio |
| **Refactor** | alterar o código existente sem mudar de forma relevante o comportamento externo, para melhorar desempenho, escala e integração | alto |
| **Rebuild** | recomeçar a aplicação, em geral com arquitetura nova | muito alto |
| **Retire** | desativar e desligar a aplicação | baixo |
| **Retain** | manter como está por ora, com a razão e a data de reavaliação registradas | nenhum |

**Seu papel**

Você apresenta a recomendação à diretoria. Quem lê vai comparar as três decisões entre si, então a justificativa de cada uma precisa citar os fatos que a sustentam.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escolha um R para o sistema de faturamento e defenda a escolha citando dois fatos do caso. Diga também qual R você quase escolheu e o que o desqualificou.
2. Escolha um R para o portal de agendamento. Explique por que replatform e refactor levam a resultados diferentes para o problema do pico de segunda-feira, e diga qual dos dois resolve o problema da publicação de seis horas.
3. Escolha um R para o controle de estoque da farmácia e descreva o que precisa acontecer com as duas funções que o ERP ainda não cobre antes que a escolha seja executável.
4. As três decisões competem pela mesma equipe de cinco pessoas. Ordene as três aplicações por ordem de execução e justifique a ordem pela restrição de dezoito meses.
5. Para a aplicação que você colocou em primeiro lugar, escreva a evidência que, seis meses depois, confirmaria que o R escolhido foi o certo, e a evidência que indicaria que foi o errado.

**Evidência esperada**

O arquivo entregue traz um R por aplicação, cada um com dois fatos do caso citados e a alternativa descartada nomeada, a distinção entre replatform e refactor aplicada ao portal, a condição de saída do sistema da farmácia, a ordem de execução justificada pelo prazo e o par de evidências que confirmaria ou refutaria a primeira decisão.

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
2. O hospital opera numa região só hoje, e a segunda região é uma intenção ainda sem projeto.
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

### Diagramar a arquitetura de referência num provedor

**Objetivo**

Traduzir o modelo de referência de plataforma em nuvem para o portfólio de um provedor concreto, produzindo um diagrama defensável.

**Situação**

O modelo de referência apresentado em [Exemplo arquitetural](exemplo-arquitetural.md) descreve uma plataforma em nuvem formada por sete peças:

1. Camada de acessibilidade, que funciona como *ingress controller*, *firewall* ou *proxy* e recebe os clientes móvel e web.
2. Dois microgateways, um para o canal móvel e outro para o canal web, cada um no próprio conjunto de escala.
3. API do plano de controle, que carrega políticas de segurança, controle de taxa de requisição e regras de escala.
4. Microsserviços de integração, cada um no próprio conjunto de escala, ligados aos microgateways.
5. Banco de dados gerenciado pelo provedor e replicado.
6. Uma carga legada, o LMS, executada em máquina virtual sem ter sido reescrita.
7. Três serviços de terceiros consumidos como SaaS: videoconferência, cobrança e CRM.

A diretoria pediu uma representação desse modelo na AWS, para discutir custo e responsabilidade com o fornecedor. O catálogo de serviços básicos, detalhado em [Estudo de caso](estudo-de-caso.md), reúne estes serviços por categoria:

| Categoria | Serviços do catálogo |
| --- | --- |
| Computação | Amazon EC2, AWS Lambda, Amazon ECS, Amazon EKS e AWS Fargate |
| Armazenamento | Amazon S3, Amazon EBS, Amazon FSx, AWS Backup e Amazon Glacier |
| Banco de dados | Amazon RDS, Amazon DynamoDB, Amazon Aurora, Amazon Redshift, Amazon ElastiCache, Amazon DocumentDB e Amazon Keyspaces |
| Rede e segurança | Amazon VPC, AWS CloudFront, AWS Route 53, AWS WAF e AWS Shield |
| IA e aprendizado de máquina | Amazon SageMaker, AWS Rekognition, AWS Textract e Amazon Comprehend |
| Monitoramento e DevOps | Amazon CloudWatch, AWS X-Ray, AWS CodePipeline e AWS CloudFormation |

A Figura 16 do [Estudo de caso](estudo-de-caso.md) mostra o nível de detalhe esperado, com Route 53, CloudFront e S3 na entrada, balanceadores e instâncias EC2 com escala automática em duas zonas de disponibilidade e um par RDS primário e réplica com replicação entre zonas.

A atividade é de desenho. Nada é provisionado no provedor, e nenhum recurso real é criado.

**Seu papel**

Você produz o diagrama e a justificativa que o acompanha. Quem lê vai perguntar por que cada serviço foi escolhido, então a resposta precisa vir junto do desenho.

**O que fazer**

1. Represente o modelo de referência usando serviços do catálogo da AWS. A ferramenta Cloudcraft, apresentada em aula, produz diagramas no nível de detalhe da Figura 16, e qualquer editor de diagramas serve.
2. Marque no desenho as duas zonas de disponibilidade e o que fica replicado entre elas.
3. Para cada serviço escolhido, escreva uma linha no formato atributo, princípio e serviço. Exemplo: reduzir operação de runtime, delegar o host da aplicação, AWS Fargate.
4. Aponte as três peças do modelo de referência que você deixou de fora e explique por quê.
5. Indique qual escolha do seu desenho seria a mais cara de reverter, e o que precisaria estar documentado hoje para que essa reversão fosse possível.

**Evidência esperada**

O arquivo entregue traz o diagrama, a lista de serviços com atributo e princípio associados a cada um, as peças omitidas com justificativa e a dependência identificada como mais difícil de trocar, acompanhada do que a tornaria reversível.

## Questões de múltipla escolha

As vinte questões a seguir formam a atividade de fixação da Unidade 6 no Canvas e cobrem o conteúdo das páginas deste módulo. Cada questão tem uma única alternativa correta e traz o nível de dificuldade entre colchetes: as simples verificam definições, as médias aplicam os conceitos a uma situação e as difíceis pedem análise de alternativas e consequências.

### Questões simples

#### Questão 1 [Simples]

No modelo PaaS, o que a organização continua operando?

- (a) Rede, armazenamento e servidores.
- (b) Aplicação e dados.
- (c) Sistema operacional e middleware.
- (d) Nenhuma camada, porque o provedor opera a pilha inteira.

#### Questão 2 [Simples]

Qual exemplo corresponde ao modelo SaaS?

- (a) Amazon EC2.
- (b) Google App Engine.
- (c) Um servidor em data center próprio.
- (d) Microsoft 365.

#### Questão 3 [Simples]

Qual é a diferença entre uma imagem e um contêiner?

- (a) A imagem empacota filesystem, dependências e metadados imutáveis, e o contêiner é uma execução isolada dessa imagem.
- (b) A imagem é uma máquina virtual completa, e o contêiner é o hipervisor.
- (c) A imagem roda em produção, e o contêiner roda apenas em desenvolvimento.
- (d) Não há diferença, os dois termos são sinônimos.

#### Questão 4 [Simples]

O que a probe de readiness pergunta ao orquestrador?

- (a) Se o processo deve ser reiniciado por estar travado.
- (b) Se a imagem tem versão reprodutível.
- (c) Se esta instância deve receber tráfego agora.
- (d) Se o cluster tem capacidade para mais réplicas.

#### Questão 5 [Simples]

Como o módulo define elasticidade?

- (a) A capacidade de crescer mantendo comportamento aceitável.
- (b) O ajuste da capacidade em resposta à demanda.
- (c) A troca de recursos da mesma réplica.
- (d) A replicação de dados entre regiões.

#### Questão 6 [Simples]

O que é uma zona, no vocabulário de nuvem do módulo?

- (a) Uma área geográfica onde o provedor oferece recursos.
- (b) Um grupo de contêineres com o mesmo rótulo.
- (c) Uma unidade de isolamento de falha dentro de uma região.
- (d) Um contrato de nível de serviço.

#### Questão 7 [Simples]

Na formulação dos seis Rs de modernização, o que significa rehost?

- (a) Mover a aplicação sem alterar o código, também chamado de lift and shift.
- (b) Recomeçar a aplicação do zero.
- (c) Desativar e desligar a aplicação.
- (d) Alterar o código sem mudar o comportamento externo.

#### Questão 8 [Simples]

O que significa que uma aplicação é stateless?

- (a) Que ela não usa banco de dados.
- (b) Que ela não registra logs.
- (c) Que ela não pode ser executada em Kubernetes.
- (d) Que ela não mantém no processo de uma réplica o único estado necessário para atender a próxima requisição.

### Questões médias

#### Questão 9 [Média]

Uma equipe colocou a verificação do banco de dados na probe de liveness. Qual risco o módulo aponta?

- (a) A probe fica lenta e atrasa a implantação.
- (b) Uma falha compartilhada no banco transforma-se em reinício coletivo das réplicas, justamente quando a dependência precisa estabilizar.
- (c) O banco passa a receber tráfego indevido.
- (d) A readiness deixa de funcionar.

#### Questão 10 [Média]

Um Pod foi apagado manualmente, e o Deployment declara três réplicas. O que acontece, e por quê?

- (a) O controlador cria outro Pod, porque o estado desejado declarado continua pedindo três réplicas.
- (b) Nada, porque a remoção manual tem precedência sobre o manifesto.
- (c) O cluster reduz o número desejado para duas réplicas.
- (d) O Service deixa de funcionar até a próxima implantação.

#### Questão 11 [Média]

Uma aplicação Java guarda o carrinho de compras em HttpSession, sustentada por sessão fixa no balanceador. Qual fator dos doze fatores é violado, e qual é a consequência?

- (a) Fator 3, configurações, porque a senha fica no código.
- (b) Fator 11, logs, porque o log morre com o contêiner.
- (c) Fator 1, base de código, porque há pastas por ambiente.
- (d) Fator 6, processos, porque o carrinho some quando a réplica é substituída em uma atualização gradual.

#### Questão 12 [Média]

Uma equipe faz git pull e recompila o código dentro do servidor de produção a cada versão. Por que isso dificulta o rollback, segundo o fator 5?

- (a) Porque o git não permite voltar versões.
- (b) Porque a recompilação apaga os logs.
- (c) Porque não existe um artefato imutável com tag para onde voltar, apenas um diretório atualizado no lugar.
- (d) Porque o rollback exige mudar de provedor.

#### Questão 13 [Média]

O HPA do laboratório declara de duas a cinco réplicas com alvo de CPU. O que o módulo afirma sobre essa configuração?

- (a) Que ela é uma política que ainda precisa de verificação e exige métrica disponível, request de CPU definido e observação de latência, fila, erro e saturação.
- (b) Que ela prova que a aplicação escala sob qualquer carga.
- (c) Que ela dispensa a definição de limits.
- (d) Que ela garante alta disponibilidade entre zonas.

#### Questão 14 [Média]

Qual é a divisão de responsabilidades entre Terraform, Ansible e Argo CD apresentada no módulo?

- (a) Os três fazem a mesma coisa e competem entre si.
- (b) Terraform sincroniza o cluster, Ansible cria redes e Argo CD instala pacotes.
- (c) Ansible é stateful com arquivo de estado, e Terraform lê o inventário a cada execução.
- (d) Terraform provisiona a infraestrutura no Day 0, Ansible prepara sistema operacional e aplicações do Day 1 em diante, e Argo CD sincroniza continuamente o cluster com o repositório.

#### Questão 15 [Média]

Uma organização compra uma agenda como SaaS. Que responsabilidade continua com ela, segundo o modelo de responsabilidade compartilhada?

- (a) Nenhuma, porque o provedor opera a pilha inteira.
- (b) A atualização do sistema operacional do provedor.
- (c) A configuração, a integração, as credenciais e a classificação dos dados enviados ao serviço.
- (d) A manutenção do hardware do provedor.

### Questões difíceis

#### Questão 16 [Difícil]

A API de elegibilidade tem duas réplicas em um cluster kind de um único nó. A equipe afirma que o serviço é altamente disponível. Como o módulo avalia a afirmação?

- (a) Correta, porque duas réplicas garantem alta disponibilidade.
- (b) Incorreta, porque uma réplica extra no mesmo nó protege contra a queda de um processo e não protege contra a perda do nó, e o cluster local não representa falha de zona.
- (c) Correta, desde que o HPA esteja configurado.
- (d) Incorreta, porque o kind não permite mais de uma réplica.

#### Questão 17 [Difícil]

Uma nova versão foi implantada, quebrou a gravação de dados e foi revertida com kubectl rollout undo. O que o rollback resolve e o que ele não resolve?

- (a) Resolve tudo, porque restaura o banco ao estado anterior.
- (b) Não resolve nada, porque o rollback só funciona antes da implantação.
- (c) Desfaz as mensagens publicadas, mas não restaura a imagem.
- (d) Retorna o Deployment à revisão anterior, mas não desfaz efeitos irreversíveis já gravados em banco, mensagens ou integrações.

#### Questão 18 [Difícil]

Uma equipe aumenta as réplicas da API para absorver um pico, mas o banco de dados já está saturado de conexões. O que o módulo alerta?

- (a) Que aumentar somente a API pode amplificar uma falha posterior, porque banco, conexões e dependências também limitam a escala.
- (b) Que a API escala de forma independente das dependências.
- (c) Que o banco escala automaticamente junto com a API.
- (d) Que o HPA reduz as conexões ao banco.

#### Questão 19 [Difícil]

Uma equipe quer abstrair todos os serviços gerenciados da nuvem para evitar lock-in. Qual é a orientação do módulo?

- (a) Abstrair tudo desde o início, porque lock-in deve ser sempre evitado.
- (b) Usar apenas IaaS, porque PaaS e SaaS sempre geram lock-in.
- (c) Aceitar lock-in quando o benefício específico é conhecido e revisável, registrando no ADR a API proprietária, o formato de dados e a condição mensurável de saída, porque abstrair tudo prematuramente cria uma plataforma paralela.
- (d) Ignorar o lock-in, porque contratos de nuvem permitem troca a qualquer momento.

#### Questão 20 [Difícil]

No caso real do iFood, em 2018, a maior parte das instâncias EC2 do horário de pico era comprada como spot. Que característica do negócio torna esse arranjo coerente com a elasticidade?

- (a) Demanda constante ao longo do dia, que dispensa ajuste de capacidade.
- (b) Sazonalidade diária, com picos no almoço e no jantar e demanda baixa entre eles, que é o caso de uso canônico de elasticidade.
- (c) Exigência de residência de dados no Brasil.
- (d) Ausência de requisitos de disponibilidade.
