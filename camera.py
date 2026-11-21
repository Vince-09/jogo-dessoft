'''Câmera que acompanha a raposa'''
from config import LARGURA

class Camera:
    '''Guarda quanto o mundo esta está deslocando em relação à janela'''

    def __init__(self,largura_fase):
        self.deslocamento_x = 0
        self.largura_fase = largura_fase

    def seguir(self, alvo):
        '''Centraliza a câmera sem passar da borda da fase'''
        self.deslocamento_x = alvo.rect.centerx - LARGURA//2
        if self.deslocamento_x < 0:
            self.deslocamento_x = 0
        maximo = self.largura_fase - LARGURA
        if self.deslocamento_x > maximo:
            self.deslocamento_x = maximo

    def posicao_na_tela(self, sprite):
        '''Retangulo que a imagem do sprite deve ser desenhada'''
        retangulo = sprite.image.get_rect()
        retangulo.midbottom = sprite.rect.midbottom
        retangulo.x -= self.deslocamento_x
        return retangulo
