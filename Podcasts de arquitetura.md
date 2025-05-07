# Lista curada de podcasts sobre casos reais de arquitetura

## Introdução a Microsserviços - Artigo de James Lewis e Martin Fowler 

<img width="500" alt="image" src="https://github.com/user-attachments/assets/e1828cb3-abd2-495e-a885-2b2f0e848375" />


* [Podcast de 10 min com o resumo do artigo](https://tinyurl.com/2s3m3yew)  
* [Artigo original](https://martinfowler.com/articles/microservices.html)

---
  

## Time de Engenharia da Halo 

<img width="500" alt="image" src="image.png" />

Durante o desenvolvimento de Halo 4, a equipe de engenharia enfrentou desafios de escala sem precedentes, nunca antes encontrados em títulos anteriores da franquia.

Halo 4 experimentou um nível de engajamento impressionante:

- Mais de 1,5 bilhão de partidas foram jogadas.

- Mais de 11,6 milhões de jogadores únicos se conectaram e competiram online.

Cada partida gerava dados de telemetria detalhados para cada jogador: abates, assistências, mortes, uso de armas, medalhas e diversas outras estatísticas relacionadas ao jogo. Essas informações precisavam ser ingeridas, processadas, armazenadas e disponibilizadas em diversos serviços, tanto para feedback em tempo real no próprio jogo quanto para plataformas externas de análise, como o Halo Waypoint.

A complexidade aumentou ainda mais porque uma única partida podia envolver de 1 a 32 jogadores. Para cada sessão de jogo, as estatísticas precisavam ser atualizadas de forma confiável em vários registros de jogadores simultaneamente, preservando a precisão e a consistência dos dados.

Como o padrão SAGA ajudou a equipe a escalar a sua arquitetura.

* Podcast de 8 min do [padrão Saga na empresa Halo (Nível Básico)](https://tinyurl.com/2s3hk3k8)  
* Podcast de 9 min do [padrão Saga na empresa Halo (Nível Avançado)](https://tinyurl.com/37nau36s)  
* Artigo complementar com o [descritivo textual do caso](https://substack.com/home/post/p-162718539).  
