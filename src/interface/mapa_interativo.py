import pygame
import json
import sys
from pathlib import Path

CAMINHO_RAIZ = Path(__file__).resolve().parents[2]
sys.path.append(str(CAMINHO_RAIZ))

from src.algoritmos.dijkstra import carregar_grafo, dijkstra, reconstruir_caminho

# ==========================================
# 1. CONFIGURAÇÕES DA TELA E ESCALA
# ==========================================
LARGURA_TELA = 1250
ALTURA_TELA = 700
LARGURA_MAPA = 880

# Escala ajustada para focar na planta gerada via código
ESCALA_X = 11.2   
ESCALA_Y = 18.5   
OFFSET_X = 30     
OFFSET_Y = 80     

MODO_DEBUG = False # Mude para True para ver os nós (bolinhas cinzas) do grafo

# Cores do Layout
PRETO = (20, 20, 25)
BRANCO = (255, 255, 255)
CHAO = (245, 245, 250)
LINHA_CHAO = (235, 235, 240)
PAREDE = (100, 100, 110)
COR_PRATELEIRA = (193, 154, 107) # Madeira
COR_GELADEIRA = (176, 224, 230)  
COR_FREEZER = (135, 206, 250)    
COR_HORTI = (144, 238, 144)      
COR_ACOUGUE = (255, 160, 122)    
COR_CAIXA = (255, 228, 181)      

CINZA = (235, 235, 235)
CINZA_ESCURO = (80, 80, 80)
VERDE = (40, 200, 40)
AZUL = (20, 130, 255)
VERMELHO = (230, 40, 40)
ROTA_COR = (255, 120, 0) # Laranja vibrante

# Catálogo Completo (44 Seções)
CATALOGO_UI = [
    {"no": "A01", "nome": "Açougue (Carnes)"},
    {"no": "G01", "nome": "Bebidas Geladas"},
    {"no": "G02", "nome": "Sobremesas Geladas"},
    {"no": "G03", "nome": "Massas Frescas"},
    {"no": "G04", "nome": "Embutidos"},
    {"no": "G05", "nome": "Laticínios"},
    {"no": "G06", "nome": "Laticínios (Parte 2)"},
    {"no": "F01", "nome": "Carnes Verm. Congeladas"},
    {"no": "F02", "nome": "Cortes de Frango"},
    {"no": "F03", "nome": "Peixes"},
    {"no": "F04", "nome": "Vegetais Congelados"},
    {"no": "F05", "nome": "Polpas"},
    {"no": "F06", "nome": "Sobremesas Congeladas"},
    {"no": "F07", "nome": "Panificação Congelada"},
    {"no": "F08", "nome": "Pratos Prontos 1"},
    {"no": "F09", "nome": "Pratos Prontos 2"},
    {"no": "M01", "nome": "Batata, Cebola, Raízes"},
    {"no": "M02", "nome": "Tomate, Pimentão"},
    {"no": "M03", "nome": "Bananas, Maçãs, Mamão"},
    {"no": "M04", "nome": "Laranja, Limão"},
    {"no": "M05", "nome": "Morango, Uva, Kiwi"},
    {"no": "M06", "nome": "Melancia, Melão, Abacaxi"},
    {"no": "M07", "nome": "Alface, Couve, Rúcula"},
    {"no": "M08", "nome": "Cheiro Verde, Hortelã"},
    {"no": "C01", "nome": "Whisky, Vodkas"},
    {"no": "C02", "nome": "Shampoo, Sabonetes"},
    {"no": "C03", "nome": "Higiene Pessoal"},
    {"no": "C04", "nome": "Fraldas, Algodão"},
    {"no": "C05", "nome": "Papel Higiênico"},
    {"no": "C06", "nome": "Limpadores e Álcool"},
    {"no": "C07", "nome": "Sabão e Amaciante"},
    {"no": "C08", "nome": "Organizadores, Baldes"},
    {"no": "C09", "nome": "Utilidades Domésticas"},
    {"no": "C10", "nome": "Leites e Açúcares"},
    {"no": "C11", "nome": "Talheres, Pet Shop"},
    {"no": "C12", "nome": "Papel Alumínio"},
    {"no": "C13", "nome": "Farináceos, Pipocas"},
    {"no": "C14", "nome": "Azeites, Vinagres"},
    {"no": "C15", "nome": "Macarrão e Molhos"},
    {"no": "C16", "nome": "Café, Alimentos Infantis"},
    {"no": "C17", "nome": "Barra de Cereais, Fitness"},
    {"no": "C18", "nome": "Doces, Chocolates"},
    {"no": "C19", "nome": "Biscoitos"},
    {"no": "C20", "nome": "Água, Sucos, Cervejas"}
]

def carregar_coordenadas():
    caminho_json = CAMINHO_RAIZ / "dados" / "grafo_ponderado.json"
    with open(caminho_json, 'r', encoding='utf-8') as f:
        return json.load(f)['coordenadas']

def para_pixel(coord):
    """Converte metros para pixels, invertendo o eixo Y"""
    x_metros, y_metros = coord
    pos_x = int(x_metros * ESCALA_X + OFFSET_X)
    pos_y = int(ALTURA_TELA - (y_metros * ESCALA_Y + OFFSET_Y))
    return (pos_x, pos_y)

def desenhar_retangulo_metros(tela, cor, x_m, y_m_bottom, larg_m, alt_m, tipo=""):
    top_left = para_pixel((x_m, y_m_bottom + alt_m))
    bottom_right = para_pixel((x_m + larg_m, y_m_bottom))
    w = bottom_right[0] - top_left[0]
    h = bottom_right[1] - top_left[1]
    
    rect = pygame.Rect(top_left[0], top_left[1], w, h)
    
    # Sombra
    sombra = pygame.Surface((w, h), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 40)) 
    tela.blit(sombra, (rect.x + 3, rect.y + 3))

    pygame.draw.rect(tela, cor, rect, border_radius=3)
    pygame.draw.rect(tela, PAREDE, rect, 1, border_radius=3)

    # Detalhes visuais para realismo
    if tipo == "prateleira":
        for i in range(1, int(alt_m)):
            y_linha = top_left[1] + (h / alt_m) * i
            pygame.draw.line(tela, (160, 120, 80), (rect.x + 2, y_linha), (rect.right - 3, y_linha), 1)

def desenhar_rotulo(tela, fonte, texto, x_m, y_m):
    """Desenha Rótulos das Seções com fundo semi-transparente"""
    txt_surf = fonte.render(texto, True, PRETO)
    bg_surf = pygame.Surface((txt_surf.get_width() + 8, txt_surf.get_height() + 4), pygame.SRCALPHA)
    bg_surf.fill((255, 255, 255, 200)) 
    pos = para_pixel((x_m, y_m))
    tela.blit(bg_surf, (pos[0] - 4, pos[1] - 2))
    tela.blit(txt_surf, pos)

def desenhar_planta_mercado(tela, fonte_titulos):
    # Fundo (Chão)
    top_left = para_pixel((0, 31))
    bottom_right = para_pixel((76, -2))
    piso_rect = pygame.Rect(top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
    pygame.draw.rect(tela, CHAO, piso_rect)
    
    # Textura de azulejos
    for x in range(piso_rect.left, piso_rect.right, 40):
        pygame.draw.line(tela, LINHA_CHAO, (x, piso_rect.top), (x, piso_rect.bottom), 1)
    for y in range(piso_rect.top, piso_rect.bottom, 40):
        pygame.draw.line(tela, LINHA_CHAO, (piso_rect.left, y), (piso_rect.right, y), 1)
        
    pygame.draw.rect(tela, PAREDE, piso_rect, 3)

    # Açougue
    desenhar_retangulo_metros(tela, COR_ACOUGUE, 2, 29, 6, 2)
    desenhar_rotulo(tela, fonte_titulos, "AÇOUGUE", 2.5, 30.5)

    # Geladeiras (Peça inteira)
    desenhar_retangulo_metros(tela, COR_GELADEIRA, 7, 4, 3, 23)
    desenhar_rotulo(tela, fonte_titulos, "GELADEIRAS", 6.2, 28)

    # Freezers (Divididos para não bloquear a rota Y=18, Y=22, Y=26)
    for x_f in [20, 26]:
        for y_f in [19, 23]:
            desenhar_retangulo_metros(tela, COR_FREEZER, x_f, y_f, 3, 2)
    desenhar_rotulo(tela, fonte_titulos, "FREEZERS", 22, 27)

    # Hortifruti (Divididos para não bloquear a rota Y=6, 10, 14)
    for x_h in [15, 21]:
        for y_h in [7, 11]:
            desenhar_retangulo_metros(tela, COR_HORTI, x_h, y_h, 2, 2)
    desenhar_rotulo(tela, fonte_titulos, "HORTIFRUTI", 15.5, 14.5)

    # Prateleiras / Corredores Gerais (Divididas ao meio para o corredor central Y=14)
    for x_c in [35.5, 39.5, 43.5, 47.5, 51.5, 55.5, 59.5, 63.5, 67.5]:
        desenhar_retangulo_metros(tela, COR_PRATELEIRA, x_c, 11, 1.5, 2, "prateleira") # Parte de baixo
        desenhar_retangulo_metros(tela, COR_PRATELEIRA, x_c, 15, 1.5, 4, "prateleira") # Parte de cima
    desenhar_rotulo(tela, fonte_titulos, "CORREDORES GERAIS", 47, 21)

    # Caixas
    for x_cx in [20, 28, 36, 44, 52]:
        desenhar_retangulo_metros(tela, COR_CAIXA, x_cx - 1.5, 1.5, 3, 1.5)
    desenhar_rotulo(tela, fonte_titulos, "CAIXAS", 34, 3.5)

def desenhar_linha_ortogonal(tela, p1_px, p2_px, coord1_m, coord2_m):
    """Garante que a linha desvie das prateleiras, roteando apenas pelas 'avenidas' vazias"""
    x1, y1 = coord1_m
    x2, y2 = coord2_m
    
    if x1 == x2 or y1 == y2:
        pygame.draw.line(tela, ROTA_COR, p1_px, p2_px, 4)
        return

    # Eixos Y do mercado onde não existem móveis
    avenidas_y = [0, 4, 6, 10, 14, 18, 20, 22, 26, 28]

    # Escolhe a avenida para fazer o "cotovelo" da curva
    if y1 in avenidas_y:
        cotovelo = para_pixel((x2, y1))
    elif y2 in avenidas_y:
        cotovelo = para_pixel((x1, y2))
    else:
        cotovelo = para_pixel((x2, y1))

    pygame.draw.line(tela, ROTA_COR, p1_px, cotovelo, 4)
    pygame.draw.line(tela, ROTA_COR, cotovelo, p2_px, 4)
    pygame.draw.circle(tela, ROTA_COR, cotovelo, 2) 

def calcular_rota_completa(grafo, itens_selecionados):
    origem_atual = "P01"
    nao_visitados = itens_selecionados.copy()
    pontos_parada = ["P01"]
    distancia_total = 0.0 
    
    while nao_visitados:
        distancias, _ = dijkstra(grafo, origem_atual)
        mais_proximo = min(nao_visitados, key=lambda no: distancias[no])
        distancia_total += distancias[mais_proximo]
        pontos_parada.append(mais_proximo)
        origem_atual = mais_proximo
        nao_visitados.remove(mais_proximo)
        
    dist_caixa, _ = dijkstra(grafo, origem_atual)
    distancia_total += dist_caixa["X01"]
    pontos_parada.append("X01") 
    
    dist_saida, _ = dijkstra(grafo, "X01")
    distancia_total += dist_saida["P02"]
    pontos_parada.append("P02") 
    
    caminho_final_passo_a_passo = []
    for i in range(len(pontos_parada) - 1):
        origem_trecho = pontos_parada[i]
        destino_trecho = pontos_parada[i+1]
        _, preds = dijkstra(grafo, origem_trecho)
        trecho = reconstruir_caminho(preds, origem_trecho, destino_trecho)
        if trecho:
            if i > 0: trecho = trecho[1:]
            caminho_final_passo_a_passo.extend(trecho)
            
    return caminho_final_passo_a_passo, pontos_parada, distancia_total

def desenhar_texto_quebrado(tela, texto, fonte, cor, x, y, max_largura):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        if fonte.size(teste_linha)[0] < max_largura:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)
    
    for i, linha in enumerate(linhas):
        tela.blit(fonte.render(linha, True, cor), (x, y + i * (fonte.get_linesize() + 2)))

def rodar_mapa():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Otimizador de Rotas - Supermercado Dijkstra")
    fonte_micro = pygame.font.SysFont("Segoe UI", 10, bold=True)
    fonte = pygame.font.SysFont("Segoe UI", 14, bold=True)
    fonte_pequena = pygame.font.SysFont("Segoe UI", 12)
    fonte_titulo = pygame.font.SysFont("Segoe UI", 20, bold=True)
    fonte_mapa = pygame.font.SysFont("Segoe UI", 11, bold=True)
    relogio = pygame.time.Clock()

    coordenadas = carregar_coordenadas()
    grafo = carregar_grafo(str(CAMINHO_RAIZ / "dados" / "grafo_ponderado.json"))

    estado = "SELECAO"
    itens_selecionados = set()
    scroll_y = 0  
    
    botao_calcular = pygame.Rect(LARGURA_MAPA + 20, ALTURA_TELA - 60, LARGURA_TELA - LARGURA_MAPA - 40, 40)
    botao_voltar = pygame.Rect(LARGURA_MAPA + 20, ALTURA_TELA - 60, LARGURA_TELA - LARGURA_MAPA - 40, 40)

    caminho_animacao = []
    pontos_parada = []
    distancia_final = 0.0
    indice_carrinho = 0
    contador_frames = 0
    frames_por_no = 8 

    rodando = True
    while rodando:
        pos_mouse = pygame.mouse.get_pos()
        altura_total_lista = len(CATALOGO_UI) * 35
        scroll_maximo = min(0, ALTURA_TELA - 160 - altura_total_lista)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEWHEEL:
                if estado == "SELECAO" or estado == "SIMULACAO":
                    scroll_y += evento.y * 30
                    scroll_y = max(scroll_maximo, min(0, scroll_y))
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado == "SELECAO":
                    for i, item in enumerate(CATALOGO_UI):
                        rect_item = pygame.Rect(LARGURA_MAPA + 20, 80 + scroll_y + (i * 35), LARGURA_TELA - LARGURA_MAPA - 40, 30)
                        if 70 < rect_item.centery < ALTURA_TELA - 70:
                            if rect_item.collidepoint(pos_mouse):
                                if item["no"] in itens_selecionados: itens_selecionados.remove(item["no"])
                                else: itens_selecionados.add(item["no"])
                                
                    if botao_calcular.collidepoint(pos_mouse) and len(itens_selecionados) > 0:
                        caminho_animacao, pontos_parada, distancia_final = calcular_rota_completa(grafo, list(itens_selecionados))
                        indice_carrinho = 0
                        contador_frames = 0
                        scroll_y = 0
                        estado = "SIMULACAO"
                
                elif estado == "SIMULACAO":
                    if botao_voltar.collidepoint(pos_mouse):
                        estado = "SELECAO"
                        itens_selecionados.clear()
                        caminho_animacao = []
                        scroll_y = 0

        # ================= DESENHO DO MAPA =================
        tela.fill((0,0,0))
        desenhar_planta_mercado(tela, fonte_mapa)

        # Desenha a Rota desviando das prateleiras
        if estado == "SIMULACAO" and caminho_animacao:
            for i in range(len(caminho_animacao) - 1):
                n1 = caminho_animacao[i]
                n2 = caminho_animacao[i+1]
                p1_px = para_pixel(coordenadas[n1])
                p2_px = para_pixel(coordenadas[n2])
                desenhar_linha_ortogonal(tela, p1_px, p2_px, coordenadas[n1], coordenadas[n2])

        # Nós do Grafo
        if MODO_DEBUG or estado == "SELECAO":
            for no, coord in coordenadas.items():
                pos = para_pixel(coord)
                pygame.draw.circle(tela, CINZA_ESCURO, pos, 3)
                if MODO_DEBUG:
                    tela.blit(fonte_micro.render(no, True, CINZA_ESCURO), (pos[0] + 5, pos[1] - 5))

        # Indicadores de Entrada, Saída e Itens Selecionados
        for no in itens_selecionados:
            pygame.draw.circle(tela, AZUL, para_pixel(coordenadas[no]), 8)
            pygame.draw.circle(tela, BRANCO, para_pixel(coordenadas[no]), 8, 2)
            
        pos_p01 = para_pixel(coordenadas["P01"])
        pygame.draw.circle(tela, VERDE, pos_p01, 10) 
        desenhar_rotulo(tela, fonte_mapa, "ENTRADA", 70.5, -2)

        pos_p02 = para_pixel(coordenadas["P02"])
        pygame.draw.circle(tela, VERMELHO, pos_p02, 10)
        desenhar_rotulo(tela, fonte_mapa, "SAÍDA", 4, -2)

        # ================= DESENHO DA INTERFACE =================
        pygame.draw.rect(tela, BRANCO, (LARGURA_MAPA, 0, LARGURA_TELA - LARGURA_MAPA, ALTURA_TELA))
        pygame.draw.line(tela, CINZA_ESCURO, (LARGURA_MAPA, 0), (LARGURA_MAPA, ALTURA_TELA), 2)
        
        if estado == "SELECAO":
            area_scroll = pygame.Rect(LARGURA_MAPA, 70, LARGURA_TELA - LARGURA_MAPA, ALTURA_TELA - 140)
            tela.set_clip(area_scroll)
            for i, item in enumerate(CATALOGO_UI):
                rect_item = pygame.Rect(LARGURA_MAPA + 20, 80 + scroll_y + (i * 35), LARGURA_TELA - LARGURA_MAPA - 40, 30)
                cor_btn = AZUL if item["no"] in itens_selecionados else CHAO
                pygame.draw.rect(tela, cor_btn, rect_item, border_radius=6)
                pygame.draw.rect(tela, CINZA_ESCURO, rect_item, 1, border_radius=6)
                cor_texto = BRANCO if item["no"] in itens_selecionados else PRETO
                txt = fonte.render(item["nome"], True, cor_texto)
                tela.blit(txt, (rect_item.x + 10, rect_item.y + 6))
                
        elif estado == "SIMULACAO":
            area_scroll = pygame.Rect(LARGURA_MAPA, 70, LARGURA_TELA - LARGURA_MAPA, ALTURA_TELA - 260)
            tela.set_clip(area_scroll)
            y_texto = 80 + scroll_y
            passo = 1
            for parada in pontos_parada:
                if parada in ["P01", "P02", "X01"]: continue 
                nome_parada = parada
                for item in CATALOGO_UI:
                    if item["no"] == parada: nome_parada = item["nome"]
                
                txt = fonte.render(f"{passo}. {nome_parada}", True, PRETO)
                tela.blit(txt, (LARGURA_MAPA + 20, y_texto))
                y_texto += 35
                passo += 1

        tela.set_clip(None)

        if estado == "SELECAO":
            pygame.draw.rect(tela, BRANCO, (LARGURA_MAPA + 1, 0, LARGURA_TELA - LARGURA_MAPA - 1, 70))
            tit = fonte_titulo.render("O que deseja comprar?", True, PRETO)
            tela.blit(tit, (LARGURA_MAPA + 20, 25))
            
            pygame.draw.rect(tela, BRANCO, (LARGURA_MAPA + 1, ALTURA_TELA - 80, LARGURA_TELA - LARGURA_MAPA - 1, 80))
            cor_calc = VERDE if len(itens_selecionados) > 0 else CINZA_ESCURO
            pygame.draw.rect(tela, cor_calc, botao_calcular, border_radius=8)
            txt_calc = fonte_titulo.render("Traçar Rota", True, BRANCO)
            tela.blit(txt_calc, (botao_calcular.x + 105, botao_calcular.y + 8))
            
        elif estado == "SIMULACAO":
            pygame.draw.rect(tela, BRANCO, (LARGURA_MAPA + 1, 0, LARGURA_TELA - LARGURA_MAPA - 1, 70))
            tit = fonte_titulo.render("Ordem Sugerida", True, PRETO)
            tela.blit(tit, (LARGURA_MAPA + 20, 25))
            
            pygame.draw.rect(tela, BRANCO, (LARGURA_MAPA + 1, ALTURA_TELA - 190, LARGURA_TELA - LARGURA_MAPA - 1, 190))
            pygame.draw.rect(tela, VERMELHO, botao_voltar, border_radius=8)
            txt_voltar = fonte_titulo.render("Nova Lista", True, BRANCO)
            tela.blit(txt_voltar, (botao_voltar.x + 105, botao_voltar.y + 8))

            if caminho_animacao:
                if indice_carrinho < len(caminho_animacao):
                    contador_frames += 1
                    if contador_frames >= frames_por_no:
                        indice_carrinho += 1
                        contador_frames = 0
                
                idx_desenho = min(indice_carrinho, len(caminho_animacao) - 1)
                pos_carrinho = para_pixel(coordenadas[caminho_animacao[idx_desenho]])
                
                # Carrinho do cliente
                pygame.draw.circle(tela, VERMELHO, pos_carrinho, 10)
                pygame.draw.circle(tela, BRANCO, pos_carrinho, 10, 2)
                guidao = pygame.Rect(pos_carrinho[0] - 8, pos_carrinho[1] + 6, 16, 4)
                pygame.draw.rect(tela, CINZA_ESCURO, guidao, border_radius=2)

                # EXIBIR RESULTADOS NO FINAL
                if indice_carrinho >= len(caminho_animacao):
                    txt_dist = fonte_titulo.render(f"Distância: {distancia_final:.1f} m", True, AZUL)
                    tela.blit(txt_dist, (LARGURA_MAPA + 20, ALTURA_TELA - 175))
                    
                    txt_vert_tit = fonte.render("Vértices Percorridos:", True, PRETO)
                    tela.blit(txt_vert_tit, (LARGURA_MAPA + 20, ALTURA_TELA - 145))
                    
                    texto_vertices = " -> ".join(caminho_animacao)
                    desenhar_texto_quebrado(tela, texto_vertices, fonte_pequena, CINZA_ESCURO, 
                                            LARGURA_MAPA + 20, ALTURA_TELA - 125, LARGURA_TELA - LARGURA_MAPA - 40)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()

if __name__ == "__main__":
    rodar_mapa()