import pygame
from config import FPS 
from fases import FASES, construir_fase
def game_screen(janela, assets):
     relogio = pygame.time.Clock() 
     grupos, inicio, largura_fase = construir_fase(FASES[0], assets)
     while True: 
        relogio.tick(FPS) 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                return 
        janela.blit(assets['fundo'], (0, 0)) 
        grupos['todos'].draw(janela) 
        pygame.display.update()