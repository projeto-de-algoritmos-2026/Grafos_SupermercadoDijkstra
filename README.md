# G35_Grafos_PA-26.2

## Estrutura

- `src/algoritmos/`: implementações de Dijkstra, matriz de distâncias e nearest neighbor.
- `dados/`: grafo ponderado em JSON e código usado para gerar/modelar o grafo.
- `docs/`: escopo, documentação técnica, tabela do mercado e descrição do grafo.
- `assets/`: imagens do mapa e do grafo.

## Execução

Na raiz do projeto:

```bash
python -m src.algoritmos.dijkstra
python -m src.algoritmos.matriz_distancias --teste
python -m src.algoritmos.nearest_neighbor --teste
```