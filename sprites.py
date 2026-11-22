"""Classes de todos os objetos do jogo (sprites)."""
import pygame
from config import (GRAVIDADE, INTERVALO_CORTE, TEMPO_FRAME, TEMPO_INVENCIVEL, VEL_MAX_QUEDA, VEL_PULO, VEL_ANDAR, VEL_AGACHADO, DURACAO_CORTE)

class Bloco(pygame.sprite.Sprite):
     """Um quadradinho sólido do cenário (chão ou plataforma)."""
     def __init__(self, imagem, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.image = imagem
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y


class Obstaculo(pygame.sprite.Sprite):
    "obstaculo parado que tira vida (espinho ou galho). (x,y) é o ponto midbottom do obstaculo"

    def __init__(self, imagem, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

class PilhaDeProvas(Obstaculo):
    "pilha de provas empilhadas que não da para pular, precisam ser cortadas"

class Bandeira(Obstaculo):
    "fim da fase"


class Animado(pygame.sprite.Sprite):
    "sprite animado (que troca de imagem de tempos em tempos)"

    def __init__(self, quadros, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.quadros = quadros
        self.quadro_atual = 0
        self.image = self.quadros[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.ultimo_quadro = pygame.time.get_ticks()

    def animar(self):
        "muda de quadro se já deu o tempo"
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_quadro > TEMPO_FRAME:
            self.ultimo_quadro = agora
            self.quadro_atual = (self.quadro_atual + 1) % len(self.quadros)
            self.image = self.quadros[self.quadro_atual]

    def update(self):
        self.animar()


class Moeda(Animado):
    "moeda girando que da pontos"

    def __init__(self, quadros, x, y):
        Animado.__init__(self, quadros, x, y)
        self.rect.center = (x, y)


class Inimigo(Animado):
    "jacaré que anda de um lado pro outro"

    def __init__(self, quadros, x, y,distancia=60):
        Animado.__init__(self, quadros, x, y)
        self.x_inicial = x
        self.distancia = distancia
        self.velocidade = 1.5
        self.x = float(x)
        self.virado_esquerda = True

    def update(self):
        if self.virado_esquerda == True:
            self.x = self.x - self.velocidade
        else:
            self.x = self.x + self.velocidade

        if self.x < self.x_inicial - self.distancia: #chegou no limite; vira
            self.virado_esquerda = False
        elif self.x > self.x_inicial + self.distancia:
            self.virado_esquerda = True

        self.rect.centerx = round(self.x)
        self.animar()
        if not self.virado_esquerda:
            self.image = pygame.transform.flip(self.image, True, False)


from config import (GRAVIDADE, INTERVALO_CORTE, VEL_MAX_QUEDA, VEL_PULO, VEL_ANDAR, VEL_AGACHADO)

class Corte(pygame.sprite.Sprite):
    "o golpe de faquinha da raposa. aparece na frente da raposa e some sozinho"

    def __init__(self, imagem, raposa):
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
            self.vx = -velocidade
            self.direcao = -1

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vx = velocidade
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
            # self.assets["som_pulo"].play()


    def agachar(self, quer_agachar):
        if quer_agachar == self.agachada or not self.no_chao and quer_agachar:
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
        # self.assets["som_corte"].play()
    def levar_dano(self):
        """Fica invencível por um tempo e dá um pulinho.""" 
        self.invencivel_ate = pygame.time.get_ticks() + TEMPO_INVENCIVEL 
        self.vy = -8
        #self.assets['som_dano'].play()
    def esta_invencivel(self):
        return pygame.time.get_ticks() < self.invencivel_ate
    



    






     