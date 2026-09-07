"""
Implementação do algoritmo de Dijkstra (sem usar bibliotecas prontas de
caminho mínimo, ex: networkx.shortest_path ou scipy.sparse.csgraph.dijkstra).

Usamos apenas `heapq`, que é somente uma estrutura de dados de heap binário
(fila de prioridade) da biblioteca padrão do Python -- o algoritmo de
Dijkstra em si (relaxamento de arestas, controle de visitados, etc.) é
implementado manualmente abaixo.

Grafo de entrada: dicionário de adjacência no formato
    {
        "NO": [("VIZINHO", peso), ("VIZINHO2", peso2), ...],
        ...
    }
compatível com o `adjacencias` de grafo_ponderado.json.
"""

import heapq
import json
import math


# ---------------------------------------------------------------------------
# 1. Carregamento e normalização do grafo
# ---------------------------------------------------------------------------


def carregar_grafo(caminho_json: str) -> dict:
    """Lê o grafo_ponderado.json e devolve o dicionário de adjacência.

    O grafo do mercado é NÃO DIRIGIDO (ver escopo_projeto.md, seção 3), mas
    algumas linhas do JSON só declaram a aresta em um dos dois sentidos.
    Para garantir consistência, simetrizamos aqui: toda aresta (u, v, w)
    lida passa a existir também como (v, u, w).
    """
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    bruto = dados["adjacencias"]
    grafo = {no: {} for no in bruto}  # no -> {vizinho: peso}

    for origem, vizinhos in bruto.items():
        # Suporta tanto lista de pares quanto dicionário aninhado no JSON
        itens_vizinhos = vizinhos.items() if isinstance(vizinhos, dict) else vizinhos

        for destino, peso in itens_vizinhos:
            # garante que ambos os nós existam no dicionário
            grafo.setdefault(origem, {})
            grafo.setdefault(destino, {})

            # se já existir uma aresta (ex: declarada nos dois sentidos com
            # pesos levemente diferentes por arredondamento), mantemos o
            # menor peso, que é o correto para efeitos de menor caminho.
            if destino not in grafo[origem] or peso < grafo[origem][destino]:
                grafo[origem][destino] = peso
            if origem not in grafo[destino] or peso < grafo[destino][origem]:
                grafo[destino][origem] = peso

    # devolve no formato de lista de tuplas (mais próximo do arquivo original)
    return {no: list(vizinhos.items()) for no, vizinhos in grafo.items()}


# ---------------------------------------------------------------------------
# 2. Dijkstra
# ---------------------------------------------------------------------------


def dijkstra(grafo: dict, origem: str):
    """Calcula a distância mínima da `origem` até todos os outros nós.

    Parâmetros
    ----------
    grafo : dict
        Dicionário {no: [(vizinho, peso), ...]}. Pesos devem ser >= 0.
    origem : str
        Nó de partida.

    Retorna
    -------
    (distancias, predecessores)
        distancias: dict {no: menor_distancia} (math.inf se inalcançável)
        predecessores: dict {no: no_anterior_no_caminho_minimo}, usado para
        reconstruir a rota com `reconstruir_caminho`.
    """
    if origem not in grafo:
        raise ValueError(f"Nó de origem '{origem}' não existe no grafo.")

    # 2.1 Inicialização: todas as distâncias começam em infinito, exceto a origem
    distancias = {no: math.inf for no in grafo}
    distancias[origem] = 0.0
    predecessores = {no: None for no in grafo}
    visitados = set()

    # 2.2 Fila de prioridade (min-heap) com (distancia_acumulada, nó)
    # heapq é só a estrutura de heap; o controle de relaxamento de arestas,
    # de nós visitados e de atualização de distâncias é feito manualmente.
    fila = [(0.0, origem)]

    while fila:
        dist_atual, u = heapq.heappop(fila)

        # nó já foi finalizado com uma distância menor -> entrada obsoleta, ignora
        if u in visitados:
            continue
        visitados.add(u)

        # 2.3 Relaxamento das arestas de u
        for v, peso in grafo.get(u, []):
            if peso < 0:
                raise ValueError("Dijkstra não suporta pesos negativos.")
            nova_dist = dist_atual + peso
            if nova_dist < distancias[v]:
                distancias[v] = nova_dist
                predecessores[v] = u
                heapq.heappush(fila, (nova_dist, v))

    return distancias, predecessores


def reconstruir_caminho(predecessores: dict, origem: str, destino: str):
    """Reconstrói a sequência de nós do caminho mínimo origem -> destino."""
    if destino not in predecessores:
        return None
    caminho = []
    no = destino
    while no is not None:
        caminho.append(no)
        if no == origem:
            break
        no = predecessores[no]
    caminho.reverse()
    if caminho[0] != origem:
        return None  # destino inalcançável a partir da origem
    return caminho


# ---------------------------------------------------------------------------
# 3. Testes com o grafo do mercado (grafo_ponderado.json)
# ---------------------------------------------------------------------------


def _fmt(v):
    return "inf" if v == math.inf else f"{v:.1f}m"


def testar_com_grafo_do_mercado(caminho_json="grafo_ponderado.json"):
    grafo = carregar_grafo(caminho_json)
    print(f"Grafo carregado: {len(grafo)} nós.\n")

    # ---- Teste 1: origem = P01 (Entrada) ------------------------------
    origem = "P01"
    distancias, preds = dijkstra(grafo, origem)
    print(f"=== Distâncias mínimas a partir de {origem} (Entrada) ===")
    for no in sorted(distancias):
        print(f"  {origem} -> {no}: {_fmt(distancias[no])}")

    # Sanity checks básicos
    assert distancias[origem] == 0.0, "distância da origem a ela mesma deve ser 0"
    assert all(d >= 0 for d in distancias.values()), (
        "distâncias não podem ser negativas"
    )
    print("\n[OK] Distância da origem a si mesma é 0.")
    print("[OK] Nenhuma distância negativa encontrada.")

    # Todos os nós devem ser alcançáveis (grafo conectado)
    inalcancaveis = [no for no, d in distancias.items() if d == math.inf]
    if inalcancaveis:
        print(f"[AVISO] Nós inalcançáveis a partir de {origem}: {inalcancaveis}")
    else:
        print(
            f"[OK] Todos os {len(distancias)} nós são alcançáveis a partir de {origem}."
        )

    # Caminho reconstruído até um item específico, ex: M05 (morango/uva)
    destino = "M05"
    caminho = reconstruir_caminho(preds, origem, destino)
    print(
        f"\nCaminho mínimo {origem} -> {destino}: {' -> '.join(caminho)}"
        f"  (distância total: {_fmt(distancias[destino])})"
    )

    # ---- Teste 2: valida contra aresta direta conhecida (G01 <-> M01 = 2.0m)
    d2, _ = dijkstra(grafo, "G01")
    assert d2["M01"] == 2.0, f"esperado 2.0m entre G01 e M01, obtido {d2['M01']}"
    print("\n[OK] Dijkstra(G01)['M01'] == 2.0m (bate com a aresta direta do grafo).")

    # ---- Teste 3: simetria -- distância(A,B) deve ser igual a distância(B,A)
    # (grafo não dirigido)
    d_g01, _ = dijkstra(grafo, "G01")
    d_x03, _ = dijkstra(grafo, "X03")
    assert abs(d_g01["X03"] - d_x03["G01"]) < 1e-9, (
        "grafo não dirigido: distâncias devem ser simétricas"
    )
    print(
        f"[OK] Simetria verificada: dist(G01,X03) == dist(X03,G01) == {_fmt(d_g01['X03'])}."
    )

    # ---- Teste 4: desigualdade triangular em uma amostra de nós
    amostra = ["P01", "P02", "A01", "C01", "M05", "F09", "X05"]

    # Otimização: precalcula Dijkstra para cada nó da amostra 1 única vez
    distancias_amostra = {node: dijkstra(grafo, node)[0] for node in amostra}

    falhas = 0
    for a in amostra:
        for b in amostra:
            for c in amostra:
                if (
                    distancias_amostra[a][b] + distancias_amostra[b][c]
                    < distancias_amostra[a][c] - 1e-6
                ):
                    falhas += 1
    assert falhas == 0, "desigualdade triangular violada"
    print(
        "[OK] Desigualdade triangular satisfeita na amostra testada "
        "(dist(a,c) <= dist(a,b) + dist(b,c))."
    )

    print("\nTodos os testes passaram.")
    return grafo, distancias, preds


if __name__ == "__main__":
    testar_com_grafo_do_mercado("grafo_ponderado.json")
