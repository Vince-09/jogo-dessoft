import pygame
from config import FPS, LARGURA
from fases import FASES, construir_fase
from sprites import Raposa
from camera import Camera


def desenhar_cenario(janela, assets, camera):
    """Sensação de profundidade para o cenario, por deixar os prédios andando mais lento"""
    janela.blit(assets['fundo'], (0, 0))
    x = -(camera.deslocamento_x * 0.3) % LARGURA
    janela.blit(assets['predios'], (x - LARGURA, 0))
    janela.blit(assets['predios'], (x, 0))

def game_screen(janela, assets):
     """Loop da fase: move a raposa, a câmera segue e tudo é desenhado"""
     relogio = pygame.time.Clock() 
     grupos, inicio, largura_fase = construir_fase(FASES[0], assets)
     raposa = Raposa(assets, inicio[0], inicio[1])
     camera = Camera(largura_fase)

     while True: 
        relogio.tick(FPS) 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                return 

        raposa.ler_teclado(pygame.key.get_pressed())
        raposa.update(grupos['blocos'])
        camera.seguir(raposa)

        desenhar_cenario(janela, assets, camera) 
        for sprite in grupos['todos']:            
            janela.blit(sprite.image, camera.posicao_na_tela(sprite))
        janela.blit(raposa.image, camera.posicao_na_tela(raposa))   
        pygame.display.update()
