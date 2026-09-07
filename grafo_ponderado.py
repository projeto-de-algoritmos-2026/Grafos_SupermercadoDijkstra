# Grafo do Mercado Ponderado com Distâncias Realistas em Metros
# Baseado no layout do mercado analisado

# Coordenadas aproximadas dos nós (x, y) em metros
# Origem (0,0) no canto superior esquerdo
coordenadas = {
    # Açougue
    "A01": (5, 28),
    # Geladeiras (coluna esquerda, vertical)
    "G06": (12, 26),
    "G05": (12, 22),
    "G04": (12, 18),
    "G03": (12, 14),
    "G02": (12, 10),
    "G01": (12, 6),
    # Freezers (superior central)
    "F01": (18, 26),
    "F02": (18, 22),
    "F03": (18, 18),
    "F04": (24, 26),
    "F05": (24, 22),
    "F06": (24, 18),
    "F07": (30, 26),
    "F08": (30, 22),
    "F09": (30, 18),
    # Frutas e Vegetais (central)
    "M07": (18, 14),
    "M08": (24, 14),
    "M02": (16, 10),
    "M03": (20, 10),
    "M05": (24, 10),
    "M01": (14, 6),
    "M04": (19, 6),
    "M06": (24, 6),
    # Corredores (lado direito, em grade vertical)
    "C11": (34, 18),
    "C12": (38, 20),
    "C13": (42, 20),
    "C14": (46, 20),
    "C15": (50, 20),
    "C16": (54, 20),
    "C17": (58, 20),
    "C18": (62, 20),
    "C19": (66, 20),
    "C20": (70, 20),
    "C10": (34, 10),
    "C09": (38, 14),
    "C08": (42, 14),
    "C07": (46, 14),
    "C06": (50, 14),
    "C05": (54, 14),
    "C04": (58, 14),
    "C03": (62, 14),
    "C02": (66, 14),
    "C01": (70, 14),
    # Caixas (inferior central)
    "X01": (20, 4),
    "X02": (28, 4),
    "X03": (36, 4),
    "X04": (44, 4),
    "X05": (52, 4),
    # Entrada/Saída
    "P01": (72, 0),  # Entrada (lado direito inferior)
    "P02": (5, 0),  # Saída (lado esquerdo inferior)
}

import math


def calcular_distancia(node1, node2):
    """Calcula distância euclidiana entre dois nós em metros"""
    x1, y1 = coordenadas[node1]
    x2, y2 = coordenadas[node2]
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # Arredondar para 1 casa decimal
    return round(distancia, 1)


# Lista de adjacência com pesos em metros
adjacencias = {
    "A01": [
        ("G06", calcular_distancia("A01", "G06")),
        ("F01", calcular_distancia("A01", "F01")),
        ("F04", calcular_distancia("A01", "F04")),
        ("F07", calcular_distancia("A01", "F07")),
    ],
    "G06": [
        ("A01", calcular_distancia("G06", "A01")),
        ("F01", calcular_distancia("G06", "F01")),
        ("F02", calcular_distancia("G06", "F02")),
        ("F03", calcular_distancia("G06", "F03")),
        ("G05", calcular_distancia("G06", "G05")),
    ],
    "G05": [
        ("G06", calcular_distancia("G05", "G06")),
        ("F01", calcular_distancia("G05", "F01")),
        ("F02", calcular_distancia("G05", "F02")),
        ("F03", calcular_distancia("G05", "F03")),
        ("M07", calcular_distancia("G05", "M07")),
        ("G04", calcular_distancia("G05", "G04")),
    ],
    "G04": [
        ("G05", calcular_distancia("G04", "G05")),
        ("F03", calcular_distancia("G04", "F03")),
        ("M07", calcular_distancia("G04", "M07")),
        ("M02", calcular_distancia("G04", "M02")),
        ("G03", calcular_distancia("G04", "G03")),
    ],
    "G03": [
        ("G04", calcular_distancia("G03", "G04")),
        ("M01", calcular_distancia("G03", "M01")),
        ("M02", calcular_distancia("G03", "M02")),
        ("M07", calcular_distancia("G03", "M07")),
        ("G02", calcular_distancia("G03", "G02")),
    ],
    "G02": [
        ("G03", calcular_distancia("G02", "G03")),
        ("M01", calcular_distancia("G02", "M01")),
        ("M02", calcular_distancia("G02", "M02")),
        ("G01", calcular_distancia("G02", "G01")),
        ("X01", calcular_distancia("G02", "X01")),
        ("P02", calcular_distancia("G02", "P02")),
    ],
    "G01": [
        ("G02", calcular_distancia("G01", "G02")),
        ("M01", calcular_distancia("G01", "M01")),
        ("X01", calcular_distancia("G01", "X01")),
        ("P02", calcular_distancia("G01", "P02")),
    ],
    "F01": [
        ("A01", calcular_distancia("F01", "A01")),
        ("G06", calcular_distancia("F01", "G06")),
        ("F02", calcular_distancia("F01", "F02")),
        ("F04", calcular_distancia("F01", "F04")),
    ],
    "F02": [
        ("F01", calcular_distancia("F02", "F01")),
        ("G06", calcular_distancia("F02", "G06")),
        ("G05", calcular_distancia("F02", "G05")),
        ("F03", calcular_distancia("F02", "F03")),
        ("A01", calcular_distancia("F02", "A01")),
    ],
    "F03": [
        ("F02", calcular_distancia("F03", "F02")),
        ("G05", calcular_distancia("F03", "G05")),
        ("G04", calcular_distancia("F03", "G04")),
        ("G03", calcular_distancia("F03", "G03")),
        ("F06", calcular_distancia("F03", "F06")),
        ("M07", calcular_distancia("F03", "M07")),
        ("M08", calcular_distancia("F03", "M08")),
    ],
    "F04": [
        ("A01", calcular_distancia("F04", "A01")),
        ("F01", calcular_distancia("F04", "F01")),
        ("F07", calcular_distancia("F04", "F07")),
        ("F05", calcular_distancia("F04", "F05")),
    ],
    "F05": [
        ("F04", calcular_distancia("F05", "F04")),
        ("F06", calcular_distancia("F05", "F06")),
    ],
    "F06": [
        ("F05", calcular_distancia("F06", "F05")),
        ("F03", calcular_distancia("F06", "F03")),
        ("F09", calcular_distancia("F06", "F09")),
        ("M03", calcular_distancia("F06", "M03")),
        ("M07", calcular_distancia("F06", "M07")),
        ("M08", calcular_distancia("F06", "M08")),
    ],
    "F07": [
        ("A01", calcular_distancia("F07", "A01")),
        ("F04", calcular_distancia("F07", "F04")),
        ("F08", calcular_distancia("F07", "F08")),
        ("C11", calcular_distancia("F07", "C11")),
    ],
    "F08": [
        ("F07", calcular_distancia("F08", "F07")),
        ("F09", calcular_distancia("F08", "F09")),
        ("C11", calcular_distancia("F08", "C11")),
    ],
    "F09": [
        ("F08", calcular_distancia("F09", "F08")),
        ("F06", calcular_distancia("F09", "F06")),
        ("M07", calcular_distancia("F09", "M07")),
        ("M08", calcular_distancia("F09", "M08")),
        ("M05", calcular_distancia("F09", "M05")),
        ("C10", calcular_distancia("F09", "C10")),
        ("C11", calcular_distancia("F09", "C11")),
    ],
    "M01": [
        ("G02", calcular_distancia("M01", "G02")),
        ("G01", calcular_distancia("M01", "G01")),
        ("M02", calcular_distancia("M01", "M02")),
        ("M04", calcular_distancia("M01", "M04")),
        ("X01", calcular_distancia("M01", "X01")),
    ],
    "M02": [
        ("M01", calcular_distancia("M02", "M01")),
        ("G03", calcular_distancia("M02", "G03")),
        ("G02", calcular_distancia("M02", "G02")),
        ("M03", calcular_distancia("M02", "M03")),
        ("M07", calcular_distancia("M02", "M07")),
        ("M04", calcular_distancia("M02", "M04")),
    ],
    "M03": [
        ("M02", calcular_distancia("M03", "M02")),
        ("G04", calcular_distancia("M03", "G04")),
        ("M06", calcular_distancia("M03", "M06")),
        ("M07", calcular_distancia("M03", "M07")),
        ("M05", calcular_distancia("M03", "M05")),
        ("M04", calcular_distancia("M03", "M04")),
        ("M01", calcular_distancia("M03", "M01")),
        ("F06", calcular_distancia("M03", "F06")),
    ],
    "M04": [
        ("M01", calcular_distancia("M04", "M01")),
        ("M05", calcular_distancia("M04", "M05")),
        ("M03", calcular_distancia("M04", "M03")),
        ("M06", calcular_distancia("M04", "M06")),
        ("X01", calcular_distancia("M04", "X01")),
        ("X02", calcular_distancia("M04", "X02")),
    ],
    "M05": [
        ("M03", calcular_distancia("M05", "M03")),
        ("M06", calcular_distancia("M05", "M06")),
        ("M08", calcular_distancia("M05", "M08")),
        ("M04", calcular_distancia("M05", "M04")),
        ("X03", calcular_distancia("M05", "X03")),
        ("X04", calcular_distancia("M05", "X04")),
        ("C11", calcular_distancia("M05", "C11")),
    ],
    "M06": [
        ("M04", calcular_distancia("M06", "M04")),
        ("M05", calcular_distancia("M06", "M05")),
        ("X02", calcular_distancia("M06", "X02")),
        ("X01", calcular_distancia("M06", "X01")),
        ("X03", calcular_distancia("M06", "X03")),
        ("C10", calcular_distancia("M06", "C10")),
    ],
    "M07": [
        ("M02", calcular_distancia("M07", "M02")),
        ("M03", calcular_distancia("M07", "M03")),
        ("G04", calcular_distancia("M07", "G04")),
        ("G03", calcular_distancia("M07", "G03")),
        ("G05", calcular_distancia("M07", "G05")),
        ("M08", calcular_distancia("M07", "M08")),
        ("F09", calcular_distancia("M07", "F09")),
        ("F06", calcular_distancia("M07", "F06")),
        ("F03", calcular_distancia("M07", "F03")),
    ],
    "M08": [
        ("M07", calcular_distancia("M08", "M07")),
        ("M05", calcular_distancia("M08", "M05")),
        ("F09", calcular_distancia("M08", "F09")),
        ("F06", calcular_distancia("M08", "F06")),
        ("F03", calcular_distancia("M08", "F03")),
        ("C11", calcular_distancia("M08", "C11")),
        ("C10", calcular_distancia("M08", "C10")),
    ],
    "C11": [
        ("F07", calcular_distancia("C11", "F07")),
        ("F08", calcular_distancia("C11", "F08")),
        ("F09", calcular_distancia("C11", "F09")),
        ("M08", calcular_distancia("C11", "M08")),
        ("M05", calcular_distancia("C11", "M05")),
        ("C12", calcular_distancia("C11", "C12")),
        ("C10", calcular_distancia("C11", "C10")),
        ("C09", calcular_distancia("C11", "C09")),
        ("C08", calcular_distancia("C11", "C08")),
    ],
    "C12": [
        ("C11", calcular_distancia("C12", "C11")),
        ("C10", calcular_distancia("C12", "C10")),
        ("C09", calcular_distancia("C12", "C09")),
        ("C08", calcular_distancia("C12", "C08")),
        ("C13", calcular_distancia("C12", "C13")),
    ],
    "C13": [
        ("C12", calcular_distancia("C13", "C12")),
        ("C14", calcular_distancia("C13", "C14")),
        ("C08", calcular_distancia("C13", "C08")),
        ("C09", calcular_distancia("C13", "C09")),
        ("C07", calcular_distancia("C13", "C07")),
    ],
    "C14": [
        ("C13", calcular_distancia("C14", "C13")),
        ("C15", calcular_distancia("C14", "C15")),
        ("C08", calcular_distancia("C14", "C08")),
        ("C07", calcular_distancia("C14", "C07")),
        ("C06", calcular_distancia("C14", "C06")),
    ],
    "C15": [
        ("C14", calcular_distancia("C15", "C14")),
        ("C16", calcular_distancia("C15", "C16")),
        ("C07", calcular_distancia("C15", "C07")),
        ("C06", calcular_distancia("C15", "C06")),
        ("C05", calcular_distancia("C15", "C05")),
    ],
    "C16": [
        ("C15", calcular_distancia("C16", "C15")),
        ("C17", calcular_distancia("C16", "C17")),
        ("C06", calcular_distancia("C16", "C06")),
        ("C05", calcular_distancia("C16", "C05")),
        ("C04", calcular_distancia("C16", "C04")),
    ],
    "C17": [
        ("C16", calcular_distancia("C17", "C16")),
        ("C18", calcular_distancia("C17", "C18")),
        ("C05", calcular_distancia("C17", "C05")),
        ("C04", calcular_distancia("C17", "C04")),
        ("C03", calcular_distancia("C17", "C03")),
    ],
    "C18": [
        ("C17", calcular_distancia("C18", "C17")),
        ("C19", calcular_distancia("C18", "C19")),
        ("C04", calcular_distancia("C18", "C04")),
        ("C03", calcular_distancia("C18", "C03")),
        ("C02", calcular_distancia("C18", "C02")),
    ],
    "C19": [
        ("C18", calcular_distancia("C19", "C18")),
        ("C20", calcular_distancia("C19", "C20")),
        ("C03", calcular_distancia("C19", "C03")),
        ("C02", calcular_distancia("C19", "C02")),
        ("C01", calcular_distancia("C19", "C01")),
    ],
    "C20": [
        ("C19", calcular_distancia("C20", "C19")),
        ("C01", calcular_distancia("C20", "C01")),
    ],
    "C01": [
        ("C20", calcular_distancia("C01", "C20")),
        ("C19", calcular_distancia("C01", "C19")),
        ("C02", calcular_distancia("C01", "C02")),
        ("P01", calcular_distancia("C01", "P01")),
    ],
    "C02": [
        ("C01", calcular_distancia("C02", "C01")),
        ("C03", calcular_distancia("C02", "C03")),
        ("P01", calcular_distancia("C02", "P01")),
        ("C20", calcular_distancia("C02", "C20")),
        ("C19", calcular_distancia("C02", "C19")),
        ("C18", calcular_distancia("C02", "C18")),
    ],
    "C03": [
        ("C02", calcular_distancia("C03", "C02")),
        ("C04", calcular_distancia("C03", "C04")),
        ("C19", calcular_distancia("C03", "C19")),
        ("P01", calcular_distancia("C03", "P01")),
        ("C18", calcular_distancia("C03", "C18")),
        ("C17", calcular_distancia("C03", "C17")),
    ],
    "C04": [
        ("C03", calcular_distancia("C04", "C03")),
        ("C05", calcular_distancia("C04", "C05")),
        ("C18", calcular_distancia("C04", "C18")),
        ("P01", calcular_distancia("C04", "P01")),
        ("X05", calcular_distancia("C04", "X05")),
        ("C17", calcular_distancia("C04", "C17")),
        ("C16", calcular_distancia("C04", "C16")),
    ],
    "C05": [
        ("C04", calcular_distancia("C05", "C04")),
        ("C06", calcular_distancia("C05", "C06")),
        ("C17", calcular_distancia("C05", "C17")),
        ("P01", calcular_distancia("C05", "P01")),
        ("X05", calcular_distancia("C05", "X05")),
        ("C16", calcular_distancia("C05", "C16")),
        ("C15", calcular_distancia("C05", "C15")),
    ],
    "C06": [
        ("C05", calcular_distancia("C06", "C05")),
        ("C07", calcular_distancia("C06", "C07")),
        ("C16", calcular_distancia("C06", "C16")),
        ("P01", calcular_distancia("C06", "P01")),
        ("X05", calcular_distancia("C06", "X05")),
        ("C15", calcular_distancia("C06", "C15")),
        ("C14", calcular_distancia("C06", "C14")),
    ],
    "C07": [
        ("C06", calcular_distancia("C07", "C06")),
        ("C08", calcular_distancia("C07", "C08")),
        ("C15", calcular_distancia("C07", "C15")),
        ("X05", calcular_distancia("C07", "X05")),
        ("X04", calcular_distancia("C07", "X04")),
        ("C14", calcular_distancia("C07", "C14")),
        ("C13", calcular_distancia("C07", "C13")),
    ],
    "C08": [
        ("C07", calcular_distancia("C08", "C07")),
        ("C09", calcular_distancia("C08", "C09")),
        ("C13", calcular_distancia("C08", "C13")),
        ("X05", calcular_distancia("C08", "X05")),
        ("X04", calcular_distancia("C08", "X04")),
        ("X03", calcular_distancia("C08", "X03")),
        ("C12", calcular_distancia("C08", "C12")),
        ("C11", calcular_distancia("C08", "C11")),
        ("C14", calcular_distancia("C08", "C14")),
    ],
    "C09": [
        ("C08", calcular_distancia("C09", "C08")),
        ("C10", calcular_distancia("C09", "C10")),
        ("C11", calcular_distancia("C09", "C11")),
        ("X05", calcular_distancia("C09", "X05")),
        ("X04", calcular_distancia("C09", "X04")),
        ("X03", calcular_distancia("C09", "X03")),
        ("C12", calcular_distancia("C09", "C12")),
        ("C13", calcular_distancia("C09", "C13")),
    ],
    "C10": [
        ("C09", calcular_distancia("C10", "C09")),
        ("C11", calcular_distancia("C10", "C11")),
        ("C12", calcular_distancia("C10", "C12")),
        ("X01", calcular_distancia("C10", "X01")),
        ("X02", calcular_distancia("C10", "X02")),
        ("X03", calcular_distancia("C10", "X03")),
        ("X04", calcular_distancia("C10", "X04")),
        ("X05", calcular_distancia("C10", "X05")),
        ("M06", calcular_distancia("C10", "M06")),
        ("M05", calcular_distancia("C10", "M05")),
        ("M08", calcular_distancia("C10", "M08")),
        ("F09", calcular_distancia("C10", "F09")),
    ],
    "X01": [
        ("G01", calcular_distancia("X01", "G01")),
        ("G02", calcular_distancia("X01", "G02")),
        ("M01", calcular_distancia("X01", "M01")),
        ("M04", calcular_distancia("X01", "M04")),
        ("M06", calcular_distancia("X01", "M06")),
        ("X02", calcular_distancia("X01", "X02")),
        ("P02", calcular_distancia("X01", "P02")),
        ("P01", calcular_distancia("X01", "P01")),
    ],
    "X02": [
        ("X01", calcular_distancia("X02", "X01")),
        ("M04", calcular_distancia("X02", "M04")),
        ("M05", calcular_distancia("X02", "M05")),
        ("M06", calcular_distancia("X02", "M06")),
        ("X03", calcular_distancia("X02", "X03")),
        ("P01", calcular_distancia("X02", "P01")),
        ("C10", calcular_distancia("X02", "C10")),
    ],
    "X03": [
        ("X02", calcular_distancia("X03", "X02")),
        ("M05", calcular_distancia("X03", "M05")),
        ("M06", calcular_distancia("X03", "M06")),
        ("X04", calcular_distancia("X03", "X04")),
        ("P01", calcular_distancia("X03", "P01")),
        ("C10", calcular_distancia("X03", "C10")),
        ("C09", calcular_distancia("X03", "C09")),
        ("C08", calcular_distancia("X03", "C08")),
    ],
    "X04": [
        ("X03", calcular_distancia("X04", "X03")),
        ("M05", calcular_distancia("X04", "M05")),
        ("C10", calcular_distancia("X04", "C10")),
        ("C09", calcular_distancia("X04", "C09")),
        ("C08", calcular_distancia("X04", "C08")),
        ("C07", calcular_distancia("X04", "C07")),
        ("C06", calcular_distancia("X04", "C06")),
        ("X05", calcular_distancia("X04", "X05")),
        ("P01", calcular_distancia("X04", "P01")),
        ("P02", calcular_distancia("X04", "P02")),
    ],
    "X05": [
        ("X04", calcular_distancia("X05", "X04")),
        ("P01", calcular_distancia("X05", "P01")),
        ("P02", calcular_distancia("X05", "P02")),
        ("C06", calcular_distancia("X05", "C06")),
        ("C07", calcular_distancia("X05", "C07")),
        ("C08", calcular_distancia("X05", "C08")),
        ("C09", calcular_distancia("X05", "C09")),
        ("C10", calcular_distancia("X05", "C10")),
        ("C04", calcular_distancia("X05", "C04")),
    ],
    "P01": [
        ("X01", calcular_distancia("P01", "X01")),
        ("X02", calcular_distancia("P01", "X02")),
        ("X03", calcular_distancia("P01", "X03")),
        ("X04", calcular_distancia("P01", "X04")),
        ("X05", calcular_distancia("P01", "X05")),
        ("P02", calcular_distancia("P01", "P02")),
        ("C06", calcular_distancia("P01", "C06")),
        ("C05", calcular_distancia("P01", "C05")),
        ("C04", calcular_distancia("P01", "C04")),
        ("C03", calcular_distancia("P01", "C03")),
        ("C02", calcular_distancia("P01", "C02")),
        ("C01", calcular_distancia("P01", "C01")),
    ],
    "P02": [
        ("G01", calcular_distancia("P02", "G01")),
        ("G02", calcular_distancia("P02", "G02")),
        ("X01", calcular_distancia("P02", "X01")),
        ("X02", calcular_distancia("P02", "X02")),
        ("X03", calcular_distancia("P02", "X03")),
        ("X04", calcular_distancia("P02", "X04")),
        ("X05", calcular_distancia("P02", "X05")),
        ("P01", calcular_distancia("P02", "P01")),
    ],
}


# Função para imprimir o grafo formatado
def imprimir_grafo():
    for nodo, conexoes in sorted(adjacencias.items()):
        conexoes_str = ", ".join([f"({nodo2}, {dist})" for nodo2, dist in conexoes])
        print(f"{nodo}: [{conexoes_str}]")


if __name__ == "__main__":
    print("=" * 80)
    print("GRAFO DO MERCADO COM DISTÂNCIAS REALISTAS (EM METROS)")
    print("=" * 80)
    print("\nCoordernadas de referência (x, y):")
    for nodo, coord in sorted(coordenadas.items()):
        print(f"  {nodo}: {coord}")
    print("\n" + "=" * 80)
    print("LISTA DE ADJACÊNCIA COM PESOS:")
    print("=" * 80 + "\n")
    imprimir_grafo()

    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DO GRAFO:")
    print("=" * 80)
    total_arestas = sum(len(conexoes) for conexoes in adjacencias.values()) // 2
    distancia_media = sum(
        dist for conexoes in adjacencias.values() for _, dist in conexoes
    ) / (sum(len(conexoes) for conexoes in adjacencias.values()))
    print(f"Total de nós: {len(adjacencias)}")
    print(f"Total de arestas: {total_arestas}")
    print(f"Distância média entre nós: {distancia_media:.2f}m")
    print(
        f"Distância máxima: {max(max(dist for _, dist in conexoes) for conexoes in adjacencias.values()):.1f}m"
    )
    print(
        f"Distância mínima: {min(min(dist for _, dist in conexoes) for conexoes in adjacencias.values()):.1f}m"
    )
