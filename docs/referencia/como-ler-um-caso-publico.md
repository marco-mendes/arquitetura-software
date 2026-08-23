# Como ler um caso público

Cada módulo desta disciplina tem uma página de casos reais. Elas descrevem arquiteturas de empresas existentes, documentadas por elas próprias, pelo fornecedor envolvido ou em publicação revisada por pares. Esta página explica como lê-las, e serve igualmente para qualquer relato que você encontre fora daqui.

## Por que um caso público engana com facilidade

Relatos de arquitetura são publicados por quem venceu. A empresa conta a decisão que deu certo, raramente as tentativas anteriores, e quase nunca o custo organizacional de sustentar o resultado. O fornecedor de nuvem que assina o estudo tem interesse comercial no desfecho. O engenheiro que apresenta em conferência descreve o estado final de uma migração de anos como se fosse escolha tomada numa reunião.

Some-se o efeito de reescrita. À medida que um caso circula em blogs, vídeos e resumos, ganha números arredondados, citações que ninguém consegue rastrear e nomes de sistemas que a empresa nunca usou. A página de [casos reais do Módulo 3](../modulo-3-servicos/casos-reais.md#o-que-circula-sem-fonte-verificavel) registra exemplos concretos disso.

Um caso público serve para reconhecer uma força em ação e formular perguntas melhores sobre o próprio sistema. Ele não transfere a decisão, porque a decisão dependia de restrições que você não tem.

## As cinco perguntas

As páginas de casos reais seguem esta sequência. Use-a também quando ler um relato por conta própria.

**Restrição.** Qual pressão concreta forçou a mudança? Volume, prazo, indisponibilidade recorrente, custo, obrigação regulatória ou tamanho da equipe. Sem uma restrição nomeada, o relato é propaganda.

**Decisão.** O que foi decidido em termos de estrutura, propriedade de dados, forma de comunicação e desenho das equipes. Nome de produto não é decisão arquitetural.

**Consequência aceita.** Toda escolha compra uma coisa e paga com outra. Um relato honesto declara o que piorou.

**Evidência.** Que dado sustenta o resultado, e quem publicou esse dado. Número sem data de apuração e sem autor identificado vale como ordem de grandeza, e falha como citação.

**Limite de transferência.** Que característica do contexto original está ausente no seu, e o que isso invalida.

## Classificação das fontes

As páginas desta disciplina distinguem três níveis, e você deveria fazer o mesmo nos seus documentos de decisão.

| Nível | O que é | Como tratar |
| --- | --- | --- |
| Primária | Publicação da própria empresa, artigo revisado por pares, repositório ou documentação oficial | Citável com atribuição direta |
| Quase primária | Relato assinado por quem participou, publicado em livro técnico, entrevista ou apresentação | Citável, identificando o autor e o veículo |
| Secundária | Blog de terceiro, resumo, notícia, vídeo explicativo | Serve para localizar a fonte original, e falha como citação |

Um estudo de caso publicado pelo fornecedor de nuvem que vendeu a solução é fonte primária quanto à autoria e material comercial quanto ao interesse. As duas coisas ao mesmo tempo. Ele diz o que a empresa autorizou a divulgar, sem auditoria externa.

## O que não fazer com um caso

Não copie a topologia. A quantidade de serviços, a escolha de banco e a plataforma de mensageria de uma empresa refletem escala, história e organização que você não tem.

Não copie a plataforma de ferramentas. Bibliotecas envelhecem, e uma que era padrão de fato em 2015 pode estar em modo de manutenção hoje. A página do Módulo 3 traz um exemplo disso.

Não use o número da empresa como meta da sua. "Reduzimos custo em 90%" descreve a distância entre a arquitetura anterior daquela empresa e a nova. Sem conhecer a base de comparação, o percentual não se transfere.

O que se transfere é a força: a razão pela qual a decisão fez sentido naquele contexto, e o critério que permite verificar se ela faz sentido no seu.
