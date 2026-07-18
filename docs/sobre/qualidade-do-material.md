# Qualidade do material

O material público é revisado como conteúdo didático e como projeto executável. Antes de uma publicação, execute as verificações a seguir a partir da raiz do repositório. Elas não substituem a leitura crítica de uma atividade nem a observação de uma oficina em aula.

## Verificações de publicação

1. Verifique a estrutura, os contratos editoriais e os testes de regressão:

   ```bash
   python -m unittest discover -s tests -v
   ```

2. Verifique links, figuras, Taxonomia de Bloom, critérios de avaliação, extensão editorial e a construção estática:

   ```bash
   python scripts/validate_content.py --all
   python -m mkdocs build --strict
   ```

3. Verifique o código de referência da plataforma hospitalar:

   ```bash
   python -m pytest laboratorios/plataforma-hospitalar/tests -q
   ```

4. Verifique se as três pilhas locais possuem configuração Compose válida:

   ```bash
   docker compose -f laboratorios/plataforma-hospitalar/infra/compose.servicos.yml config --quiet
   docker compose -f laboratorios/plataforma-hospitalar/infra/compose.governanca.yml config --quiet
   docker compose -f laboratorios/plataforma-hospitalar/infra/compose.eventos.yml config --quiet
   ```

## Sistemas e execução local

As oficinas descrevem caminhos para Windows, macOS e Linux. Elas usam ferramentas locais e de código aberto, como Python, Docker Engine com Compose, Bruno, RabbitMQ, Kong, OpenTelemetry e kind. Cada página informa seus pré-requisitos e uma contingência quando o ambiente não estiver disponível.

O código de referência está em Python para tornar a execução comum à turma. Os conceitos, contratos e evidências também indicam equivalentes em Java e .NET. Uma oficina não deve pressupor que o estudante possa alterar configurações globais do sistema ou remover recursos de outros projetos.

## Figuras e acessibilidade

Imagens didáticas são arquivos locais versionados em `docs/assets/images/`. Toda figura recebe texto alternativo e uma leitura textual logo após a figura; assim, a relação arquitetural permanece compreensível quando a imagem não é exibida. Diagramas Mermaid recebem a mesma leitura textual.

Os prompts que originaram os infográficos ficam em [prompts das imagens](../assets/images/prompts.md). Ao substituir uma figura, mantenha o idioma português, verifique legibilidade em tela estreita e atualize texto alternativo, leitura textual e prompt. Não use dados reais de pacientes, profissionais ou organizações nas imagens e exemplos.

## Respostas, exemplos e critérios de avaliação

Os exercícios de Recordar e Compreender podem oferecer apoio direto quando ele ajuda a consolidar vocabulário. Nos níveis Aplicar, Analisar e Avaliar, o material apresenta situação, papel, insumos, condução e entrega esperada, mas não publica uma resposta única para o cenário. Os critérios de avaliação descrevem o que observar e os percentuais relativos de cada aspecto.

A revisão editorial garante a rastreabilidade das fontes que fundamentam cada capítulo, respostas expansíveis para apoiar estudantes em níveis iniciais, contexto completo — situação, papel, insumos, condução e entrega — nas atividades avançadas e acessibilidade das figuras por meio de texto alternativo e leitura textual. Essas garantias permitem verificar a origem do conteúdo e compreender as atividades e relações arquiteturais sem depender apenas de uma imagem ou de conhecimento prévio.

Gabaritos, notas de condução e observações de turma pertencem ao material do professor, mantido fora do site público e do controle de versão. Os exemplos públicos usam dados sintéticos e devem declarar suas limitações quando não representam uma topologia de produção.

## Como reportar uma correção

Abra uma issue no repositório com o link da página, uma descrição breve do problema e, quando houver oficina, o sistema operacional, a versão da ferramenta e os passos que permitem reproduzi-lo. Para um erro de conteúdo, informe também o trecho e a correção proposta. Para uma figura, descreva o que ficou ilegível ou qual relação arquitetural não está clara.

Não inclua segredos, credenciais, dados clínicos, capturas de tela com informação identificável ou arquivos internos de aula. Uma correção é revisada com as verificações pertinentes e com a atualização da leitura textual ou do procedimento quando isso for necessário.
