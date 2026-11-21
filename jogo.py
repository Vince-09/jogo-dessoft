"""Arquivo principal. Para jogar"""
import pygame
from config import LARGURA, ALTURA, TITULO
from assets import load_assets
from game_screen import game_screen

# ----- Inicialização -----
pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
assets = load_assets()

# ----- Roda a fase -----
game_screen(janela, assets)

# ----- Finalização -----
pygame.quit()