# Documentação Técnica — Backend do Algoritmo (Dijkstra + Heurística de Rota)

Este documento explica o que já foi implementado em
`src/algoritmos/dijkstra.py`, `src/algoritmos/matriz_distancias.py` e
`src/algoritmos/nearest_neighbor.py`, e serve como referência
para o grupo responsável pela **interface gráfica em pygame** (desenho do
mapa do mercado e simulação da rota sugerida).

O objetivo geral do backend é: dada uma lista de itens de compra, calcular
a **sequência de corredores a percorrer** e a **distância total mínima
percorrida**, usando o grafo do mercado (`dados/grafo_ponderado.json`).

---

## 1. Visão geral do pipeline

```
lista de itens (texto ou seleção numerada)
        │
        ▼
mapear_item_para_no()  -----------------  matriz_distancias.py
        │
        ▼
calcular_matriz_distancias()  -----------  matriz_distancias.py
   (roda dijkstra() uma vez por item)  ---  dijkstra.py
        │
        ▼
vizinho_mais_proximo()  -----------------  nearest_neighbor.py
   (decide a ORDEM de visita dos itens)
        │
        ▼
rota (lista de nós) + distância total
```

**Importante para a defesa do projeto (e para a interface gráfica também
deixar isso claro, se possível na tela):** Dijkstra resolve o caminho
mínimo entre dois pontos, mas **não decide a melhor ordem de visitar
vários pontos** — isso é uma variação do Problema do Caixeiro-Viajante
(TSP), NP-difícil. A solução adotada combina os dois algoritmos:

1. **Dijkstra** calcula a distância mínima entre cada par de pontos
   relevantes (itens da lista + entrada do mercado).
2. **Nearest neighbor** (heurística gulosa) usa essas distâncias para
   decidir a ordem de visita: sempre vai ao item não visitado mais
   próximo da posição atual.

O resultado é uma **rota aproximada**, não necessariamente a rota
globalmente ótima — isso é esperado e deve ser declarado, inclusive na
interface, se fizer sentido (ex: um texto "rota aproximada" ao lado do
mapa).

---

## 2. `src/algoritmos/dijkstra.py` — Grafo do mercado + caminho mínimo

### O que faz
Implementa o algoritmo de Dijkstra "na mão" (sem `networkx` ou
`scipy.sparse.csgraph.dijkstra`), usando apenas `heapq` como estrutura de
fila de prioridade. Complexidade: `O((V + E) log V)`.

### Formato dos dados
O grafo é representado como um dicionário de adjacência:
```python
grafo = {
    "P01": [("X01", 52.2), ("X02", 44.2), ...],
    "C10": [("C09", 5.7), ("C11", 8.0), ...],
    ...
}
```
Cada chave é o código de um nó (corredor, freezer, geladeira, caixa,
entrada/saída — ver `docs/tabela_mercado.md`), e o valor é a lista de
`(nó_vizinho, peso_em_metros)`.

### Funções principais

#### `carregar_grafo(caminho_json: str) -> dict`
Lê `grafo_ponderado.json` e devolve o dicionário de adjacência pronto
para uso. **Importante**: o grafo do mercado é não-dirigido, mas algumas
arestas no JSON só estão declaradas em um sentido — esta função
**simetriza** automaticamente (garante que se existe `A -> B`, também
existe `B -> A` com o mesmo peso).

```python
grafo = carregar_grafo("grafo_ponderado.json")
```

#### `dijkstra(grafo: dict, origem: str) -> (distancias, predecessores)`
Calcula a distância mínima da `origem` até **todos** os outros nós do
grafo, de uma vez só.

- `distancias`: dict `{nó: distância_mínima_em_metros}` (`math.inf` se
  inalcançável).
- `predecessores`: dict `{nó: nó_anterior_no_caminho_mínimo}` — **é isso
  que permite reconstruir o caminho completo, nó a nó**, não apenas a
  distância total.

```python
distancias, preds = dijkstra(grafo, "P01")
distancias["C10"]   # ex: 39.4  (metros, da Entrada até o corredor C10)
```

#### `reconstruir_caminho(predecessores: dict, origem: str, destino: str) -> list[str] | None`
Usa o dicionário `predecessores` (gerado por `dijkstra`) para devolver a
**sequência de nós** do caminho mínimo entre `origem` e `destino`, ex:
```python
["P01", "X04", "C08", "C09", "C10"]
```
Devolve `None` se o destino for inalcançável.

> ⚠️ **Atenção**: `predecessores` é sempre relativo a uma única `origem`.
> Se você quer o caminho completo entre `A -> B` e depois `B -> C`, você
> precisa rodar `dijkstra(grafo, "A")` para o primeiro trecho e
> `dijkstra(grafo, "B")` para o segundo (ver seção 5, abaixo, com o
> código pronto para isso).

---

## 3. `src/algoritmos/matriz_distancias.py` — Matriz de distâncias entre itens

### O que faz
1. Mapeia cada item da lista de compras (texto livre, ex: `"Leite"`) para
   o nó do grafo correspondente (ex: `"C10"`), usando a tabela de
   produtos por corredor (`tabela_mercado.md`, replicada no dicionário
   `DESCRICOES_NO`).
2. Roda `dijkstra()` **uma única vez para cada nó de interesse** (não
   para cada par!) e monta uma matriz k×k com a distância mínima entre
   todos os pares de itens + a entrada do mercado.

### Funções principais

#### `mapear_item_para_no(item: str) -> str`
Converte texto livre em código de nó, com normalização de acentos/caixa e
correspondência exata ou por substring. Também aceita o código do nó
diretamente (ex: `"C10"`).

#### `calcular_matriz_distancias(itens, grafo=None, no_entrada="P01", incluir_entrada=True) -> (matriz, nos_interesse, item_para_no)`
- `matriz`: dict de dict, `matriz[nó_a][nó_b]` = distância mínima em
  metros.
- `nos_interesse`: lista ordenada dos nós usados (entrada primeiro, se
  incluída, depois um nó por item, sem repetição).
- `item_para_no`: dict `{texto_original_do_item: nó_encontrado}` — útil
  para rotular a interface (ex: mostrar "Leite" ao lado do nó "C10").

```python
matriz, nos, item_para_no = calcular_matriz_distancias(
    ["Leite", "Batata", "Cerveja"], grafo=grafo, incluir_entrada=True
)
```

#### Catálogo numerado de itens (o que a interface de texto usa hoje)
Estas funções existem para o fluxo de terminal, mas os dados que elas
expõem (`catalogo`, `item_para_no`, `DESCRICOES_NO`) também servem de
base para uma tela de seleção de itens em pygame:

- `catalogar_itens() -> list[dict]`: gera a lista enumerada de **todos**
  os produtos do mercado (a partir de `DESCRICOES_NO`), cada entrada no
  formato `{"numero": int, "item": str, "no": str}`.
- `imprimir_catalogo_itens(catalogo=None)`: imprime a lista no terminal
  (1 a N). Não é necessária no pygame, mas `catalogar_itens()` sozinha
  já dá tudo que uma tela gráfica de seleção de produtos precisaria
  (número, nome do item, nó/corredor onde fica).
- `ler_selecao_por_numero(catalogo=None) -> list[str]`: lê a seleção do
  usuário via `input()` (modo terminal). No pygame, o equivalente seria
  capturar cliques/checkboxes na lista gerada por `catalogar_itens()` e
  montar a lista de nomes de item da mesma forma.
- `selecionar_itens_mercado() -> list[str]`: função de conveniência que
  junta as duas anteriores (fluxo de terminal completo).

#### `DESCRICOES_NO: dict`
Dicionário `{nó: "descrição, dos, produtos, do, corredor"}`, é a
representação em código de `tabela_mercado.md`. Útil para rotular os
corredores no mapa desenhado (ex: escrever "C10 — Adoçantes, Leites..."
ao lado do nó no pygame).

---

## 4. `src/algoritmos/nearest_neighbor.py` — Heurística de ordenação da rota

### O que faz
Recebe a matriz de distâncias (de `matriz_distancias.py`) e decide a
**ordem** de visita dos itens: partindo do ponto atual, sempre vai ao
item não visitado mais próximo. É uma aproximação gulosa — **não** é a
rota ótima (isso seria TSP). Complexidade: `O(k²)` para `k` itens.

Critério de desempate (quando dois itens estão à mesma distância):
escolhe o de **menor código de nó em ordem alfabética**, o que torna o
resultado determinístico (mesma entrada → sempre a mesma rota).

### Função principal

#### `vizinho_mais_proximo(matriz, no_partida, nos_a_visitar=None) -> (rota, distancia_total)`
- `rota`: lista de nós na ordem em que devem ser visitados (**não**
  inclui `no_partida`).
- `distancia_total`: soma das distâncias de cada perna da rota, em
  metros.

```python
rota, distancia_total = vizinho_mais_proximo(matriz, "P01", itens_nos)
# rota: ["C01", "C17", "C10", "F03"]
# distancia_total: 76.2
```

#### `imprimir_rota(rota, distancia_total, item_para_no, no_partida)`
Imprime a rota no terminal de forma legível, com o nome do item ao lado
do nó (usa `item_para_no`, vindo de `calcular_matriz_distancias`). Não é
necessária no pygame — a lógica de exibição lá será o próprio mapa
desenhado.

---

## 5. Guia para a equipe de interface gráfica (pygame)

### 5.1 Dados que vocês vão precisar

| Dado | Onde está | Para que serve |
|---|---|---|
| Coordenadas (x, y) de cada nó, em metros | `dados/grafo_ponderado.json` → chave `"coordenadas"` (ou dict `coordenadas` em `dados/grafo_ponderado.py`) | Posicionar cada corredor/freezer/geladeira/caixa no mapa desenhado |
| Dimensões do mercado | `dados/grafo_ponderado.json` → `"metadata"."dimensoes_mercado"` (`"72m x 30m"`) | Definir a escala metros → pixels da tela |
| Grafo de adjacência | `carregar_grafo("dados/grafo_ponderado.json")` | Desenhar as arestas (corredores conectando os nós) e calcular caminhos |
| Descrição de produtos por nó | `DESCRICOES_NO` (`matriz_distancias.py`) ou `tabela_mercado.md` | Rotular os corredores no mapa e montar uma tela de seleção de itens |

Como as coordenadas já vêm em metros com origem no canto superior
esquerdo (ver comentário em `grafo_ponderado.py`), a conversão para
pixels é simples:
```python
ESCALA = 10  # pixels por metro, ajustem conforme o tamanho da janela
def para_pixel(x_metros, y_metros):
    return x_metros * ESCALA, y_metros * ESCALA
```

### 5.2 Sequência de chamadas para obter a rota completa

```python
from dijkstra import carregar_grafo, dijkstra, reconstruir_caminho
from matriz_distancias import calcular_matriz_distancias, selecionar_itens_mercado
from nearest_neighbor import vizinho_mais_proximo

grafo = carregar_grafo("grafo_ponderado.json")

# 1) obter a lista de itens (pode reaproveitar selecionar_itens_mercado()
#    para prototipar rápido, ou substituir por uma tela gráfica de
#    seleção usando catalogar_itens() como fonte dos dados)
lista_de_compras = selecionar_itens_mercado()

# 2) matriz de distâncias entre entrada + itens
matriz, nos_interesse, item_para_no = calcular_matriz_distancias(
    lista_de_compras, grafo=grafo, incluir_entrada=True
)
itens_nos = [no for no in nos_interesse if no != "P01"]

# 3) ordem de visita (heurística) + distância total
rota, distancia_total = vizinho_mais_proximo(matriz, "P01", itens_nos)
```

Neste ponto vocês já têm `rota` (ex: `["C01", "C17", "C10", "F03"]`) e
`distancia_total` (em metros) — suficiente para mostrar a **ordem** dos
pontos no mapa e o número final de metros percorridos.

### 5.3 Reconstruindo o caminho nó a nó (para desenhar/animar o trajeto real)

`rota` só dá os **pontos de parada** (os itens), não o caminho físico
passo a passo entre eles (ex: quais corredores intermediários o cliente
atravessa entre C01 e C17). Para isso, é preciso rodar `dijkstra()` e
`reconstruir_caminho()` **para cada perna da rota**, porque
`predecessores` é sempre relativo a uma origem específica:

```python
pontos = ["P01"] + rota  # inclui o ponto de partida (entrada)
caminho_completo = []

for i in range(len(pontos) - 1):
    origem, destino = pontos[i], pontos[i + 1]
    _, preds = dijkstra(grafo, origem)
    trecho = reconstruir_caminho(preds, origem, destino)
    if i > 0:
        trecho = trecho[1:]  # evita repetir o nó de junção entre pernas
    caminho_completo.extend(trecho)

# caminho_completo agora é a lista COMPLETA de nós a percorrer,
# na ordem exata, pronta para animar no pygame:
# ["P01", "X04", "C08", "C09", "C10", "C11", ..., "F03"]
```

Com `caminho_completo`, o grupo de interface pode:
- Desenhar uma linha ligando os pontos, na ordem, sobre o mapa.
- Animar um "cursor"/ícone de carrinho se movendo de nó em nó (usando
  `para_pixel()` da seção 5.1 para converter cada nó em posição de
  tela).
- Destacar visualmente os pontos de parada (itens da lista) de forma
  diferente dos nós apenas "de passagem".

### 5.4 Resumo das funções reutilizáveis (evitar duplicar lógica)

| Função | Arquivo | Uso na interface gráfica |
|---|---|---|
| `carregar_grafo()` | `dijkstra.py` | Carregar o grafo uma vez no início do programa |
| `dijkstra()` | `dijkstra.py` | Obter distâncias/predecessores a partir de um nó (necessário por perna da rota, ver 5.3) |
| `reconstruir_caminho()` | `dijkstra.py` | Obter a sequência de nós entre dois pontos, para desenhar o trajeto real |
| `catalogar_itens()` | `matriz_distancias.py` | Fonte de dados para uma tela gráfica de seleção de produtos (número, nome, nó) |
| `DESCRICOES_NO` | `matriz_distancias.py` | Rotular corredores/produtos no mapa |
| `calcular_matriz_distancias()` | `matriz_distancias.py` | Obter a matriz de distâncias a partir da lista de itens escolhida na tela |
| `vizinho_mais_proximo()` | `nearest_neighbor.py` | Obter a ordem de visita (rota) e a distância total |

Não é necessário reimplementar nenhuma lógica de cálculo de distância ou
de ordenação — basta importar essas funções nos módulos do pygame e
consumir os dados que elas retornam (listas de nós e números de
distância) para desenhar e animar.

---

## 6. Observações finais

- O grafo tem **51 nós** e (após simetrização) até **168 arestas**
  bidirecionais, cobrindo corredores, freezers, geladeiras, açougue,
  hortifruti, caixas e entrada/saída (ver `grafo_ponderado.json` e
  `tabela_mercado.md` para a legenda completa de cada nó).
- Toda a lógica de cálculo (Dijkstra, matriz de distâncias, heurística)
  já está testada com verificações automáticas (simetria, desigualdade
  triangular, determinismo da heurística, alcançabilidade de todos os
  nós) — rodáveis com `python -m src.algoritmos.dijkstra`, `python -m
  src.algoritmos.matriz_distancias --teste` e `python -m
  src.algoritmos.nearest_neighbor --teste`.
- A interface gráfica não precisa reimplementar nada do cálculo: o
  trabalho dela é **ler os retornos** dessas funções (listas de nós,
  distâncias em metros) e traduzir isso em desenho/animação na tela.
