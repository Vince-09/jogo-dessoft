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