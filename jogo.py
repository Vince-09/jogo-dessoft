import pygame 
from config import LARGURA, ALTURA, TITULO, FPS, AZUL_CEU
# ----- Inicialização ----
pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
relogio = pygame.time.Clock()
# ----- Loop principal ----
rodando = True
while rodando:
     relogio.tick(FPS)    # no máximo 60 voltas por segundo 
     for evento in pygame.event.get():     # 1) trata eventos 
        if evento.type == pygame.QUIT:
             rodando = False
     janela.fill(AZUL_CEU)                # 4) gera saídas
     pygame.display.update() 
# ----- Finalização ----
pygame.quit()