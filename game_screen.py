"""A tela principal do jogo: o game loop das fases."""
import pygame
from config import (FPS, LARGURA, ALTURA, PRETO, AMARELO, VIDAS_INICIAIS, TEMPO_INVENCIVEL, PONTOS_MOEDA, PONTOS_INIMIGO, PONTOS_PROVAS, SAIR, GAME_OVER, VITORIA)
from sprites import Raposa, PilhaDeProvas, Inimigo
from fases import FASES, construir_fase
from camera import Camera


def desenhar_cenario(janela, assets, camera):
    """Céu fixo + prédios que andam mais devagar (parallax)."""
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
    """Roda todas as fases. Devolve (próximo_estado, pontos)."""
    relogio = pygame.time.Clock()
    vidas = VIDAS_INICIAIS
    pontos = 0
    indice_fase = 0

    # pygame.mixer.music.load('assets/snd/musica.wav')   # Etapa 10
    # pygame.mixer.music.set_volume(0.3)
    # pygame.mixer.music.play(-1)

    while indice_fase < len(FASES):
        # ---------- Monta a fase ----------
        grupos, inicio, largura_fase = construir_fase(FASES[indice_fase], assets)
        grupos['cortes'] = pygame.sprite.Group()
        raposa = Raposa(assets, inicio[0], inicio[1])
        camera = Camera(largura_fase)
        pausado = False
        terminou_fase = False

        # ---------- Loop da fase ----------
        while not terminou_fase:
            relogio.tick(FPS)

            # 1) Trata eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return SAIR, pontos
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return SAIR, pontos
                    if evento.key == pygame.K_p:
                        pausado = not pausado
                    if not pausado:
                        if evento.key in [pygame.K_UP, pygame.K_w, pygame.K_SPACE]:
                            raposa.pular()
                        if evento.key in [pygame.K_x, pygame.K_j]:
                            raposa.cortar(grupos)

            if pausado:
                texto = assets['fonte_grande'].render('PAUSADO', True, AMARELO)
                janela.blit(texto, texto.get_rect(center=(LARGURA // 2, ALTURA // 2)))
                pygame.display.update()
                continue          # pula o resto do loop: nada se move

            # 2) Atualiza o estado do jogo
            raposa.ler_teclado(pygame.key.get_pressed())
            raposa.update(grupos['blocos'])
            grupos['todos'].update()
            grupos['cortes'].update()
            camera.seguir(raposa)

            # 3) Verifica as consequências (colisões)
            acertos = pygame.sprite.groupcollide(grupos['cortes'], grupos['cortaveis'], False, True)
            for alvos in acertos.values():
                for alvo in alvos:
                    if isinstance(alvo, PilhaDeProvas):
                        pontos += PONTOS_PROVAS
                    elif isinstance(alvo, Inimigo):
                        pontos += PONTOS_INIMIGO

            for inimigo in pygame.sprite.spritecollide(raposa, grupos['inimigos'], False):
                if raposa.vy > 0 and raposa.rect.bottom - inimigo.rect.top < 20:
                    inimigo.kill()
                    raposa.vy = -10       # quicada
                    pontos += PONTOS_INIMIGO

            moedas_pegas = pygame.sprite.spritecollide(raposa, grupos['moedas'], True)
            if len(moedas_pegas) > 0:
                pontos += PONTOS_MOEDA * len(moedas_pegas)

            # Perigos (espinhos, galho, jacaré)
            if not raposa.esta_invencivel():
                if len(pygame.sprite.spritecollide(raposa, grupos['perigos'], False)) > 0:
                    vidas -= 1
                    raposa.levar_dano()

            # Caiu num buraco: perde uma vida e volta para o começo da fase
            if raposa.rect.top > ALTURA:
                vidas -= 1
                raposa = Raposa(assets, inicio[0], inicio[1])
                raposa.invencivel_ate = pygame.time.get_ticks() + TEMPO_INVENCIVEL

            if vidas <= 0:
                return GAME_OVER, pontos

            if len(pygame.sprite.spritecollide(raposa, grupos['bandeira'], False)) > 0:
                terminou_fase = True

            # 4) Gera a saída (desenha tudo)
            desenhar_cenario(janela, assets, camera)
            for sprite in grupos['todos']:
                janela.blit(sprite.image, camera.posicao_na_tela(sprite))
            for golpe in grupos['cortes']:
                janela.blit(golpe.image, camera.posicao_na_tela(golpe))
            # Invencível: a raposa pisca
            if not raposa.esta_invencivel() or (pygame.time.get_ticks() // 100) % 2 == 0:
                janela.blit(raposa.image, camera.posicao_na_tela(raposa))
            desenhar_hud(janela, assets, vidas, pontos, indice_fase + 1)
            pygame.display.update()

        # Saiu do loop da fase: vai para a próxima
        indice_fase += 1

    return VITORIA, pontos

            

