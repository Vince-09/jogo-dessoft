import pygame
from config import FPS 
from fases import FASES, construir_fase
from sprites import Raposa


def game_screen(janela, assets):
     relogio = pygame.time.Clock() 
     grupos, inicio, largura_fase = construir_fase(FASES[0], assets)
     raposa = Raposa(assets, inicio[0], inicio[1])

     while True: 
        relogio.tick(FPS) 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                return 

        raposa.ler_teclado(pygame.key.get_pressed())
        raposa.update(grupos['blocos'])

        janela.blit(assets['fundo'], (0, 0)) 
        grupos['todos'].draw(janela)
        posicao = raposa.image.get_rect()
        posicao.midbottom = raposa.rect.midbottom
        janela.blit(raposa.image, posicao)
        pygame.display.update()





