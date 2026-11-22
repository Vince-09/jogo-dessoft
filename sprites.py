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


from config import (GRAVIDADE, INTERVALO_CORTE, VEL_MAX_QUEDA, VEL_PULO, VEL_ANDAR, VEL_AGACHADO)

class Corte(pygame.sprite.Sprite):
    "o golpe de faquinha da raposa. aparece na frente da raposa e some sozinho"

    def __init__(self, assets, raposa):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem
        self.rect = self.image.get_rect()
        self.raposa = raposa
        self.criado_em = pygame.time.get_ticks()
        if raposa.direcao == -1:
            self.image = pygame.transform.flip(imagem, True, False)
        self.posicionar()


    def posicionar(self):
        "coloca o corte na frente da raposa (15 pixles por cima dela, para acertar os obstaculos mesmo com a raposa encostada neles)"
        self.rect.centery = self.raposa.rect.centery
        if self.raposa.direcao == 1:
            self.rect.left = self.raposa.rect.right - 15
        else:
            self.rect.right = self.raposa.rect.left + 15


    def update(self):
        self.posicionar()
        if pygame.time.get_ticks() - self.criado_em > DURACAO_CORTE:
            self.kill()

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

        self.ultimo_corte = -INTERVALO_CORTE
        self.invencivel_ate = 0



    def ler_teclado(self, teclas):

        self.agachar(teclas[pygame.K_DOWN] or teclas[pygame.K_s])
        if self.agachada == True:
            velocidade = VEL_AGACHADO
        else:
            velocidade = VEL_ANDAR

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
            elif self.vx < 0:
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

    
    def pular(self):
        if self.no_chao and not self.agachada:
            self.vy = VEL_PULO
            self.no_chao = False
            self.assets["som pulo"].play()


    def agachar(self, agachar):
        if agachar == self.agachada or not self.no_chao and quer_agachar:
            return
        base = self.rect.midbottom
        self.agachada = quer_agachar
        if self.agachada:
            self.rect.height = self.ALTURA_AGACHADA
        else:
            self.rect.height = self.ALTURA_EM_PE
        self.rect.midbottom = base
        self.y = float(self.rect.y)


    def cortar(self, grupos):
        "cria um golpe de faca (se ja passou do intervalo minimo)"
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_corte < INTERVALO_CORTE:
            return
        self.ultimo_corte = agora
        golpe = Corte(self.assets["corte"], self)
        grupos["cortes"].add(golpe)
        self.assets["som corte"].play()

    






     