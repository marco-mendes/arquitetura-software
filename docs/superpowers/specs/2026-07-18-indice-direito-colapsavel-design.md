# Índice direito colapsável — desenho

## Objetivo

Permitir que a pessoa estudante recolha o índice de títulos exibido à direita das páginas do portal, liberando largura para a leitura sem perder a possibilidade de navegar pelos títulos da página.

## Comportamento

- Em telas de desktop, o índice abre visível, como hoje.
- Um botão acessível, posicionado junto ao índice, alterna entre os rótulos **Recolher índice** e **Mostrar índice**.
- Ao recolher, o painel deixa de ocupar a coluna lateral e o conteúdo central pode usar a largura liberada.
- A escolha é armazenada apenas no navegador da pessoa usuária e é reaplicada quando ela navega para outra página do portal.
- O botão informa corretamente o estado expandido para tecnologias assistivas e pode ser acionado por teclado.
- Em telas em que o tema já não exibe o índice direito, a melhoria não introduz botão, espaço vazio ou alteração de navegação.

## Implementação proposta

Criar um pequeno JavaScript próprio do portal que, após cada carregamento de página (inclusive com a navegação instantânea do Material for MkDocs), localiza o índice secundário do tema e acrescenta o botão de alternância. Uma classe no elemento raiz representa o estado recolhido; regras CSS específicas para desktop ocultam o painel e permitem que a coluna de conteúdo se expanda. O estado é persistido em `localStorage` com uma chave exclusiva do curso.

Não serão alterados os textos didáticos, a navegação principal à esquerda, a tipografia, a paleta ou a experiência móvel existente.

## Critérios de aceitação

1. Em uma página com títulos, o índice aparece aberto no primeiro acesso.
2. O botão recolhe e restaura o índice sem recarregar a página.
3. O conteúdo ganha a largura correspondente quando o índice está recolhido.
4. O rótulo e o atributo `aria-expanded` acompanham o estado atual.
5. Depois de navegar para outra página, o estado escolhido permanece.
6. Em viewport móvel, o índice e o botão adicional não aparecem.
7. O build estrito do MKDocs e os testes editoriais existentes continuam aprovados.
