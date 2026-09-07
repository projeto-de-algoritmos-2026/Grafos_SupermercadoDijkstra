"""
Matriz de distâncias mínimas entre itens da lista de compras.

Depende de dijkstra.py (issue #5): usa `carregar_grafo` e `dijkstra` para
calcular, com uma única execução de Dijkstra por nó de interesse, a
distância mínima entre TODOS os pares de itens da lista (incluindo o
ponto de entrada do mercado como origem da rota).

Fluxo:
    1. Cada item da lista de compras (nome em texto livre, ex: "Leite")
       é mapeado para um nó do grafo (ex: "C10"), usando as descrições
       de produto->corredor da tabela_mercado.md.
    2. Para cada nó de interesse (entrada + itens, sem repetição), roda-se
       Dijkstra uma vez a partir dele. Isso já dá a distância mínima até
       TODOS os outros nós de interesse simultaneamente -- não é preciso
       rodar Dijkstra par a par (O(k) execuções em vez de O(k^2)).
    3. Os resultados são organizados em uma matriz k x k (dict de dict),
       pronta para ser consumida pela heurística de nearest neighbor
       (próxima etapa do projeto, ver escopo_projeto.md secao 4.4).
"""

import math
import sys
import unicodedata

try:
    from .dijkstra import CAMINHO_GRAFO, carregar_grafo, dijkstra
except ImportError:
    from dijkstra import CAMINHO_GRAFO, carregar_grafo, dijkstra


# ---------------------------------------------------------------------------
# 1. Mapeamento produto (texto livre) -> nó do grafo
#    Fonte: tabela_mercado.md
# ---------------------------------------------------------------------------

DESCRICOES_NO = {
    # Corredores
    "C01": "Whisky, Vodkas, Aguardentes",
    "C02": "Condicionadores, Shampoo, Cremes de Pentear, Sabonetes, Gel para Cabelo",
    "C03": "Desodorante, Escovas, Cremes Dentais, Hidratantes, Absorventes",
    "C04": "Cotonetes, Algodao, Fraldas",
    "C05": "Papel Higienico, Desinfetante, Desodorizadores",
    "C06": "Limpadores Perfumados, Alcool, Inseticidas, Detergentes, Multiuso, Limpa Aluminio",
    "C07": "Sabao em Po, Sabao Liquido, Sabao em Barra, Agua Sanitaria, Alvejantes, Amaciantes",
    "C08": "Organizadores, Baldes, Lixeiras",
    "C09": "Utilidades, Garrafa Termica, Potes Plasticos, Tacas, Pratos, Copos de Vidro, Porcelanas",
    "C10": "Adocantes, Leite Condensado, Leites, Carvao",
    "C11": "Talheres, Panelas, Automotivos, Racoes, Pet Shop",
    "C12": "Papel Aluminio, Papel Toalha, Descartaveis, Guardanapos",
    "C13": "Farinaceos, Pipocas, Canjicas, Sardinhas, Azeitonas, Palmitos, Milho Verde",
    "C14": "Azeites, Vinagres, Oleos, Temperos",
    "C15": "Extrato de Tomate, Molhos, Batata Palha, Macarrao, Massas",
    "C16": "Cafe, Filtro de Papel, Cappuccino, Alimentos Infantis, Achocolatados, Leite em Po",
    "C17": "Barra de Cereais, Fitness",
    "C18": "Pirulitos, Balas, Geleias, Chocolates",
    "C19": "Biscoitos",
    "C20": "Agua Mineral, Isotonicos, Sucos, Cervejas e Refrigerantes",
    # Freezers
    "F01": "Carnes Vermelha",
    "F02": "Cortes de Frango",
    "F03": "Peixes",
    "F04": "Vegetais Congelados",
    "F05": "Polpas",
    "F06": "Sobremesas Congeladas",
    "F07": "Panificacao Congelada",
    "F08": "Pratos Prontos",
    "F09": "Pratos Prontos",
    # Geladeiras
    "G01": "Bebidas Geladas",
    "G02": "Sobremesas Refrigeradas",
    "G03": "Massas Frescas",
    "G04": "Embutidos",
    "G05": "Laticinios",
    "G06": "Laticinios",
    # Açougue
    "A01": (
        "Alcatra, Contrafile, Coxao Mole, Patinho, Acem, Musculo, Miolo de Paleta, "
        "Costela, Picanha, Maminha, Fraldinha, File Mignon, Costelinha, Lombo, "
        "Pernil, Bacon, Linguica, Frango Passarinho"
    ),
    # Frutas e vegetais
    "M01": "Batata, Cebola, Abobora, Inhame, Cenoura, Beterraba",
    "M02": "Tomate, Pimentao, Abobrinha, Chuchu, Pepino",
    "M03": "Bananas, Macas, Mamao",
    "M04": "Laranja, Limao, Tangerina",
    "M05": "Morango, Uva, Kiwi, Ameixa",
    "M06": "Melancia, Melao, Abacaxi",
    "M07": "Alface, Couve, Agriao, Rucula, Espinafre",
    "M08": "Cheiro Verde, Coentro, Cebolinha, Hortela",
    # Entrada / Saída
    "P01": "Entrada",
    "P02": "Saida",
}


def _normalizar(texto: str) -> str:
    """minúsculas, sem acento, sem espaços nas pontas -- para comparação robusta."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.strip().lower()


def mapear_item_para_no(item: str) -> str:
    """Converte o nome de um item da lista de compras no código do nó do grafo.

    Aceita tanto texto livre ("Leite", "sabao em po") quanto o código do nó
    já pronto ("C10"), o que é útil para itens que não constam na tabela de
    descrições ou para testes diretos.
    """
    item_norm = _normalizar(item)

    # já é um código de nó válido (ex: "C10", "m05")?
    codigo = item.strip().upper()
    if codigo in DESCRICOES_NO or codigo in ("P01", "P02"):
        return codigo

    # 1ª tentativa: correspondência EXATA com algum termo do corredor
    # (evita que "Batata" bata em "Batata Palha" quando existe um termo
    # "Batata" exato em outro corredor, por exemplo).
    candidatos = []
    for no, descricao in DESCRICOES_NO.items():
        termos = [_normalizar(t) for t in descricao.split(",")]
        if item_norm in termos:
            candidatos.append(no)

    # 2ª tentativa (fallback): correspondência por substring, só usada se
    # nenhum termo exato foi encontrado em nenhum corredor.
    if not candidatos:
        for no, descricao in DESCRICOES_NO.items():
            termos = [_normalizar(t) for t in descricao.split(",")]
            for termo in termos:
                if item_norm in termo or termo in item_norm:
                    candidatos.append(no)
                    break

    if not candidatos:
        raise ValueError(
            f"Item '{item}' não encontrado em nenhuma seção do mercado "
            f"(verifique a grafia ou use o código do nó diretamente)."
        )
    if len(candidatos) > 1:
        # Em caso de ambiguidade, avisa mas segue com o primeiro achado
        print(
            f"[AVISO] Item '{item}' bateu com mais de um corredor "
            f"{candidatos}; usando '{candidatos[0]}'."
        )
    return candidatos[0]


# ---------------------------------------------------------------------------
# 1.1 Catálogo numerado de itens do mercado (baseado em DESCRICOES_NO, que
#     por sua vez reflete a tabela_mercado.md) + seleção do usuário por
#     número, tudo em uma única linha.
#
#     Esta é a ÚNICA fonte de catalogação/seleção de itens do projeto:
#     tanto este arquivo quanto nearest_neighbor.py importam e usam as
#     funções abaixo, para evitar duplicar a lógica em dois lugares.
# ---------------------------------------------------------------------------

# Nós que não representam produtos comprável (entrada/saída do mercado) e
# por isso não entram no catálogo numerado.
_NOS_NAO_PRODUTO = ("P01", "P02")


def catalogar_itens(descricoes_no: dict | None = None) -> list[dict]:
    """Monta o catálogo enumerado (1..N) de todos os itens do mercado.

    Cada entrada de `DESCRICOES_NO` (ex: "C10": "Adocantes, Leite Condensado,
    Leites, Carvao") é quebrada em itens individuais separados por vírgula,
    e cada item individual recebe um número sequencial único.

    Parâmetros
    ----------
    descricoes_no : dict, opcional
        Mapa {nó: "descrição, com, itens, separados, por, virgula"}.
        Se None, usa `DESCRICOES_NO` (derivado de tabela_mercado.md).

    Retorna
    -------
    catalogo : list[dict]
        Lista de entradas, na ordem de enumeração, cada uma no formato:
        {"numero": int, "item": str, "no": str}
    """
    if descricoes_no is None:
        descricoes_no = DESCRICOES_NO

    catalogo = []
    numero = 1
    for no, descricao in descricoes_no.items():
        if no in _NOS_NAO_PRODUTO:
            continue
        termos = [t.strip() for t in descricao.split(",") if t.strip()]
        for termo in termos:
            catalogo.append({"numero": numero, "item": termo, "no": no})
            numero += 1
    return catalogo


def imprimir_catalogo_itens(catalogo: list[dict] | None = None) -> list[dict]:
    """Imprime no terminal a lista de 1 a N de todos os itens do mercado.

    Formato: "  <número>. <item> (<nó>)", um item por linha.
    Retorna o catálogo usado (útil para passar em seguida a
    `ler_selecao_por_numero` sem recalcular).
    """
    if catalogo is None:
        catalogo = catalogar_itens()

    largura_numero = len(str(len(catalogo)))
    print("=" * 70)
    print("ITENS DISPONÍVEIS NO MERCADO")
    print("=" * 70)
    for entrada in catalogo:
        numero_fmt = str(entrada["numero"]).rjust(largura_numero)
        print(f"  {numero_fmt}. {entrada['item']} ({entrada['no']})")
    print("-" * 70)
    print(f"Total: {len(catalogo)} itens.\n")
    return catalogo


def ler_selecao_por_numero(catalogo: list[dict] | None = None) -> list[str]:
    """Lê, em UMA ÚNICA LINHA, os números dos itens escolhidos pelo usuário.

    Aceita os números separados por vírgula e/ou espaço (ex: "1, 5, 12 20").
    Números repetidos são ignorados na segunda ocorrência; números fora do
    intervalo válido ou não numéricos geram um aviso e são descartados.

    Parâmetros
    ----------
    catalogo : list[dict], opcional
        Catálogo já gerado por `catalogar_itens` (para não recalcular).
        Se None, gera um novo catálogo internamente.

    Retorna
    -------
    itens : list[str]
        Lista dos nomes dos itens escolhidos, na ordem em que os números
        foram digitados. Pronta para ser usada como `itens` em
        `calcular_matriz_distancias`.
    """
    if catalogo is None:
        catalogo = catalogar_itens()

    indice_por_numero = {entrada["numero"]: entrada for entrada in catalogo}

    linha = input(
        "Digite os números dos itens desejados, separados por vírgula ou "
        "espaço (ex: 1, 5, 12, 20): "
    ).strip()

    if not linha:
        return []

    partes = linha.replace(",", " ").split()
    selecionados = []
    ja_vistos = set()

    for parte in partes:
        try:
            numero = int(parte)
        except ValueError:
            print(f"[AVISO] '{parte}' não é um número válido; ignorando.")
            continue

        if numero not in indice_por_numero:
            print(
                f"[AVISO] Número {numero} fora do intervalo "
                f"(1-{len(catalogo)}); ignorando."
            )
            continue

        if numero in ja_vistos:
            continue
        ja_vistos.add(numero)
        selecionados.append(indice_por_numero[numero])

    return [entrada["item"] for entrada in selecionados]


def selecionar_itens_mercado() -> list[str]:
    """Fluxo completo: imprime o catálogo numerado e lê a seleção do usuário.

    Função de conveniência usada tanto pelo `matriz_distancias.py` quanto
    pelo `nearest_neighbor.py` para gerar a lista de compras dinâmica a
    partir da escolha do usuário, evitando duplicar a lógica nos dois
    arquivos.

    Retorna
    -------
    itens : list[str]
        Lista de nomes de itens escolhidos (ver `ler_selecao_por_numero`).
    """
    catalogo = imprimir_catalogo_itens()
    itens = ler_selecao_por_numero(catalogo)
    if not itens:
        print("[AVISO] Nenhum item válido selecionado.")
    return itens


# ---------------------------------------------------------------------------
# 2. Cálculo da matriz de distâncias
# ---------------------------------------------------------------------------


def calcular_matriz_distancias(
    itens: list[str],
    grafo: dict | None = None,
    caminho_json: str = str(CAMINHO_GRAFO),
    no_entrada: str = "P01",
    incluir_entrada: bool = True,
):
    """Calcula a distância mínima (Dijkstra) entre cada par de itens da lista.

    Parâmetros
    ----------
    itens : list[str]
        Lista de itens da compra (texto livre ou código do nó).
    grafo : dict, opcional
        Grafo já carregado (ver `carregar_grafo`). Se None, carrega de
        `caminho_json`.
    caminho_json : str
        Caminho do grafo_ponderado.json, usado apenas se `grafo` for None.
    no_entrada : str
        Nó de partida da rota (padrão: "P01", Entrada).
    incluir_entrada : bool
        Se True (padrão), inclui o ponto de entrada como uma "linha/coluna"
        extra na matriz -- necessário para a heurística de nearest neighbor
        decidir o primeiro item a visitar.

    Retorna
    -------
    matriz : dict[str, dict[str, float]]
        matriz[no_a][no_b] = distância mínima em metros entre no_a e no_b.
        As chaves são os NÓS do grafo (não o texto original do item).
    nos_interesse : list[str]
        Lista ordenada dos nós usados como linhas/colunas da matriz
        (entrada primeiro, se incluída, depois um nó por item, na ordem
        de entrada, sem repetição).
    item_para_no : dict[str, str]
        Mapeamento do texto original de cada item para o nó encontrado,
        para exibição amigável dos resultados.
    """
    if grafo is None:
        grafo = carregar_grafo(caminho_json)

    # 2.1 mapeia cada item de texto livre para o nó do grafo correspondente
    item_para_no = {item: mapear_item_para_no(item) for item in itens}

    # 2.2 monta a lista de nós de interesse, sem duplicar nós repetidos
    nos_interesse = []
    if incluir_entrada:
        nos_interesse.append(no_entrada)
    for no in item_para_no.values():
        if no not in nos_interesse:
            nos_interesse.append(no)

    for no in nos_interesse:
        if no not in grafo:
            raise ValueError(f"Nó '{no}' não existe no grafo carregado.")

    # 2.3 roda Dijkstra UMA VEZ a partir de cada nó de interesse (O(k) execuções,
    # não O(k^2)) e recorta apenas as distâncias para os demais nós de interesse
    matriz = {}
    for origem in nos_interesse:
        distancias_completas, _ = dijkstra(grafo, origem)
        matriz[origem] = {
            destino: distancias_completas[destino] for destino in nos_interesse
        }

    return matriz, nos_interesse, item_para_no


# ---------------------------------------------------------------------------
# 3. Exibição da matriz
# ---------------------------------------------------------------------------


def imprimir_matriz(matriz: dict, nos_interesse: list[str], item_para_no: dict):
    rotulo_no = {no: no for no in nos_interesse}
    # rótulo amigável: "P01 (Entrada)" / "C10 (Leite)"
    no_para_item = {}
    for item, no in item_para_no.items():
        no_para_item.setdefault(no, []).append(item)

    def rotulo(no):
        if no in no_para_item:
            return f"{no} ({', '.join(no_para_item[no])})"
        if no == "P01":
            return "P01 (Entrada)"
        return no

    largura = max(len(rotulo(no)) for no in nos_interesse) + 2

    cabecalho = " " * largura + "".join(f"{no:>9}" for no in nos_interesse)
    print(cabecalho)
    for origem in nos_interesse:
        linha = f"{rotulo(origem):<{largura}}"
        for destino in nos_interesse:
            d = matriz[origem][destino]
            linha += f"{d:9.1f}" if d != math.inf else f"{'inf':>9}"
        print(linha)

    print("\nLegenda:")
    for item, no in item_para_no.items():
        print(f"  '{item}' -> nó {no} ({DESCRICOES_NO.get(no, '')})")


# ---------------------------------------------------------------------------
# 4. Entrada dinâmica da lista de compras
# ---------------------------------------------------------------------------


def ler_lista_de_compras() -> list[str]:
    """Lê a lista de compras dinamicamente, sem nada fixo no código.

    Ordem de prioridade:
      1. Argumentos de linha de comando. Aceita tanto
         `python matriz_distancias.py Leite Batata Frango`
         quanto `python matriz_distancias.py "Leite, Batata, Frango"`.
      2. Se nenhum argumento for passado, pergunta interativamente:
         o usuário pode digitar todos os itens separados por vírgula em
         uma única linha, OU um item por linha, encerrando com uma linha
         vazia ou a palavra 'fim'.

    Retorna
    -------
    list[str]
        Lista de itens digitados pelo usuário (texto livre).
    """
    argv = sys.argv[1:]
    if argv:
        if len(argv) == 1 and "," in argv[0]:
            return [item.strip() for item in argv[0].split(",") if item.strip()]
        return [item.strip() for item in argv if item.strip()]

    print("Digite os itens da lista de compras.")
    print("- Todos de uma vez, separados por vírgula (ex: Leite, Batata, Cerveja)")
    print("- OU um item por linha, terminando com linha vazia ou 'fim'\n")

    primeira_linha = input("Itens: ").strip()
    if not primeira_linha or primeira_linha.lower() == "fim":
        return []
    if "," in primeira_linha:
        return [item.strip() for item in primeira_linha.split(",") if item.strip()]

    itens = [primeira_linha]
    while True:
        linha = input(f"Item {len(itens) + 1} (ou 'fim' para terminar): ").strip()
        if not linha or linha.lower() == "fim":
            break
        itens.append(linha)
    return itens


# ---------------------------------------------------------------------------
# 5. Execução principal (lista dinâmica) + suíte de regressão opcional
# ---------------------------------------------------------------------------


def _executar_testes_regressao():
    """Suíte de testes fixa (issue #6), usada para validar que a matriz
    continua correta após mudanças no código. Rode com `--teste`."""
    lista_de_compras = ["Leite", "Batata", "Frango", "Sabonete", "Macarrao", "Cerveja"]
    grafo = carregar_grafo(CAMINHO_GRAFO)

    matriz, nos_interesse, item_para_no = calcular_matriz_distancias(
        lista_de_compras, grafo=grafo, incluir_entrada=True
    )

    print("=" * 70)
    print("MATRIZ DE DISTÂNCIAS MÍNIMAS (metros) -- lista de compras de teste")
    print("=" * 70)
    print(f"Lista de compras: {lista_de_compras}\n")
    imprimir_matriz(matriz, nos_interesse, item_para_no)

    print("\n" + "=" * 70)
    print("VALIDAÇÕES")
    print("=" * 70)

    assert len(matriz) == len(nos_interesse)
    for origem in nos_interesse:
        assert set(matriz[origem].keys()) == set(nos_interesse)
    print(
        f"[OK] Matriz {len(nos_interesse)}x{len(nos_interesse)} "
        f"cobrindo entrada + {len(set(item_para_no.values()))} nós de itens distintos."
    )

    for no in nos_interesse:
        assert matriz[no][no] == 0.0
    print("[OK] Diagonal principal (distância de cada nó a si mesmo) é 0.")

    for a in nos_interesse:
        for b in nos_interesse:
            assert abs(matriz[a][b] - matriz[b][a]) < 1e-9
    print("[OK] Matriz simétrica (dist(a,b) == dist(b,a)).")

    assert all(d != math.inf for d in matriz["P01"].values())
    print("[OK] Todos os itens da lista são alcançáveis a partir da Entrada (P01).")

    print(f"\nDistância Entrada -> Sabonete (C02): {matriz['P01']['C02']:.1f}m")
    print("\nTodos os testes passaram.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--teste":
        _executar_testes_regressao()
        sys.exit(0)

    grafo = carregar_grafo(CAMINHO_GRAFO)
    lista_de_compras = selecionar_itens_mercado()

    if not lista_de_compras:
        print("\nNenhum item informado. Encerrando sem calcular a matriz.")
        sys.exit(0)

    try:
        matriz, nos_interesse, item_para_no = calcular_matriz_distancias(
            lista_de_compras, grafo=grafo, incluir_entrada=True
        )
    except ValueError as erro:
        print(f"\n[ERRO] {erro}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("MATRIZ DE DISTÂNCIAS MÍNIMAS (metros)")
    print("=" * 70)
    print(f"Lista de compras: {lista_de_compras}\n")
    imprimir_matriz(matriz, nos_interesse, item_para_no)
