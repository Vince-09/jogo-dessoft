import pygame
from config import FPS, LARGURA, PONTOS_MOEDA, PONTOS_INIMIGO, PONTOS_PROVAS, PRETO, TEMPO_INVENCIVEL
from fases import FASES, construir_fase
from sprites import Raposa, PilhaDeProvas, Inimigo
from camera import Camera


def desenhar_cenario(janela, assets, camera):
    """Sensação de profundidade para o cenario, por deixar os prédios andando mais lento"""
    janela.blit(assets['fundo'], (0, 0))
    x = -(camera.deslocamento_x * 0.3) % LARGURA
    janela.blit(assets['predios'], (x - LARGURA, 0))
    janela.blit(assets['predios'], (x, 0))
def desenhar_hud(janela, assets, vidas, pontos, numero_fase):
    """Desenha vidas, pontos e fase no topo da tela."""   
    for i in range(vidas):      
        janela.blit(assets['coracao'], (10 + i * 30, 10))   
    texto = assets['fonte_pequena'].render(f'Pontos: {pontos}', True, PRETO)  
    janela.blit(texto, (LARGURA - 170, 12))   
    texto = assets['fonte_pequena'].render(f'Fase {numero_fase}', True, PRETO)   
    janela.blit(texto, (LARGURA // 2 - 30, 12))
def game_screen(janela, assets):
     """Loop da fase: move a raposa, a câmera segue e tudo é desenhado"""
     relogio = pygame.time.Clock() 
     grupos, inicio, largura_fase = construir_fase(FASES[0], assets)
     grupos["cortes"] = pygame.sprite.Group()
     raposa = Raposa(assets, inicio[0], inicio[1])
     camera = Camera(largura_fase)
     pontos = 0

     while True: 
        relogio.tick(FPS) 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                return 

            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_UP, pygame.K_w, pygame.K_SPACE]:
                    raposa.pular()
                if evento.key in [pygame.K_x, pygame.K_k, pygame.K_c]:
                    raposa.cortar(grupos)

        raposa.ler_teclado(pygame.key.get_pressed())
        raposa.update(grupos['blocos'])
        grupos['todos'].update()                 
        grupos["cortes"].update()

        acertos = pygame.sprite.groupcollide(grupos['cortes'], grupos['cortaveis'], False, True)
        for alvos in acertos.values():
            for alvo in alvos:
                if isinstance(alvo, PilhaDeProvas):
                    pontos += PONTOS_PROVAS
                elif isinstance(alvo, Inimigo):
                    pontos += PONTOS_INIMIGO

        #pular em cima do jacaré (como no Mario Bros)
        for inimigo in pygame.sprite.spritecollide(raposa, grupos['inimigos'], False):
            if raposa.vy > 0 and raposa.rect.bottom - inimigo.rect.top < 20:
                inimigo.kill()
                raposa.vy = -10  # quicada
                pontos += PONTOS_INIMIGO

        moedas_pegas = pygame.sprite.spritecollide(raposa, grupos['moedas'], True)
        if len(moedas_pegas) > 0:
            pontos += PONTOS_MOEDA * len(moedas_pegas)

        camera.seguir(raposa)

        desenhar_cenario(janela, assets, camera) 
        for sprite in grupos['todos']:            
            janela.blit(sprite.image, camera.posicao_na_tela(sprite))
        janela.blit(raposa.image, camera.posicao_na_tela(raposa))
        for golpe in grupos["cortes"]:
            janela.blit(golpe.image, camera.posicao_na_tela(golpe))
        pygame.display.update()
def levar_dano(self):
    """Fica invencível por um tempo e dá um pulinho.""" 
    self.invencivel_ate = pygame.time.get_ticks() + TEMPO_INVENCIVEL 
    self.vy = -8
    self.assets['som_dano'].play()
def esta_invencivel(self):
    return pygame.time.get_ticks() < self.invencivel_ate



