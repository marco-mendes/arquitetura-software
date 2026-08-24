# Knight Capital: 45 minutos, 460 milhões de dólares

Em 1º de agosto de 2012, às 9h30 da manhã, a bolsa de Nova York abriu. Quarenta e cinco minutos depois, a Knight Capital Americas tinha comprado e vendido 397 milhões de ações que ninguém pediu, acumulado uma posição não intencional de bilhões de dólares e perdido mais de **460 milhões**. A empresa, que respondia por cerca de 10% do volume negociado em ações listadas nos Estados Unidos, foi vendida meses depois.

A causa não foi um ataque, nem uma falha de hardware, nem um algoritmo mal calibrado. Foi um deploy manual em oito servidores no qual um técnico esqueceu um.

O relato a seguir vem da ordem administrativa que a SEC publicou em 16 de outubro de 2013. É um documento regulatório, com o detalhe técnico apurado e as datas confirmadas, e é raro ter uma fonte dessa qualidade sobre um incidente de software.

## 2003: o código que parou de ser usado e continuou lá

A Knight operava um roteador automático de ordens chamado SMARS. A função dele é receber ordens grandes de clientes (o documento as chama de *parent orders*) e quebrá-las em ordens menores, as *child orders*, enviadas a diferentes centros de negociação conforme a liquidez disponível.

Dentro do SMARS existia uma funcionalidade chamada **Power Peg**. A Knight parou de usá-la em 2003. Não removeu o código. Nas palavras da SEC: *"Despite the lack of use, the Power Peg functionality remained present and callable at the time of the RLP deployment."*

Presente e chamável. Por nove anos.

## 2005: a bomba é armada

O Power Peg tinha uma trava de segurança. Conforme as ordens filhas eram executadas, uma função de quantidade acumulada contava quantas ações da ordem original já tinham sido negociadas, e mandava parar quando a ordem estivesse completa.

Em 2005, a Knight moveu essa contagem para um trecho anterior do SMARS. A frase seguinte da ordem da SEC é a que define o caso: *"Knight did not retest the Power Peg code after moving the cumulative quantity function to determine whether Power Peg would still function correctly if called."*

O código morto perdeu o freio, e ninguém testou porque ninguém pretendia chamá-lo de novo. A partir desse dia, o Power Peg era uma função que, se acionada, enviaria ordens filhas indefinidamente, sem nunca reconhecer que a ordem original já tinha sido preenchida.

Ficou assim por sete anos.

## Julho de 2012: a flag é reaproveitada

A bolsa de Nova York lançaria em 1º de agosto de 2012 o Retail Liquidity Program. Para participar, a Knight escreveu código novo no SMARS.

Duas decisões de implementação se combinaram. O código novo foi escrito para ocupar o lugar do código não usado do Power Peg. E **reaproveitou a mesma flag** que antigamente ativava o Power Peg. A intenção era apagar o Power Peg, de modo que a flag ligada passasse a acionar a funcionalidade nova.

A partir de 27 de julho, o código foi implantado em etapas, em alguns servidores por dia. E então:

> *"During the deployment of the new code, however, one of Knight's technicians did not copy the new code to one of the eight SMARS computer servers. Knight did not have a second technician review this deployment and no one at Knight realized that the Power Peg code had not been removed from the eighth server, nor the new RLP code added. Knight had no written procedures that required such a review."*

Sete servidores com o código novo. Um servidor com o código de 2003, sem freio, e uma flag que agora seria ligada por ordens de clientes reais.

## 8h01: o sistema avisa 97 vezes

Antes da abertura do mercado, ordens destinadas ao pré-mercado passaram pelo SMARS. A partir de 8h01, um sistema interno começou a gerar mensagens automáticas de erro, chamadas *BNET rejects*, que citavam o SMARS e traziam a descrição **"Power Peg disabled"**.

O sistema enviou **97 dessas mensagens** a um grupo de funcionários antes das 9h30.

A ordem da SEC é precisa sobre por que elas não serviram para nada: *"Knight did not design these types of messages to be system alerts, and Knight personnel generally did not review them when they were received."* E completa que as mensagens eram em tempo real, foram causadas pela falha de implantação, e ofereciam uma oportunidade de identificar e corrigir o problema antes da abertura.

Noventa e sete avisos, com o nome do subsistema e o nome exato da funcionalidade defeituosa, entregues com noventa minutos de antecedência a um grupo de pessoas para quem aquilo era ruído.

## 9h30: quarenta e cinco minutos

O mercado abriu. As ordens chegaram com a flag ligada. Os sete servidores corretos processaram normalmente. O oitavo acionou o Power Peg.

Como a função de quantidade acumulada tinha sido movida em 2005, esse servidor passou a enviar ordens filhas em sequência rápida para cada ordem que entrava, sem considerar quantas execuções já tinham voltado. Outra parte do sistema sabia que as ordens já estavam preenchidas, e essa informação não chegava ao SMARS.

O resultado, nos números da SEC: **212** ordens de clientes viraram milhões de ordens filhas, produzindo **4 milhões de execuções em 154 ações** e mais de **397 milhões de ações** negociadas em aproximadamente **45 minutos**. A Knight terminou com posição comprada de cerca de 3,5 bilhões de dólares em 80 ações e vendida de cerca de 3,15 bilhões em 74 ações.

O mercado sentiu. Em 75 daquelas ações, as execuções da Knight passaram de 20% do volume e moveram o preço em mais de 5%. Em 37 delas, o preço andou mais de 10% e a Knight respondeu por mais da metade do volume negociado.

## O erro que piorou tudo

Aqui está a parte mais dolorosa do documento, e a mais instrutiva para uma disciplina de governança.

A Knight não tinha procedimento de resposta a incidente. Nas palavras da SEC: *"Knight did not have supervisory procedures to guide its relevant personnel when significant issues developed."* A empresa deixou a equipe de tecnologia tentar diagnosticar o problema com o sistema em produção, negociando ao vivo.

Numa das tentativas de correção, a equipe **desinstalou o código novo dos sete servidores onde ele havia sido implantado corretamente**.

> *"This action worsened the problem, causing additional incoming parent orders to activate the Power Peg code that was present on those servers, similar to what had already occurred on the eighth server."*

A hipótese era razoável: o problema apareceu depois do deploy, então reverter o deploy deveria resolver. Estava errada, porque o defeito não estava no código novo. Estava no código antigo que o novo deveria ter apagado. Reverter transformou um servidor defeituoso em oito.

## Os controles que existiam e não pararam nada

A ordem da SEC cataloga o que havia, e é um inventário familiar.

Existiam controles de entrada de ordem errônea na interface do cliente, no sistema de gestão de ordens e no sistema de execução interna. Nenhum deles ficava no SMARS, que era o último elo antes do mercado. Não havia comparação entre o que entrava no SMARS e o que saía dele, nem procedimento para interromper o SMARS diante do próprio comportamento aberrante.

Existia um limite de posição de 2 milhões de dólares numa conta interna, a chamada Conta 33, onde as posições foram se acumulando. O limite não estava ligado a nenhum controle automático capaz de impedir novas ordens.

Existia a ferramenta principal de monitoração de risco, o **PMON**. Ela é descrita como sistema de monitoração pós-execução: mostrava as posições depois de feitas, não gerava alerta automático, não exibia os limites na tela (quem olhasse precisava saber de cor qual era o limite aplicável) e ficava lenta justamente em eventos de alto volume como aquele, produzindo relatórios imprecisos.

O padrão se repete nos três casos. O controle existia como artefato. Nenhum deles estava ligado a uma ação automática capaz de parar o sistema.

## O desfecho formal

A SEC concluiu que a Knight violou a Regra 15c3-5 do Exchange Act, a chamada regra de acesso ao mercado, em vigor desde julho de 2011. Entre as violações listadas está uma que interessa diretamente a este módulo:

> *"Knight did not have technology governance controls and supervisory procedures sufficient to ensure the orderly deployment of new code or to prevent the activation of code no longer intended for use in Knight's current operations but left on its servers that were accessing the market."*

A empresa foi censurada e pagou penalidade civil de 12 milhões de dólares — valor irrelevante diante dos 460 milhões perdidos em 45 minutos. A certificação anual do executivo-chefe para 2012 foi considerada defeituosa porque não atestava a conformidade exigida pela regra.

## Questões para discussão

Releia o caso com a lente do arquiteto. As questões abaixo pedem recuperar os fatos, explicar os mecanismos e comparar as escolhas descritas no próprio caso.

**1.** Reconstrua a cronologia do caso em quatro marcos: 2003, 2005, julho de 2012 e 1º de agosto de 2012. Diga o que aconteceu em cada um.

**2.** Explique por que mover a função de quantidade acumulada, em 2005, transformou o Power Peg num defeito latente, e por que a mudança pareceu inofensiva na época.

**3.** Noventa e sete mensagens nomeando o subsistema e o defeito chegaram noventa minutos antes da abertura do mercado. Explique a diferença entre notificação e alerta que esse episódio evidencia.

**4.** A reversão do código novo nos sete servidores corretos piorou o incidente. Explique o raciocínio que levou a essa ação e identifique em que suposição ele estava errado.

**5.** Compare os três controles que existiam — o limite da Conta 33, o PMON e o teto de 9,5% no preço — quanto ao que cada um observava e ao que cada um era capaz de interromper.

## Fontes

- U.S. Securities and Exchange Commission, [In the Matter of Knight Capital Americas LLC — Release No. 34-70694, Administrative Proceeding File No. 3-15570](https://www.sec.gov/litigation/admin/2013/34-70694.pdf) — 16 de outubro de 2013. Fonte primária de toda a cronologia, de todas as citações e de todos os números deste caso.
- SEC, [Rule 15c3-5 — Risk Management Controls for Brokers or Dealers with Market Access](https://www.sec.gov/rules/final/2010/34-63241.pdf) — a regra que a Knight violou, útil para ver como um regulador descreve controles de risco em sistemas automatizados.
- NYSE, [Release No. 34-67347](https://www.sec.gov/rules/sro/nyse/2012/34-67347.pdf) — aprovação do Retail Liquidity Program, o programa cuja data de início criou o prazo do deploy.
