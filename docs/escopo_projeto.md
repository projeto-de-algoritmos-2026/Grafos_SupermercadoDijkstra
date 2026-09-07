# Otimização de Trajeto de Compras em Supermercado com Dijkstra

## 1. Problema

Um cliente entra em um supermercado com uma lista de N itens a comprar. Os itens estão espalhados em corredores diferentes, e o cliente normalmente percorre o mercado de forma desordenada, gerando deslocamento maior do que o necessário. O objetivo é reduzir a distância total percorrida dado um conjunto de itens a coletar.

## 2. Delimitação do escopo (o que Dijkstra resolve e o que não resolve)

Isso precisa estar explícito no relatório e na apresentação, não escondido:

- **O que Dijkstra resolve corretamente**: dado um ponto de origem no grafo do mercado, a distância mínima até qualquer outro ponto (ou entre dois pontos específicos).
- **O que Dijkstra NÃO resolve**: a ordem ótima de visita de múltiplos pontos (itens da lista) para minimizar o percurso total. Isso é uma variação do Problema do Caixeiro-Viajante (TSP), NP-difícil na forma geral.
- **Solução adotada**: Dijkstra calcula as distâncias par a par entre todos os itens da lista (e do ponto de entrada/caixa). Uma heurística gulosa (nearest neighbor) usa essas distâncias para montar uma rota aproximada, sempre indo ao item não visitado mais próximo da posição atual.
- **Consequência a declarar na arguição**: a rota gerada é uma aproximação razoável, não a rota globalmente ótima. Isso é esperado e correto de se admitir; o contrário (afirmar otimalidade sem prova) é o erro que enfraquece a defesa.

## 3. Modelagem do grafo

- **Nós**: cruzamentos de corredores, pontos de entrada, caixas, e a localização de cada categoria/item de produto.
- **Arestas**: trechos de corredor entre nós adjacentes, com peso = distância física (metros) ou tempo estimado de deslocamento.
- **Grafo não dirigido** (na maioria dos mercados o cliente pode andar nos dois sentidos do corredor), exceto se o layout tiver corredores de sentido único (alguns mercados grandes têm isso em certas seções).
- **Fonte do dado de layout**: planta baixa real de um mercado (se algum membro do grupo tiver acesso) ou um layout desenhado à mão com justificativa de que reflete uma estrutura plausível de mercado real (corredores em grade, seções por categoria).

## 4. Solução técnica, por etapa

1. **Construção do grafo**: representar o mercado como grafo ponderado (matriz de adjacência ou lista de adjacência, dependendo do tamanho).
2. **Entrada do usuário**: lista de itens desejados, mapeados para nós do grafo (cada item já tem localização conhecida no grafo).
3. **Cálculo de distâncias**: rodar Dijkstra a partir de cada item da lista (e do ponto de entrada) para obter a matriz de distâncias mínimas entre todos os pares relevantes.
4. **Ordenação heurística**: aplicar nearest neighbor sobre a matriz de distâncias para definir a sequência de visita.
5. **Saída**: rota sugerida (sequência de itens) e visualização do caminho sobre o grafo/planta do mercado.

## 5. Dados necessários

- Layout do mercado (planta baixa real ou desenhada) com nós e distâncias entre eles.
- Mapeamento de produto → localização (corredor/seção).
- Lista de compras de teste (real ou simulada) para validar o sistema.

## 6. Validação e critérios de teste

- Comparar o resultado da heurística contra a solução ótima calculada por força bruta em listas pequenas (até ~10 itens, onde testar todas as permutações é viável), para medir o quão longe a heurística fica do ótimo.
- Testar com grafos de tamanhos diferentes para observar o comportamento do tempo de execução do Dijkstra (complexidade O((V+E) log V) com heap).
- Documentar casos em que a heurística falha feio (por exemplo, quando o item mais próximo geograficamente está em direção oposta ao restante da lista, gerando zigue-zague).

## 7. Pontos em aberto para o grupo decidir

- Layout real de mercado (dado de verdade) ou layout desenhado por vocês com justificativa de plausibilidade.
- Interface: visualização gráfica do grafo/rota (mais trabalho, mais impacto visual) ou saída em texto/lista ordenada (mais simples, mais tempo para o núcleo do algoritmo).
- Tamanho do grafo de teste: um mercado pequeno é mais fácil de validar manualmente, mas um mercado maior demonstra melhor a necessidade real do algoritmo.
