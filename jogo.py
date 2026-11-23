"""Arquivo principal. Para jogar: python3 jogo.py"""
import pygame
from config import LARGURA, ALTURA, TITULO, SAIR, INICIO, INSTRUCOES, JOGANDO, GAME_OVER, VITORIA
from assets import load_assets
from telas import tela_inicio, tela_instrucoes, tela_fim
from game_screen import game_screen

# ----- Inicialização -----
pygame.init()
pygame.mixer.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
assets = load_assets()

# ----- Máquina de estados -----
estado = INICIO
pontos = 0
tempo_ms = 0
while estado != SAIR:
    if estado == INICIO:
        estado = tela_inicio(janela, assets)
    elif estado == INSTRUCOES:
        estado = tela_instrucoes(janela, assets)
    elif estado == JOGANDO:
        estado, pontos, tempo_ms = game_screen(janela, assets)
    elif estado == GAME_OVER:
        estado = tela_fim(janela, assets, False, pontos, tempo_ms)
    elif estado == VITORIA:
        estado = tela_fim(janela, assets, True, pontos, tempo_ms)
# ----- Finalização -----
pygame.quit()