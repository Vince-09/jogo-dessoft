"""Mapas das fases e a função que transforma um mapa em sprites."""
import pygame
from config import TAM_BLOCO
from sprites import Bloco, Obstaculo, PilhaDeProvas, Inimigo, Moeda, Bandeira

FASE_1 = [
    '..............................................................',
    '..............................................................',
    '..............................................................',
    '..............................................................',
    '..............................................................',
    '.....MM......................M................................',
    '....BBBB....................BBB............MM.................',
    '..................................MM..........................',
    '..............................................................',
    '.J...........E.......C....A.....M...I...E.....A...C..M..I...F.',
    'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG..GGGGGGGGGGGGGGGGGGGGGGGGGG',
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT..TTTTTTTTTTTTTTTTTTTTTTTTTT',
]

FASES = [FASE_1]


def construir_fase(mapa, assets):
    """Percorre o mapa e cria um sprite para cada caractere."""
    grupos = {
        'blocos': pygame.sprite.Group(),   # chão e plataformas (sólidos)
        "perigos": pygame.sprite.Group(), #todos que tiram vida ao encostar
        "cortaveis": pygame.sprite.Group(), #todos que a faca destói
        "inimigos": pygame.sprite.Group(), 
        "moedas": pygame.sprite.Group(),
        "bandeira": pygame.sprite.Group(),
        'todos': pygame.sprite.Group(),  
          # usado para desenhar
    }
    inicio = (0, 0)
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])):
            letra = mapa[linha][coluna]
            x = coluna * TAM_BLOCO
            y = linha * TAM_BLOCO
            chao_do_bloco = y + TAM_BLOCO   # base do quadradinho
            if letra == 'G':
                novo = Bloco(assets['grama'], x, y)
                grupos['blocos'].add(novo)
                grupos['todos'].add(novo)
            elif letra == 'T':
                novo = Bloco(assets['terra'], x, y)
                grupos['blocos'].add(novo)
                grupos['todos'].add(novo)
            elif letra == 'B':
                novo = Bloco(assets['bloco'], x, y)
                grupos['blocos'].add(novo)
                grupos['todos'].add(novo)
            elif letra == "E":
                novo = Obstaculo(assets["espinho"], x + TAM_BLOCO // 2, chao_do_bloco)
                grupos["perigos"].add(novo)
                grupos["todos"].add(novo)
            elif letra == "A":
                if linha == 0 or mapa[coluna][linha-1] != "A":
                    novo = Obstaculo(assets["galho"], x + TAM_BLOCO // 2, 360)
                    grupos["perigos"].add(novo)
                    grupos["todos"].add(novo)
            elif letra == "C":
                novo = PilhaDeProvas(assets["provas"], x + TAM_BLOCO // 2, chao_do_bloco)
                grupos["blocos"].add(novo)
                grupos["cortaveis"].add(novo)
                grupos["todos"].add(novo)
            elif letra == "I":
                novo = Inimigo(assets["inimigo"], x + TAM_BLOCO // 2, chao_do_bloco)
                grupos["inimigos"].add(novo)
                grupos["perigos"].add(novo)
                grupos["cortaveis"].add(novo)
                grupos["todos"].add(novo)
            elif letra == "M":
                novo = Moeda(assets["moeda"], x + TAM_BLOCO // 2, y+TAM_BLOCO//2)
                grupos["moedas"].add(novo)
                grupos["todos"].add(novo)
            elif letra == "F":
                novo = Bandeira(assets["bandeira"], x + TAM_BLOCO // 2, chao_do_bloco)
                grupos["bandeira"].add(novo)
                grupos["todos"].add(novo)
            elif letra == 'J':
                inicio = (x + TAM_BLOCO // 2, chao_do_bloco)

    largura_fase = len(mapa[0]) * TAM_BLOCO
    return grupos, inicio, largura_fase