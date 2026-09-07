# Grafo Ponderado do Mercado - Distâncias em Metros

## Metodologia de Ponderação

Este grafo foi ponderado com **distâncias realistas em metros** baseado no layout físico do supermercado fornecido. As coordenadas foram estimadas observando o mapa do mercado e utilizando a fórmula da distância euclidiana:

```
distância = √[(x₂ - x₁)² + (y₂ - y₁)²]
```

> Usamos coordenadas estimadas do layout para prototipagem. Para implementação em produção, seria necessário levantamento de campo com medições reais.

### Características do Mercado Modelado:

- **Dimensões aproximadas**: 72m × 30m
- **Total de nós**: 51
- **Total de arestas**: 158
- **Distância média entre nós conectados**: 9.68m
- **Distância mínima**: 2.0m (ex: G01 ↔ M01)
- **Distância máxima**: 67.0m (ex: P01 ↔ P02)

---

## Coordenadas dos Nós

| Nó | Coordenadas (x, y) | Seção | Descrição |
|----|-------------------|-------|-----------|
| A01 | (5, 28) | Açougue | Carnes e produtos de açougue |
| G01 | (12, 6) | Geladeiras | Bebidas geladas |
| G02 | (12, 10) | Geladeiras | Sobremesas |
| G03 | (12, 14) | Geladeiras | Massas frescas |
| G04 | (12, 18) | Geladeiras | Embutidos |
| G05 | (12, 22) | Geladeiras | Laticínios |
| G06 | (12, 26) | Geladeiras | Laticínios |
| F01 | (18, 26) | Freezers | Carnes vermelha |
| F02 | (18, 22) | Freezers | Cortes de frango |
| F03 | (18, 18) | Freezers | Peixes |
| F04 | (24, 26) | Freezers | Vegetais congelados |
| F05 | (24, 22) | Freezers | Polpas |
| F06 | (24, 18) | Freezers | Sobremesas |
| F07 | (30, 26) | Freezers | Panificação |
| F08 | (30, 22) | Freezers | Pratos prontos |
| F09 | (30, 18) | Freezers | Pratos prontos |
| M01 | (14, 6) | Frutas/Vegetais | Batata, cebola, raízes |
| M02 | (16, 10) | Frutas/Vegetais | Tomate, pimentão, abóbora |
| M03 | (20, 10) | Frutas/Vegetais | Bananas, maçãs, mamão |
| M04 | (19, 6) | Frutas/Vegetais | Laranja, limão, tangerina |
| M05 | (24, 10) | Frutas/Vegetais | Morango, uva, kiwi |
| M06 | (24, 6) | Frutas/Vegetais | Melancia, melão, abacaxi |
| M07 | (18, 14) | Frutas/Vegetais | Alface, couve, rúcula |
| M08 | (24, 14) | Frutas/Vegetais | Cheiro verde, hortelã |
| C01 | (70, 14) | Corredores | Bebidas alcoólicas |
| C02 | (66, 14) | Corredores | Shampoo, sabonetes |
| C03 | (62, 14) | Corredores | Higiene pessoal |
| C04 | (58, 14) | Corredores | Fraldas, algodão |
| C05 | (54, 14) | Corredores | Papel higiênico |
| C06 | (50, 14) | Corredores | Limpadores |
| C07 | (46, 14) | Corredores | Sabões e amaciantes |
| C08 | (42, 14) | Corredores | Organizadores, baldes |
| C09 | (38, 14) | Corredores | Utilidades domésticas |
| C10 | (34, 10) | Corredores | Leites e açúcares |
| C11 | (34, 18) | Corredores | Talheres, panelas |
| C12 | (38, 20) | Corredores | Papel alumínio |
| C13 | (42, 20) | Corredores | Farináceos |
| C14 | (46, 20) | Corredores | Azeites, vinagres |
| C15 | (50, 20) | Corredores | Molhos, macarrão |
| C16 | (54, 20) | Corredores | Café, alimentos infantis |
| C17 | (58, 20) | Corredores | Barras de cereais |
| C18 | (62, 20) | Corredores | Doces, chocolates |
| C19 | (66, 20) | Corredores | Biscoitos |
| C20 | (70, 20) | Corredores | Bebidas (água, suco) |
| X01 | (20, 4) | Caixas | Caixa 1 |
| X02 | (28, 4) | Caixas | Caixa 2 |
| X03 | (36, 4) | Caixas | Caixa 3 |
| X04 | (44, 4) | Caixas | Caixa 4 |
| X05 | (52, 4) | Caixas | Caixa 5 |
| P01 | (72, 0) | Entrada/Saída | Entrada |
| P02 | (5, 0) | Entrada/Saída | Saída |

---

## Lista de Adjacência com Pesos (Distância em Metros)

```
A01: [(G06, 7.3), (F01, 13.2), (F04, 19.1), (F07, 25.1)]
G06: [(A01, 7.3), (F01, 6.0), (F02, 7.2), (F03, 10.0), (G05, 4.0)]
G05: [(G06, 4.0), (F01, 7.2), (F02, 6.0), (F03, 7.2), (M07, 10.0), (G04, 4.0)]
G04: [(G05, 4.0), (F03, 6.0), (M07, 7.2), (M02, 8.9), (G03, 4.0)]
G03: [(G04, 4.0), (M01, 8.2), (M02, 5.7), (M07, 6.0), (G02, 4.0)]
G02: [(G03, 4.0), (M01, 4.5), (M02, 4.0), (G01, 4.0), (X01, 10.0), (P02, 12.2)]
G01: [(G02, 4.0), (M01, 2.0), (X01, 8.2), (P02, 9.2)]

F01: [(A01, 13.2), (G06, 6.0), (F02, 4.0), (F04, 6.0)]
F02: [(F01, 4.0), (G06, 7.2), (G05, 6.0), (F03, 4.0), (A01, 14.3)]
F03: [(F02, 4.0), (G05, 7.2), (G04, 6.0), (G03, 7.2), (F06, 6.0), (M07, 4.0), (M08, 7.2)]
F04: [(A01, 19.1), (F01, 6.0), (F07, 6.0), (F05, 4.0)]
F05: [(F04, 4.0), (F06, 4.0)]
F06: [(F05, 4.0), (F03, 6.0), (F09, 6.0), (M03, 8.9), (M07, 7.2), (M08, 4.0)]
F07: [(A01, 25.1), (F04, 6.0), (F08, 4.0), (C11, 8.9)]
F08: [(F07, 4.0), (F09, 4.0), (C11, 5.7)]
F09: [(F08, 4.0), (F06, 6.0), (M07, 12.6), (M08, 7.2), (M05, 10.0), (C10, 8.9), (C11, 4.0)]

M01: [(G02, 4.5), (G01, 2.0), (M02, 4.5), (M04, 5.0), (X01, 6.3)]
M02: [(M01, 4.5), (G03, 5.7), (G02, 4.0), (M03, 4.0), (M07, 4.5), (M04, 5.0)]
M03: [(M02, 4.0), (G04, 11.3), (M06, 5.7), (M07, 4.5), (M05, 4.0), (M04, 4.1), (M01, 7.2), (F06, 8.9)]
M04: [(M01, 5.0), (M05, 6.4), (M03, 4.1), (M06, 5.0), (X01, 2.2), (X02, 9.2)]
M05: [(M03, 4.0), (M06, 4.0), (M08, 4.0), (M04, 6.4), (X03, 13.4), (X04, 20.9), (C11, 12.8)]
M06: [(M04, 5.0), (M05, 4.0), (X02, 4.5), (X01, 4.5), (X03, 12.2), (C10, 10.8)]
M07: [(M02, 4.5), (M03, 4.5), (G04, 7.2), (G03, 6.0), (G05, 10.0), (M08, 6.0), (F09, 12.6), (F06, 7.2), (F03, 4.0)]
M08: [(M07, 6.0), (M05, 4.0), (F09, 7.2), (F06, 4.0), (F03, 7.2), (C11, 10.8), (C10, 10.8)]

C11: [(F07, 8.9), (F08, 5.7), (F09, 4.0), (M08, 10.8), (M05, 12.8), (C12, 4.5), (C10, 8.0), (C09, 5.7), (C08, 8.9)]
C12: [(C11, 4.5), (C10, 10.8), (C09, 6.0), (C08, 7.2), (C13, 4.0)]
C13: [(C12, 4.0), (C14, 4.0), (C08, 6.0), (C09, 7.2), (C07, 7.2)]
C14: [(C13, 4.0), (C15, 4.0), (C08, 7.2), (C07, 6.0), (C06, 7.2)]
C15: [(C14, 4.0), (C16, 4.0), (C07, 7.2), (C06, 6.0), (C05, 7.2)]
C16: [(C15, 4.0), (C17, 4.0), (C06, 7.2), (C05, 6.0), (C04, 7.2)]
C17: [(C16, 4.0), (C18, 4.0), (C05, 7.2), (C04, 6.0), (C03, 7.2)]
C18: [(C17, 4.0), (C19, 4.0), (C04, 7.2), (C03, 6.0), (C02, 7.2)]
C19: [(C18, 4.0), (C20, 4.0), (C03, 7.2), (C02, 6.0), (C01, 7.2)]
C20: [(C19, 4.0), (C01, 6.0)]

C01: [(C20, 6.0), (C19, 7.2), (C02, 4.0), (P01, 14.1)]
C02: [(C01, 4.0), (C03, 4.0), (P01, 15.2), (C20, 7.2), (C19, 6.0), (C18, 7.2)]
C03: [(C02, 4.0), (C04, 4.0), (C19, 7.2), (P01, 17.2), (C18, 6.0), (C17, 7.2)]
C04: [(C03, 4.0), (C05, 4.0), (C18, 7.2), (P01, 19.8), (X05, 11.7), (C17, 6.0), (C16, 7.2)]
C05: [(C04, 4.0), (C06, 4.0), (C17, 7.2), (P01, 22.8), (X05, 10.2), (C16, 6.0), (C15, 7.2)]
C06: [(C05, 4.0), (C07, 4.0), (C16, 7.2), (P01, 26.1), (X05, 10.2), (C15, 6.0), (C14, 7.2)]
C07: [(C06, 4.0), (C08, 4.0), (C15, 7.2), (X05, 11.7), (X04, 10.2), (C14, 6.0), (C13, 7.2)]
C08: [(C07, 4.0), (C09, 4.0), (C13, 6.0), (X05, 14.1), (X04, 10.2), (X03, 11.7), (C12, 7.2), (C11, 8.9), (C14, 7.2)]
C09: [(C08, 4.0), (C10, 5.7), (C11, 5.7), (X05, 17.2), (X04, 11.7), (X03, 10.2), (C12, 6.0), (C13, 7.2)]
C10: [(C09, 5.7), (C11, 8.0), (C12, 10.8), (X01, 15.2), (X02, 8.5), (X03, 6.3), (X04, 11.7), (X05, 19.0), (M06, 10.8), (M05, 10.0), (M08, 10.8), (F09, 8.9)]

X01: [(G01, 8.2), (G02, 10.0), (M01, 6.3), (M04, 2.2), (M06, 4.5), (X02, 8.0), (P02, 15.5), (P01, 52.2)]
X02: [(X01, 8.0), (M04, 9.2), (M05, 7.2), (M06, 4.5), (X03, 8.0), (P01, 44.2), (C10, 8.5)]
X03: [(X02, 8.0), (M05, 13.4), (M06, 12.2), (X04, 8.0), (P01, 36.2), (C10, 6.3), (C09, 10.2), (C08, 11.7)]
X04: [(X03, 8.0), (M05, 20.9), (C10, 11.7), (C09, 11.7), (C08, 10.2), (C07, 10.2), (C06, 11.7), (X05, 8.0), (P01, 28.3), (P02, 39.2)]
X05: [(X04, 8.0), (P01, 20.4), (P02, 47.2), (C06, 10.2), (C07, 11.7), (C08, 14.1), (C09, 17.2), (C10, 19.0), (C04, 11.7)]

P01: [(X01, 52.2), (X02, 44.2), (X03, 36.2), (X04, 28.3), (X05, 20.4), (P02, 67.0), (C06, 26.1), (C05, 22.8), (C04, 19.8), (C03, 17.2), (C02, 15.2), (C01, 14.1)]
P02: [(G01, 9.2), (G02, 12.2), (X01, 15.5), (X02, 23.3), (X03, 31.3), (X04, 39.2), (X05, 47.2), (P01, 67.0)]
```


### Padrões Identificados

- **Arestas mais curtas (2-4m)**: Dentro de mesma seção (freezers, geladeiras, frutas)
- **Arestas médias (6-8m)**: Entre seções adjacentes
- **Arestas longas (15+m)**: De entrada/saída até seções distantes
