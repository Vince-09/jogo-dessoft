"""Classes de todos os objetos do jogo (sprites)."""
import pygame
class Bloco(pygame.sprite.Sprite):
     """Um quadradinho sólido do cenário (chão ou plataforma)."""
     def __init__(self, imagem, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.image = imagem
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y


from config import (GRAVIDADE, VEL_MAX_QUEDA, VEL_PULO, VEL_ANDAR, VEL_AGACHADO)

class Raposa(pygame.sprite.Sprite):
    LARGURA_HITBOX = 34
    ALTURA_EM_PE = 52
    ALTURA_AGACHADA = 28

    def __init__(self, assets, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animacoes = assets["raposa"]
        self.assets = assets
        self.image = self.animacoes["parado"][0]

        self.rect = pygame.Rect(0,0, self.LARGURA_HITBOX, self.ALTURA_EM_PE)
        self.rect.midbottom = (x, y)
        self.y = float(self.rect.y)

        self.vx = 0
        self.vy = 0
        self.no_chao = False
        self.agachada = False
        self.direcao = 1


    def ler_teclado(self, teclas):
        self.vx = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vx = -VEL_ANDAR
            self.direcao = -1

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vx = VEL_ANDAR
            self.direcao = 1


    def mover(self, blocos):
        #eixo x
        self.rect.x += self.vx
        for bloco in pygame.sprite.spritecollide(self, blocos, False):
            if self.vx > 0:
                self.rect.right = bloco.rect.left
            elif self.vy < 0:
                self.rect.left = bloco.rect.right


        #eixo y com gravidade
        self.vy = min(self.vy + GRAVIDADE, VEL_MAX_QUEDA)
        self.y += self.vy
        self.rect.y = round(self.y)
        self.no_chao = False
        for bloco in pygame.sprite.spritecollide(self, blocos, False):
            if self.vy > 0:
                self.rect.bottom = bloco.rect.top
                self.no_chao = True
            elif self.vy < 0:
                self.rect.top = bloco.rect.bottom

            self.vy = 0
            self.y = float(self.rect.y)

        if self.rect.left < 0:
            self.rect.left = 0  #nao sai pela esquerda do mapa

    def update(self, blocos):
        self.mover(blocos)





     