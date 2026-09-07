"""
Heurística gulosa de nearest neighbor (vizinho mais próximo).

Recebe a matriz de distâncias mínimas calculada na issue #6
(`calcular_matriz_distancias`, em matriz_distancias.py) e decide a ORDEM
de visita dos itens: partindo da posição atual, sempre vai ao item não
visitado mais próximo.

Isso NÃO garante a rota ótima (isso seria TSP, NP-difícil -- ver
escopo_projeto.md, seção 2), apenas uma aproximação razoável e barata de
calcular: O(k^2) comparações para k itens.

Critério de desempate: quando dois (ou mais) itens não visitados estão à
mesma distância do ponto atual, escolhe-se o de MENOR código de nó em
ordem alfabética (ex.: entre "C02" e "C20" empatados, escolhe "C02").
Isso torna o resultado 100% determinístico -- rodar a heurística duas
vezes com a mesma entrada sempre produz a mesma rota.
"""

import sys

try:
    from .matriz_distancias import (
        DESCRICOES_NO,
        calcular_matriz_distancias,
        ler_lista_de_compras,
        selecionar_itens_mercado,
    )
    from .dijkstra import CAMINHO_GRAFO, carregar_grafo
except ImportError:
    from matriz_distancias import (
        DESCRICOES_NO,
        calcular_matriz_distancias,
        ler_lista_de_compras,
        selecionar_itens_mercado,
    )
    from dijkstra import CAMINHO_GRAFO, carregar_grafo


# ---------------------------------------------------------------------------
# 1. Heurística de nearest neighbor
# ---------------------------------------------------------------------------


def vizinho_mais_proximo(
    matriz: dict,
    no_partida: str,
    nos_a_visitar: list | None = None,
):
    """Decide a ordem de visita dos nós, sempre indo ao mais próximo.

    Parâmetros
    ----------
    matriz : dict[str, dict[str, float]]
        Matriz de distâncias completa (saída de `calcular_matriz_distancias`),
        deve conter `no_partida` e todos os nós de `nos_a_visitar` como
        linhas/colunas.
    no_partida : str
        Nó de onde a rota começa (ex.: "P01", ponto de entrada).
    nos_a_visitar : list[str], opcional
        Nós que precisam ser visitados (os itens da lista de compras).
        Se None, usa todas as chaves da matriz exceto `no_partida`.

    Retorna
    -------
    rota : list[str]
        Sequência de nós na ordem em que devem ser visitados (NÃO inclui
        `no_partida` -- ele é só o ponto de partida, não um item a comprar).
    distancia_total : float
        Soma das distâncias de cada perna da rota (partida -> 1º item ->
        2º item -> ... -> último item), em metros.
    """
    if no_partida not in matriz:
        raise ValueError(f"Nó de partida '{no_partida}' não está na matriz.")

    if nos_a_visitar is None:
        nos_a_visitar = [no for no in matriz if no != no_partida]

    for no in nos_a_visitar:
        if no not in matriz:
            raise ValueError(f"Nó '{no}' não está na matriz de distâncias.")

    nao_visitados = set(nos_a_visitar)
    # nó de partida não deve ser "visitado" como se fosse um item da lista
    nao_visitados.discard(no_partida)

    atual = no_partida
    rota = []
    distancia_total = 0.0

    while nao_visitados:
        # escolhe o não-visitado mais próximo de 'atual'.
        # chave de ordenação (distância, nó): em caso de empate na distância,
        # o `min` usa o segundo elemento da tupla (o código do nó) como
        # desempate -> ordem alfabética, de forma determinística.
        proximo = min(nao_visitados, key=lambda no: (matriz[atual][no], no))

        distancia_total += matriz[atual][proximo]
        rota.append(proximo)
        nao_visitados.remove(proximo)
        atual = proximo

    return rota, distancia_total


# ---------------------------------------------------------------------------
# 2. Exibição amigável da rota
# ---------------------------------------------------------------------------


def imprimir_rota(
    rota: list, distancia_total: float, item_para_no: dict, no_partida: str
):
    no_para_itens = {}
    for item, no in item_para_no.items():
        no_para_itens.setdefault(no, []).append(item)

    def rotulo(no):
        itens = no_para_itens.get(no)
        return f"{no} ({', '.join(itens)})" if itens else no

    print(f"Ponto de partida: {no_partida} (Entrada)")
    for i, no in enumerate(rota, start=1):
        print(f"  {i}. {rotulo(no)}")
    print(f"Distância total percorrida: {distancia_total:.1f}m")


# ---------------------------------------------------------------------------
# 3. Suíte de testes fixa (regressão) -- com pelo menos 3 listas de compras
#    diferentes + caso de empate. Rodar com `--teste`.
# ---------------------------------------------------------------------------


def _executar_testes_regressao():
    grafo = carregar_grafo(CAMINHO_GRAFO)

    listas_de_teste = {
        "Lista 1 - compras variadas": [
            "Leite",
            "Batata",
            "Frango",
            "Sabonete",
            "Macarrao",
            "Cerveja",
        ],
        "Lista 2 - churrasco": [
            "Picanha",
            "Cerveja",
            "Sabao em Po",
            "Carvao",
            "Limao",
            "Azeite",
        ],
        "Lista 3 - café da manhã": [
            "Cafe",
            "Leite em Po",
            "Biscoitos",
            "Laranja",
            "Papel Toalha",
        ],
    }

    for titulo, lista in listas_de_teste.items():
        print("=" * 70)
        print(titulo)
        print("=" * 70)
        print(f"Lista de compras: {lista}\n")

        matriz, nos_interesse, item_para_no = calcular_matriz_distancias(
            lista, grafo=grafo, incluir_entrada=True
        )
        itens_nos = [no for no in nos_interesse if no != "P01"]

        rota, distancia_total = vizinho_mais_proximo(matriz, "P01", itens_nos)

        imprimir_rota(rota, distancia_total, item_para_no, "P01")
        print()

        # -- validações básicas --------------------------------------
        assert set(rota) == set(itens_nos), (
            "rota deve visitar todos os itens, sem repetir"
        )
        assert len(rota) == len(set(rota)), "rota não deve repetir nós"
        print("[OK] Todos os itens da lista foram visitados exatamente uma vez.\n")

    # -----------------------------------------------------------------
    # 4. Caso de empate explícito (desempate alfabético)
    # -----------------------------------------------------------------
    print("=" * 70)
    print("Caso de empate proposital (duas distâncias iguais)")
    print("=" * 70)

    # matriz artificial: a partir de "INI", os nós "B" e "A" estão à MESMA
    # distância (5.0m). Sem desempate, o resultado seria ambíguo (poderia
    # depender da ordem interna do set / hashing). Com desempate alfabético,
    # "A" deve sempre ser escolhido antes de "B".
    matriz_empate = {
        "INI": {"INI": 0.0, "A": 5.0, "B": 5.0, "C": 12.0},
        "A": {"INI": 5.0, "A": 0.0, "B": 3.0, "C": 7.0},
        "B": {"INI": 5.0, "A": 3.0, "B": 0.0, "C": 4.0},
        "C": {"INI": 12.0, "A": 7.0, "B": 4.0, "C": 0.0},
    }
    rota_empate, dist_empate = vizinho_mais_proximo(
        matriz_empate, "INI", ["A", "B", "C"]
    )
    print(
        f"Rota resultante: INI -> {' -> '.join(rota_empate)} "
        f"(distância total: {dist_empate:.1f}m)"
    )

    # A e B empatam em 5.0m a partir de INI -> desempate alfabético escolhe "A".
    assert rota_empate[0] == "A", (
        f"esperado desempate alfabético escolhendo 'A' primeiro, obtido '{rota_empate[0]}'"
    )
    print(
        "[OK] Empate (INI->A == INI->B == 5.0m) resolvido escolhendo 'A' "
        "(ordem alfabética), de forma determinística."
    )

    # roda de novo para confirmar que o resultado é sempre o mesmo (determinismo)
    for _ in range(5):
        rota_repeticao, _ = vizinho_mais_proximo(matriz_empate, "INI", ["A", "B", "C"])
        assert rota_repeticao == rota_empate, "heurística deve ser determinística"
    print("[OK] Resultado é determinístico em múltiplas execuções (5x testado).")

    print("\nTodos os testes passaram.")


# ---------------------------------------------------------------------------
# 4. Execução principal: catálogo numerado + seleção dinâmica do usuário
#
#    Reutiliza `selecionar_itens_mercado` (definida em matriz_distancias.py)
#    para imprimir a lista de 1 a N com todos os itens do mercado e ler a
#    escolha do usuário em uma única linha de números. A lista de compras
#    resultante é então processada normalmente: matriz de distâncias
#    (Dijkstra) + heurística de nearest neighbor, terminando com a
#    distância mínima total percorrida, em metros.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--teste":
        _executar_testes_regressao()
        sys.exit(0)

    grafo = carregar_grafo(CAMINHO_GRAFO)

    lista_de_compras = selecionar_itens_mercado()
    if not lista_de_compras:
        print("\nNenhum item selecionado. Encerrando sem calcular a rota.")
        sys.exit(0)

    print(f"\nLista de compras selecionada: {lista_de_compras}\n")

    try:
        matriz, nos_interesse, item_para_no = calcular_matriz_distancias(
            lista_de_compras, grafo=grafo, incluir_entrada=True
        )
    except ValueError as erro:
        print(f"\n[ERRO] {erro}")
        sys.exit(1)

    itens_nos = [no for no in nos_interesse if no != "P01"]
    rota, distancia_total = vizinho_mais_proximo(matriz, "P01", itens_nos)

    print("=" * 70)
    print("ROTA SUGERIDA (heurística nearest neighbor)")
    print("=" * 70)
    imprimir_rota(rota, distancia_total, item_para_no, "P01")
    print(f"\n>>> DISTÂNCIA MÍNIMA TOTAL PERCORRIDA: {distancia_total:.1f}m <<<")
